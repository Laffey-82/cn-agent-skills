"""代码审查辅助脚本:扫描改动文件,标记常见问题位置。

用法:
    python review_helper.py [--base main] [--head HEAD]

只做"标记",结论需要人确认。脚本不判定对错,只把可疑点列出来。
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def git_diff(base: str, head: str) -> str:
    result = subprocess.run(
        ["git", "diff", "--stat", f"{base}...{head}"],
        capture_output=True,
        text=True,
    )
    return result.stdout


def changed_files(base: str, head: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...{head}"],
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def scan_file(path: Path) -> list[tuple[str, int, str]]:
    """返回 [(行号, 模式, 说明)]"""
    findings: list[tuple[str, int, str]] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return findings

    patterns = [
        (re.compile(r"(?i)(password|secret|token|api[_-]?key)\s*=\s*['\"][^'\"]+['\"]"), "疑似硬编码密钥"),
        (re.compile(r"except\s*:\s*(pass|#.*)?$"), "裸 except 且无处理,可能吞异常"),
        (re.compile(r"(?i)\b(todo|fixme|hack)\b"), "遗留 TODO/FIXME"),
        (re.compile(r"innerHTML\s*=|v-html\s*="), "直接渲染 HTML,需确认是否含用户输入"),
        (re.compile(r"eval\s*\(|exec\s*\("), "动态执行,需确认输入来源"),
        (re.compile(r"SELECT\s+.+\s+FROM\s+.+\s*\+"), "疑似字符串拼接 SQL"),
        (re.compile(r"(?i)print\s*\(|console\.log\s*\("), "调试输出残留(需确认是否应删除)"),
    ]

    for i, line in enumerate(lines, 1):
        for pattern, note in patterns:
            if pattern.search(line):
                findings.append((i, pattern.pattern[:30], note))
                break  # 每行最多报一个,减少噪音
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="代码审查辅助")
    parser.add_argument("--base", default="main", help="基线分支,默认 main")
    parser.add_argument("--head", default="HEAD", help="对比对象,默认 HEAD")
    args = parser.parse_args()

    print(f"== 改动概览 ==\n{git_diff(args.base, args.head)}")
    files = changed_files(args.base, args.head)
    if not files:
        print("没有检测到改动文件。")
        return 0

    total = 0
    for name in files:
        if not name.lower().endswith((".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".java", ".php", ".rb", ".sql")):
            continue
        path = Path(name)
        if not path.exists():
            continue
        findings = scan_file(path)
        if findings:
            print(f"\n== {name} ==")
            for lineno, pattern, note in findings:
                print(f"  L{lineno:<5} [{note}] ({pattern})")
                total += 1

    print(f"\n共标记 {total} 处,请逐条人工确认后再下结论。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
