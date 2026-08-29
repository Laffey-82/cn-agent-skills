"""技术方案文档检查脚本:检查方案文档的完整性。

用法:
    python design_checker.py <方案.md>

检查项:
- 必需章节是否齐全且非空(背景与目标、方案对比、风险与应对);
- 方案对比是否至少两个方案;
- 选型结论是否给出理由;
- 风险是否每条有应对;
- 是否残留占位符。

脚本只做标记,结论需要人确认。
"""

import argparse
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = ["背景与目标", "方案对比", "风险与应对"]
RECOMMENDED_SECTIONS = ["选型结论", "架构设计", "数据模型", "接口设计", "关键流程", "上线与回滚"]
FENCE_RE = re.compile(r"^\s*```")
HEADING_RE = re.compile(r"^(#{2,4})\s+(.+?)\s*$")
PLACEHOLDER_RE = re.compile(r"(TODO|TBD|待补充|【[^】]*】)")


def in_fence(lines: list[str], idx: int) -> bool:
    count = 0
    for line in lines[: idx + 1]:
        if FENCE_RE.match(line):
            count += 1
    return count % 2 == 1


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def check_design(path: Path) -> list[tuple[int, str, str]]:
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

    # 方案对比:至少两个方案(表格数据行或编号列表)
    if "方案对比" in found:
        for idx, (lineno, level, title) in enumerate(headings):
            if title != "方案对比":
                continue
            end = len(lines) - 1
            for other_lineno, other_level, _ in headings[idx + 1 :]:
                if other_level <= level:
                    end = other_lineno - 1
                    break
            section = lines[lineno : end + 1]
            table_rows = 0
            bullet_count = 0
            for line in section:
                if line.strip().startswith("|") and is_separator_like(line):
                    continue
                if line.strip().startswith("|") and not re.match(r"^\|[\s:\-|]+\|$", line):
                    table_rows += 1
                if re.match(r"^\s*[-*]\s*(方案|Option|A[.:]|B[.:])", line, re.IGNORECASE):
                    bullet_count += 1
            if table_rows < 2 and bullet_count < 2:
                findings.append((lineno, "建议", "方案对比至少列两个方案(表格两行或两条编号)"))
            break

    # 选型结论:给出理由
    if "选型结论" in found:
        for idx, (lineno, level, title) in enumerate(headings):
            if title != "选型结论":
                continue
            end = len(lines) - 1
            for other_lineno, other_level, _ in headings[idx + 1 :]:
                if other_level <= level:
                    end = other_lineno - 1
                    break
            section_text = "\n".join(lines[lineno : end + 1])
            if not any(l.strip() for l in lines[lineno : end + 1]):
                findings.append((lineno, "必须", "选型结论为空"))
            elif not re.search(r"(选|因为|理由|成本|不选|权衡)", section_text):
                findings.append((lineno, "建议", "选型结论建议写明理由(为什么选这个不选那个)"))
            break

    # 风险与应对:至少出现"应对"
    if "风险与应对" in found:
        for idx, (lineno, level, title) in enumerate(headings):
            if title != "风险与应对":
                continue
            end = len(lines) - 1
            for other_lineno, other_level, _ in headings[idx + 1 :]:
                if other_level <= level:
                    end = other_lineno - 1
                    break
            section_text = "\n".join(lines[lineno : end + 1])
            if "应对" not in section_text and "对策" not in section_text:
                findings.append((lineno, "建议", "风险章节建议每条风险配'应对',别只列现象"))
            break

    for i, line in enumerate(lines, 1):
        if PLACEHOLDER_RE.search(line) and not in_fence(lines, i - 1):
            findings.append((i, "建议", "残留占位符(TODO/待补充/【】),确认是否已填"))

    return findings


def is_separator_like(line: str) -> bool:
    cells = split_row(line)
    return bool(cells) and all(re.fullmatch(r":?-+:?", cell.strip()) for cell in cells)


def main() -> int:
    parser = argparse.ArgumentParser(description="技术方案检查")
    parser.add_argument("files", nargs="+", help="方案 Markdown 文件")
    parser.add_argument("--strict", action="store_true", help="存在'必须'级问题时以非零码退出(用于 CI)")
    args = parser.parse_args()

    total = 0
    total_must = 0
    for file_arg in args.files:
        path = Path(file_arg)
        findings = check_design(path)
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

    print(f"\n共检查 {len(args.files)} 个方案,标记 {total} 项。请逐条人工确认后再评审。")
    if args.strict and total_must > 0:
        print("strict 模式:存在'必须'级问题,退出码 1。")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
