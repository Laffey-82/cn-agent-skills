"""安全扫描辅助脚本:扫描指定目录下的代码,标记常见安全问题位置。

用法:
    python security_scanner.py <路径>

只做标记,结论需要人确认。
"""

import argparse
import re
import sys
from pathlib import Path

IGNORE_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", ".next"}
EXTENSIONS = {".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".java", ".php", ".rb", ".sql"}

PATTERNS = [
    (re.compile(r"(?i)(password|passwd|secret|token|api[_-]?key)\s*[:=]\s*['\"][A-Za-z0-9_\-]{8,}['\"]"), "疑似硬编码密钥"),
    (re.compile(r"SELECT\s+.+\s+FROM\s+.+\s*(\+|%|f['\"])"), "疑似字符串拼接 SQL"),
    (re.compile(r"eval\s*\(|exec\s*\(|os\.system\s*\(|subprocess\.(run|call|Popen)\s*\([^)]*shell\s*=\s*True"), "动态执行/命令注入风险"),
    (re.compile(r"innerHTML\s*=|v-html\s*=|dangerouslySetInnerHTML"), "直接渲染 HTML,确认是否含用户输入"),
    (re.compile(r"open\s*\([^)]*(\.\./|/etc/|/var/)"), "路径拼接疑似可穿越"),
    (re.compile(r"except\s*:\s*(pass|continue)?\s*$"), "裸 except 吞异常"),
    (re.compile(r"debug\s*=\s*True|DEBUG\s*=\s*True"), "调试模式残留"),
    (re.compile(r"csrf\s*=\s*False|csrf_exempt|@csrf_protect.*|x-frame-options"), "CSRF/安全头配置需确认"),
]


def scan_file(path: Path) -> list[tuple[int, str]]:
    findings = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return findings
    for i, line in enumerate(text.splitlines(), 1):
        for pattern, note in PATTERNS:
            if pattern.search(line):
                findings.append((i, note))
                break
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="安全扫描辅助")
    parser.add_argument("path", help="要扫描的目录或文件")
    args = parser.parse_args()

    target = Path(args.path)
    if target.is_file():
        files = [target]
    else:
        files = [
            p
            for p in target.rglob("*")
            if p.is_file() and p.suffix.lower() in EXTENSIONS and not any(part in IGNORE_DIRS for part in p.parts)
        ]

    total = 0
    for f in files:
        findings = scan_file(f)
        if findings:
            print(f"== {f} ==")
            for lineno, note in findings:
                print(f"  L{lineno:<5} [{note}]")
                total += 1

    print(f"\n共标记 {total} 处,请逐条人工确认后再下结论。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
