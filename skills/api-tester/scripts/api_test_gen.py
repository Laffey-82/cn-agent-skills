"""API 契约测试骨架生成脚本:把契约 JSON 转成 pytest 测试文件。

用法:
    python api_test_gen.py --new contract.json              # 生成契约模板
    python api_test_gen.py contract.json -o test_login.py   # 生成 pytest 骨架

契约格式见 --new 生成的模板。脚本只生成骨架,用例和断言要按实际契约
核对后再执行,不要在没确认环境的情况下跑测试。
"""

import argparse
import json
import re
import sys
from pathlib import Path

ALLOWED_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}
TYPE_NAMES = {"str", "int", "float", "bool", "list", "dict"}

TEMPLATE_CONTRACT = {
    "name": "api-contract",
    "base_path": "/api",
    "cases": [
        {
            "name": "正常路径示例",
            "method": "GET",
            "path": "/ping",
            "headers": {"Accept": "application/json"},
            "params": {},
            "path_params": {},
            "body": None,
            "expected_status": 200,
            "expected_fields": {"message": "str"},
        },
        {
            "name": "异常路径示例",
            "method": "GET",
            "path": "/items/{id}",
            "headers": {},
            "params": {},
            "path_params": {"id": 1},
            "body": None,
            "expected_status": 404,
            "expected_fields": {},
        },
    ],
}


def validate_contract(contract: dict) -> list[str]:
    errors = []
    if not isinstance(contract, dict):
        return ["契约必须是 JSON 对象"]
    if not isinstance(contract.get("name"), str) or not contract["name"].strip():
        errors.append("name 必须是非空字符串")
    cases = contract.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("cases 必须是非空数组")
        return errors
    for idx, case in enumerate(cases, 1):
        if not isinstance(case, dict):
            errors.append(f"用例 {idx} 必须是对象")
            continue
        method = case.get("method", "").upper()
        if method not in ALLOWED_METHODS:
            errors.append(f"用例 {idx} method '{case.get('method')}' 不在 {sorted(ALLOWED_METHODS)} 中")
        path = case.get("path", "")
        if not isinstance(path, str) or not path.startswith("/"):
            errors.append(f"用例 {idx} path 应以 / 开头")
        if not isinstance(case.get("expected_status"), int):
            errors.append(f"用例 {idx} expected_status 必须是整数")
    return errors


def py_literal(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=None)


def render_case(case: dict, index: int, base_path: str = "") -> str:
    name = case.get("name") or f"用例 {index}"
    method = case["method"].upper()
    path = case["path"]
    if base_path and not path.startswith(base_path):
        path = base_path + path
    path_params = case.get("path_params") or {}
    for key, value in path_params.items():
        path = path.replace("{" + key + "}", str(value))

    headers = case.get("headers") or {}
    params = case.get("params") or {}
    body = case.get("body")
    expected = case["expected_status"]
    fields = case.get("expected_fields") or {}

    lines = [
        f"def test_case_{index}():",
        f'    """{name}:{method} {path} 期望 {expected}"""',
    ]
    kwargs = []
    if headers:
        kwargs.append(f"        headers={py_literal(headers)},")
    if params:
        kwargs.append(f"        params={py_literal(params)},")
    if body is not None:
        kwargs.append(f"        json={py_literal(body)},")
    if kwargs:
        lines.append(f'    resp = _request("{method}", {py_literal(path)},')
        lines.extend(kwargs)
        lines.append("    )")
    else:
        lines.append(f'    resp = _request("{method}", {py_literal(path)})')
    lines.append(f"    assert resp.status_code == {expected}, f\"状态码 {{resp.status_code}} != {expected},响应:{{resp.text}}\"")
    lines.append("    data = resp.json()")
    for field, kind in fields.items():
        lines.append(f'    assert "{field}" in data, f"响应缺少字段 {field}:{{data}}"')
        if kind in TYPE_NAMES:
            lines.append(f"    assert isinstance(data[\"{field}\"], {kind}), f\"字段 {field} 类型不对:{{data}}\"")
    return "\n".join(lines)


def render_file(contract: dict) -> str:
    name = contract["name"]
    cases = contract["cases"]
    base_path = contract.get("base_path") or ""
    blocks = [f'"""接口测试骨架:{name}。']
    blocks.append("")
    blocks.append("由 api_test_gen.py 生成。用例和断言按实际契约核对后再执行。")
    blocks.append("运行:API_BASE_URL=http://127.0.0.1:8000 pytest <本文件>")
    blocks.append('"""')
    blocks.append("")
    blocks.append("import os")
    blocks.append("")
    blocks.append("import requests")
    blocks.append("")
    blocks.append('BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000")')
    blocks.append("TIMEOUT = 10")
    blocks.append("")
    blocks.append("")
    blocks.append("def _request(method, path, **kwargs):")
    blocks.append('    return requests.request(method, f"{BASE_URL}{path}", timeout=TIMEOUT, **kwargs)')
    blocks.append("")
    for idx, case in enumerate(cases, 1):
        blocks.append(render_case(case, idx, base_path))
        blocks.append("")
    return "\n".join(blocks)


def main() -> int:
    parser = argparse.ArgumentParser(description="API 契约测试骨架生成")
    parser.add_argument("contract", nargs="?", help="契约 JSON 文件路径")
    parser.add_argument("--new", metavar="FILE", help="生成契约模板文件")
    parser.add_argument("-o", "--out", default=None, help="输出 pytest 文件,默认 test_api.py")
    args = parser.parse_args()

    if args.new:
        target = Path(args.new)
        if target.exists():
            print(f"文件已存在,不覆盖:{target}")
            return 1
        target.write_text(json.dumps(TEMPLATE_CONTRACT, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"契约模板已生成:{target}")
        print("填好后运行:python api_test_gen.py <契约文件> -o <测试文件>")
        return 0

    if not args.contract:
        parser.error("需要 contract 文件或 --new")

    contract_path = Path(args.contract)
    try:
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"无法读取契约文件 {contract_path}:{exc}")
        return 1

    errors = validate_contract(contract)
    if errors:
        print("契约校验失败:")
        for error in errors:
            print(f"  - {error}")
        return 1

    out = Path(args.out) if args.out else Path("test_api.py")
    out.write_text(render_file(contract), encoding="utf-8")
    print(f"已生成:{out}")
    print("核对用例和断言后,再按文件头说明运行。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
