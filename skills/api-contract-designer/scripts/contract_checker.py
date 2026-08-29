"""API 契约检查脚本:校验契约 JSON 的完整性。

用法:
    python contract_checker.py --new contract.json   # 生成契约模板
    python contract_checker.py contract.json         # 校验契约

检查项:
- name/base_path/endpoints 是否合法;
- 方法白名单、路径以 / 开头;
- 路径参数 {x} 是否有对应 in=path 参数;
- 必填参数是否有类型;
- 每个接口至少一个响应;
- method+path 是否重复。

脚本只做标记,结论需要人确认。
"""

import argparse
import json
import re
import sys
from pathlib import Path

ALLOWED_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}
ALLOWED_LOCATIONS = {"path", "query", "header", "body"}

TEMPLATE = {
    "name": "api-contract",
    "version": "0.1.0",
    "base_path": "/api",
    "endpoints": [
        {
            "method": "GET",
            "path": "/items",
            "summary": "列表",
            "auth": "none",
            "params": [{"name": "page", "in": "query", "type": "int", "required": False}],
            "responses": {"200": {"desc": "成功"}},
            "error_codes": [400],
        },
        {
            "method": "GET",
            "path": "/items/{id}",
            "summary": "详情",
            "auth": "none",
            "params": [{"name": "id", "in": "path", "type": "string", "required": True}],
            "responses": {"200": {"desc": "成功"}, "404": {"desc": "不存在"}},
            "error_codes": [404],
        },
    ],
}


def check_contract(contract: dict) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    if not isinstance(contract, dict):
        return [(0, "必须", "契约必须是 JSON 对象")]
    if not isinstance(contract.get("name"), str) or not contract["name"].strip():
        findings.append((0, "必须", "name 必须是非空字符串"))
    if "version" not in contract:
        findings.append((0, "建议", "建议补 version,方便契约版本管理"))
    base_path = contract.get("base_path", "")
    if not isinstance(base_path, str) or not base_path.startswith("/"):
        findings.append((0, "必须", "base_path 应以 / 开头"))

    endpoints = contract.get("endpoints")
    if not isinstance(endpoints, list) or not endpoints:
        findings.append((0, "必须", "endpoints 必须是非空数组"))
        return findings

    seen = set()
    for idx, ep in enumerate(endpoints, 1):
        if not isinstance(ep, dict):
            findings.append((0, "必须", f"endpoint {idx} 必须是对象"))
            continue
        method = ep.get("method", "").upper()
        path = ep.get("path", "")
        if method not in ALLOWED_METHODS:
            findings.append((0, "必须", f"endpoint {idx} method '{ep.get('method')}' 不在 {sorted(ALLOWED_METHODS)}"))
        if not isinstance(path, str) or not path.startswith("/"):
            findings.append((0, "必须", f"endpoint {idx} path 应以 / 开头"))
        if not ep.get("summary"):
            findings.append((0, "建议", f"endpoint {idx} 建议补 summary"))
        if "auth" not in ep:
            findings.append((0, "建议", f"endpoint {idx} 建议写明 auth(认证方式)"))

        key = (method, path)
        if key in seen:
            findings.append((0, "必须", f"endpoint {idx} 的 {method} {path} 重复"))
        seen.add(key)

        params = ep.get("params") or []
        names = []
        placeholders = re.findall(r"\{(\w+)\}", path)
        path_param_names = []
        for p in params:
            if not isinstance(p, dict):
                findings.append((0, "必须", f"endpoint {idx} 的参数必须是对象"))
                continue
            pname = p.get("name")
            if pname in names:
                findings.append((0, "必须", f"endpoint {idx} 参数名 '{pname}' 重复"))
            names.append(pname)
            if p.get("in") not in ALLOWED_LOCATIONS:
                findings.append((0, "必须", f"endpoint {idx} 参数 '{pname}' 的 in 不在 {sorted(ALLOWED_LOCATIONS)}"))
            if p.get("required") and not p.get("type"):
                findings.append((0, "必须", f"endpoint {idx} 必填参数 '{pname}' 缺 type"))
            if p.get("in") == "path":
                path_param_names.append(pname)

        for ph in placeholders:
            if ph not in path_param_names:
                findings.append((0, "必须", f"endpoint {idx} 路径参数 {{{ph}}} 没有对应的 in=path 参数"))

        responses = ep.get("responses")
        if not isinstance(responses, dict) or not responses:
            findings.append((0, "必须", f"endpoint {idx} 至少需要一个响应(如 200)"))
        elif not any(code.startswith("2") for code in responses):
            findings.append((0, "建议", f"endpoint {idx} 建议有一个 2xx 成功响应"))

        for code in ep.get("error_codes") or []:
            if not isinstance(code, int):
                findings.append((0, "必须", f"endpoint {idx} error_codes 里的 '{code}' 必须是数字"))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="API 契约检查")
    parser.add_argument("contract", nargs="?", help="契约 JSON 文件")
    parser.add_argument("--new", metavar="FILE", help="生成契约模板")
    parser.add_argument("--strict", action="store_true", help="存在'必须'级问题时以非零码退出(用于 CI)")
    args = parser.parse_args()

    if args.new:
        target = Path(args.new)
        if target.exists():
            print(f"文件已存在,不覆盖:{target}")
            return 1
        target.write_text(json.dumps(TEMPLATE, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"契约模板已生成:{target}")
        return 0
    if not args.contract:
        parser.error("需要 contract 文件或 --new")

    try:
        contract = json.loads(Path(args.contract).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"无法读取契约 {args.contract}:{exc}")
        return 1

    findings = check_contract(contract)
    must = sum(1 for _, level, _ in findings if level == "必须")
    suggest = len(findings) - must
    print(f"== {args.contract} ==")
    if not findings:
        print("  未发现问题")
    else:
        for lineno, level, note in findings:
            print(f"  [{level}] {note}")
        verdict = "不通过" if must else ("修改后通过" if suggest else "通过")
        print(f"  结论:{verdict}(必须 {must} 项,建议 {suggest} 项)")
    print("脚本只做标记,契约是否合理需要人确认。")
    if args.strict and must > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
