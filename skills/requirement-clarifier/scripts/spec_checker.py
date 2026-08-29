"""需求规格检查脚本:检查需求规格文档的完整性和可执行性。

用法:
    python spec_checker.py <需求规格.md>
    python spec_checker.py <多个文件...>

检查项:
- 必需章节是否齐全(背景与目标、用户与场景、功能范围、验收标准、边界与异常、约束条件、待确认问题);
- 章节是否为空(标题下没有内容);
- 功能范围是否同时写明"必须做"和"不做";
- 验收标准是否含糊(空泛词、没有条目);
- 是否残留未填占位符(待确认问题章节里的除外)。

脚本只做标记,结论需要人确认。模板见 references/SPEC_TEMPLATE.md。
"""

import argparse
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "背景与目标",
    "用户与场景",
    "功能范围",
    "验收标准",
    "边界与异常",
    "约束条件",
    "待确认问题",
]

HEADING_RE = re.compile(r"^#{2,3}\s+(.+?)\s*$")
VAGUE_ACCEPT_RE = re.compile(r"(做好就行|差不多|尽量|大概|完善|正常(使用|运行|操作)|后续再说|到时候看)")
PLACEHOLDER_RE = re.compile(r"(TODO|TBD|XXX|待补充|【[^】]*】)")


def parse_document(lines: list[str]) -> tuple[dict[str, tuple[int, int]], list[str]]:
    """返回 (章节名 -> (起始行, 结束行)), 以及按行号切出的各章节正文列表。"""
    headings: list[tuple[int, str]] = []
    for i, line in enumerate(lines, 1):
        m = HEADING_RE.match(line)
        if m:
            headings.append((i, m.group(1).strip()))

    sections: dict[str, tuple[int, int]] = {}
    for idx, (start, title) in enumerate(headings):
        end = headings[idx + 1][0] - 1 if idx + 1 < len(headings) else len(lines)
        sections[title] = (start, end)
    return sections, [line for line in lines]


def check_spec(path: Path) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        findings.append((0, "必须", f"无法读取文件:{path}"))
        return findings

    sections, _ = parse_document(lines)

    for name in REQUIRED_SECTIONS:
        if name not in sections:
            findings.append((0, "必须", f"缺少章节 '## {name}'"))

    for name, (start, end) in sections.items():
        body = [line.strip() for line in lines[start:end]]
        has_content = any(line for line in body if line and not line.startswith("#"))
        if not has_content:
            findings.append((start, "必须", f"章节 '{name}' 为空,补内容或删掉"))

    if "功能范围" in sections:
        start, end = sections["功能范围"]
        body = "\n".join(lines[start:end])
        if "必须做" not in body or "不做" not in body:
            findings.append((start, "建议", "功能范围建议同时写明'必须做'和'不做'"))

    if "验收标准" in sections:
        start, end = sections["验收标准"]
        body_lines = [line for line in lines[start:end] if line.strip()]
        bullet_count = sum(1 for line in body_lines if re.match(r"^\s*[-*]", line))
        for i, line in enumerate(lines[start:end], start):
            if VAGUE_ACCEPT_RE.search(line):
                findings.append((i, "建议", "验收标准疑似含糊,换成可验证的表述(如'用户能添加任务,输入标题和日期')"))
        if bullet_count == 0:
            findings.append((start, "建议", "验收标准没有条目,建议逐条列出"))

    for i, line in enumerate(lines, 1):
        if PLACEHOLDER_RE.search(line):
            section_of = "待确认问题"
            for name, (s, e) in sections.items():
                if s <= i <= e:
                    section_of = name
                    break
            if section_of != "待确认问题":
                findings.append((i, "建议", "残留占位符(TODO/待补充/【】),确认是否已填"))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="需求规格检查")
    parser.add_argument("files", nargs="+", help="需求规格 Markdown 文件")
    args = parser.parse_args()

    total = 0
    for file_arg in args.files:
        path = Path(file_arg)
        findings = check_spec(path)
        must = sum(1 for _, level, _ in findings if level == "必须")
        suggest = len(findings) - must
        total += len(findings)

        print(f"\n== {path} ==")
        if not findings:
            print("  未发现问题")
            continue
        for lineno, level, note in findings:
            loc = f"L{lineno}" if lineno else "结构"
            print(f"  {loc:<6} [{level}] {note}")
        verdict = "不通过" if must else ("修改后通过" if suggest else "通过")
        print(f"  结论:{verdict}(必须 {must} 项,建议 {suggest} 项)")

    print(f"\n共检查 {len(args.files)} 个文档,标记 {total} 项。请逐条人工确认后再定稿。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
