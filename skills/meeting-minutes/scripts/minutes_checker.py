"""会议纪要检查脚本:检查纪要的落地性。

用法:
    python minutes_checker.py <会议纪要.md>

检查项:
- 必需章节是否齐全(结论与决定、待办事项);
- 待办表格是否含"事项/负责人/截止时间"列;
- 每条待办是否有明确负责人(不能是"团队/相关部门/待定");
- 每条待办是否有具体截止日期(不能是"尽快/下周");
- 是否残留占位符。

脚本只做标记,结论需要人确认。
"""

import argparse
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = ["结论与决定", "待办事项"]
RECOMMENDED_SECTIONS = ["会议信息", "风险与需跟进"]
REQUIRED_COLUMNS = ["事项", "负责人", "截止时间"]
FENCE_RE = re.compile(r"^\s*```")
HEADING_RE = re.compile(r"^#{2,4}\s+(.+?)\s*$")
VAGUE_OWNER_RE = re.compile(r"(团队|相关部门|负责人|待定|TBD|某某)")
SOFT_DEADLINE_RE = re.compile(r"(尽快|下周|近期|之后|到时候|待定|TBD|再说)")
DATE_RE = re.compile(r"\d{4}[-/年]\d{1,2}([-/月]\d{1,2}日?)?")
PLACEHOLDER_RE = re.compile(r"(TODO|TBD|待补充|【[^】]*】)")


def in_fence(lines: list[str], idx: int) -> bool:
    count = 0
    for line in lines[: idx + 1]:
        if FENCE_RE.match(line):
            count += 1
    return count % 2 == 1


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(line: str) -> bool:
    cells = split_row(line)
    return bool(cells) and all(re.fullmatch(r":?-+:?", cell.strip()) for cell in cells)


def check_minutes(path: Path) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        findings.append((0, "必须", f"无法读取文件:{path}"))
        return findings

    headings: list[tuple[int, str]] = []
    for i, line in enumerate(lines, 1):
        if in_fence(lines, i - 1):
            continue
        m = HEADING_RE.match(line)
        if m:
            headings.append((i, m.group(1).strip()))
    found = {title for _, title in headings}

    for name in REQUIRED_SECTIONS:
        if name not in found:
            findings.append((0, "必须", f"缺少章节 '## {name}'"))
    for name in RECOMMENDED_SECTIONS:
        if name not in found:
            findings.append((0, "建议", f"建议补章节 '## {name}'"))

    # 找待办表格:含 事项/负责人/截止时间 列的表
    action_table = None
    tables = []
    i = 0
    while i < len(lines):
        if not in_fence(lines, i) and lines[i].strip().startswith("|") and i + 1 < len(lines) and is_separator(lines[i + 1]):
            header = split_row(lines[i])
            rows = []
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append((j + 1, split_row(lines[j])))
                j += 1
            tables.append((i + 1, header, rows))
            i = j
            continue
        i += 1

    for header_lineno, header, rows in tables:
        if all(col in header for col in REQUIRED_COLUMNS):
            action_table = (header_lineno, header, rows)
            break

    if action_table is None:
        findings.append((0, "必须", "未找到待办表格(需要'事项/负责人/截止时间'三列)"))
        return findings

    header_lineno, header, rows = action_table
    col = {name: header.index(name) for name in REQUIRED_COLUMNS}
    if "交付标准" in header:
        deliverable_idx = header.index("交付标准")
    else:
        deliverable_idx = None
        findings.append((header_lineno, "建议", "待办表格建议补'交付标准'列,让'做完'有定义"))

    for lineno, cells in rows:
        if len(cells) < len(header):
            cells = cells + [""] * (len(header) - len(cells))
        owner = cells[col["负责人"]].strip()
        deadline = cells[col["截止时间"]].strip()
        item = cells[col["事项"]].strip()

        if not item:
            findings.append((lineno, "必须", "待办事项为空"))
        if not owner:
            findings.append((lineno, "必须", "待办缺少负责人"))
        elif VAGUE_OWNER_RE.search(owner):
            findings.append((lineno, "建议", f"负责人 '{owner}' 不够具体,写到具体的人"))
        if not deadline:
            findings.append((lineno, "必须", "待办缺少截止时间"))
        elif SOFT_DEADLINE_RE.search(deadline):
            findings.append((lineno, "建议", f"截止时间 '{deadline}' 不够具体,写具体日期"))
        elif not DATE_RE.search(deadline):
            findings.append((lineno, "建议", f"截止时间 '{deadline}' 建议写成 YYYY-MM-DD"))
        if deliverable_idx is not None and not cells[deliverable_idx].strip():
            findings.append((lineno, "建议", "交付标准为空,建议写明'做完'长什么样"))

        for cell in cells:
            if PLACEHOLDER_RE.search(cell):
                findings.append((lineno, "建议", "残留占位符,确认是否已填"))
                break

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="会议纪要检查")
    parser.add_argument("files", nargs="+", help="会议纪要 Markdown 文件")
    parser.add_argument("--strict", action="store_true", help="存在'必须'级问题时以非零码退出(用于 CI)")
    args = parser.parse_args()

    total = 0
    total_must = 0
    for file_arg in args.files:
        path = Path(file_arg)
        findings = check_minutes(path)
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

    print(f"\n共检查 {len(args.files)} 份纪要,标记 {total} 项。请逐条人工确认后再分发。")
    if args.strict and total_must > 0:
        print("strict 模式:存在'必须'级问题,退出码 1。")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
