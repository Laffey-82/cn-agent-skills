"""技术文档检查脚本:检查 Markdown 文档的结构问题。

用法:
    python doc_checker.py README.md
    python doc_checker.py README.md --require 快速开始 使用示例

检查项:
- 相对链接指向的文件是否存在(不检查 http/https/锚点);
- 代码围栏是否配对;
- 是否残留占位符(TODO/待补充/【】);
- 章节是否为空;
- --require 指定的必需章节是否缺失。

脚本只做标记,结论需要人确认。示例能不能跑通由人验证,脚本不代替。
"""

import argparse
import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^\s*```")
HEADING_RE = re.compile(r"^(#{2,4})\s+(.+?)\s*$")
PLACEHOLDER_RE = re.compile(r"(TODO|TBD|XXX|待补充|【[^】]*】)")


def in_fence(lines: list[str], idx: int) -> bool:
    """判断第 idx 行(0 基)是否在代码围栏内。"""
    count = 0
    for line in lines[: idx + 1]:
        if FENCE_RE.match(line):
            count += 1
    return count % 2 == 1


def check_doc(path: Path, required: list[str]) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        findings.append((0, "必须", f"无法读取文件:{path}"))
        return findings

    # 代码围栏配对
    fence_count = sum(1 for line in lines if FENCE_RE.match(line))
    if fence_count % 2 == 1:
        findings.append((0, "必须", f"代码围栏数量为奇数({fence_count}),Markdown 会渲染错乱"))

    headings: list[tuple[int, int, str]] = []
    fence_open = False
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            fence_open = not fence_open
            continue
        if fence_open:
            continue
        m = HEADING_RE.match(line)
        if m:
            headings.append((i, len(m.group(1)), m.group(2).strip()))

    # 必需章节
    found = {title for _, _, title in headings}
    for name in required:
        if name not in found:
            findings.append((0, "必须", f"缺少必需章节 '{name}'"))

    # 空章节:标题到下一个标题之间没有正文,子标题算内容
    for idx, (lineno, level, title) in enumerate(headings):
        end = len(lines) - 1
        for other_lineno, other_level, _ in headings[idx + 1 :]:
            if other_level <= level:
                end = other_lineno - 1
                break
        body = lines[lineno : end + 1]
        has_content = any(
            line.strip() and not FENCE_RE.match(line) and not HEADING_RE.match(line)
            for line in body
        )
        if not has_content:
            findings.append((lineno, "建议", f"章节 '{title}' 为空,补内容或删掉"))

    # 占位符 + 坏链接(跳过围栏内)
    for idx, line in enumerate(lines):
        lineno = idx + 1
        if in_fence(lines, idx):
            continue

        if PLACEHOLDER_RE.search(line):
            findings.append((lineno, "建议", "残留占位符(TODO/待补充/【】),确认是否已填"))

        for link in LINK_RE.findall(line):
            target = link.strip().strip("<>")
            if not target:
                findings.append((lineno, "必须", "空链接,补上目标地址"))
                continue
            if target.startswith(("http://", "https://", "mailto:", "//", "#")):
                continue
            file_part = target.split("#", 1)[0]
            if not file_part:
                continue
            resolved = (path.parent / file_part).resolve()
            if not resolved.exists():
                findings.append((lineno, "必须", f"相对链接指向的文件不存在:{target}"))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="技术文档检查")
    parser.add_argument("files", nargs="+", help="Markdown 文档路径")
    parser.add_argument("--require", nargs="*", default=[], help="必需章节名,按 ## 标题匹配")
    parser.add_argument("--strict", action="store_true", help="存在'必须'级问题时以非零码退出(用于 CI)")
    args = parser.parse_args()

    total = 0
    total_must = 0
    for file_arg in args.files:
        path = Path(file_arg)
        findings = check_doc(path, args.require)
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

    print(f"\n共检查 {len(args.files)} 个文档,标记 {total} 项。请逐条人工确认后再定稿。")
    if args.strict and total_must > 0:
        print("strict 模式:存在'必须'级问题,退出码 1。")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
