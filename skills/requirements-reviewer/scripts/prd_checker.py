"""需求文档(PRD)检查脚本:检查需求文档的结构完整性,输出缺口清单。

用法:
    python prd_checker.py <需求文档.md>

检查项:
- 必需章节是否齐全且非空(背景与目标、功能范围、验收标准、边界与异常);
- 功能范围是否同时写了"做"和"不做";
- 验收标准是否含糊(没法据此写测试);
- 是否残留占位符。

脚本只做标记,评审结论需要人确认。
"""

import argparse
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = ["背景与目标", "功能范围", "验收标准", "边界与异常"]
RECOMMENDED_SECTIONS = ["用户与场景", "需求明细", "优先级", "上线与指标"]
FENCE_RE = re.compile(r"^\s*```")
HEADING_RE = re.compile(r"^(#{2,4})\s+(.+?)\s*$")
VAGUE_RE = re.compile(r"(做好就行|差不多|尽量|完善|正常(使用|运行)|后续再说|待定)")
PLACEHOLDER_RE = re.compile(r"(TODO|TBD|待补充|【[^】]*】)")


def in_fence(lines: list[str], idx: int) -> bool:
    count = 0
    for line in lines[: idx + 1]:
        if FENCE_RE.match(line):
            count += 1
    return count % 2 == 1


def check_prd(path: Path) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        findings.append((0, "必须", f"无法读取文件:{path}"))
        return findings

    headings: list[tuple[int, int, str]] = []
    for i, line in enumerate(lines, 1):
        if in_fence(lines, i - 1):
            continue
        m = HEADING_RE.match(line)
        if m:
            headings.append((i, len(m.group(1)), m.group(2).strip()))
    found = {title for _, _, title in headings}

    for name in REQUIRED_SECTIONS:
        if name not in found:
            findings.append((0, "必须", f"缺少章节 '## {name}'"))
    for name in RECOMMENDED_SECTIONS:
        if name not in found:
            findings.append((0, "建议", f"建议补章节 '## {name}'"))

    for idx, (lineno, level, title) in enumerate(headings):
        end = len(lines) - 1
        for other_lineno, other_level, _ in headings[idx + 1 :]:
            if other_level <= level:
                end = other_lineno - 1
                break
        body = lines[lineno : end + 1]
        if not any(l.strip() and not FENCE_RE.match(l) and not HEADING_RE.match(l) for l in body):
            findings.append((lineno, "必须", f"章节 '{title}' 为空,补内容或删掉"))

    for idx, (lineno, level, title) in enumerate(headings):
        if title != "功能范围":
            continue
        end = len(lines) - 1
        for other_lineno, other_level, _ in headings[idx + 1 :]:
            if other_level <= level:
                end = other_lineno - 1
                break
        section_text = "\n".join(lines[lineno : end + 1])
        has_do = bool(re.search(r"(必须做|做:|范围)", section_text))
        has_not = bool(re.search(r"(不做|非目标|不在本次范围)", section_text))
        if not (has_do and has_not):
            findings.append((lineno, "建议", "功能范围建议同时写清'做'和'不做',防止暗含需求"))
        break

    for idx, (lineno, level, title) in enumerate(headings):
        if title != "验收标准":
            continue
        end = len(lines) - 1
        for other_lineno, other_level, _ in headings[idx + 1 :]:
            if other_level <= level:
                end = other_lineno - 1
                break
        for j, line in enumerate(lines[lineno : end + 1], start=lineno):
            if VAGUE_RE.search(line):
                findings.append((j, "建议", "验收标准疑似含糊,换成可测试的表述"))
        break

    for i, line in enumerate(lines, 1):
        if PLACEHOLDER_RE.search(line) and not in_fence(lines, i - 1):
            findings.append((i, "建议", "残留占位符(TODO/待补充/【】),确认是否已填"))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="需求文档检查")
    parser.add_argument("files", nargs="+", help="需求文档 Markdown 文件")
    parser.add_argument("--strict", action="store_true", help="存在'必须'级问题时以非零码退出(用于 CI)")
    args = parser.parse_args()

    total = 0
    total_must = 0
    for file_arg in args.files:
        path = Path(file_arg)
        findings = check_prd(path)
        must = sum(1 for _, level, _ in findings if level == "必须")
        suggest = len(findings) - must
        total += len(findings)
        total_must += must

        print(f"\n== {path} ==")
        if not findings:
            print("  未发现问题")
            continue
        for lineno, level, note in findings:
            loc = f"L{lineno}" if lineno else "结构"
            print(f"  {loc:<6} [{level}] {note}")
        verdict = "不通过" if must else ("修改后通过" if suggest else "通过")
        print(f"  结论:{verdict}(必须 {must} 项,建议 {suggest} 项)")

    print(f"\n共检查 {len(args.files)} 份需求,标记 {total} 项。请逐条人工确认后再定评审结论。")
    if args.strict and total_must > 0:
        print("strict 模式:存在'必须'级问题,退出码 1。")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
