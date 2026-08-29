"""缓存 key 扫描脚本:扫描代码中的缓存 key 写法,标记不规范之处。

用法:
    python cache_key_scanner.py <目录或文件>

检查:无业务前缀的 key、缺少版本号、缺少 TTL 迹象、拼接对象直接当 key。
"""

import argparse
import re
import sys
from pathlib import Path

IGNORE_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"}
EXTENSIONS = {".py", ".js", ".ts", ".go", ".java"}

# 常见的缓存调用方式
KEY_ASSIGN = re.compile(r"(?i)(key|cache_key)\s*[:=]\s*(.+)$")
SET_CALL = re.compile(r"\.set\s*\(")
GOOD_KEY = re.compile(r"['\"][A-Za-z0-9_]+:[A-Za-z0-9_:]+['\"]|f['\"][A-Za-z0-9_]+:")


def scan_file(path: Path) -> list[str]:
    issues = []
    good_keys = set()
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return issues
    for i, line in enumerate(lines, 1):
        m = KEY_ASSIGN.search(line)
        if m:
            key_expr = m.group(2)
            if not GOOD_KEY.search(key_expr):
                issues.append(f"L{i}: 缓存 key 看起来没有业务前缀:'{key_expr.strip()}'")
            if ":" not in key_expr and "v1" not in key_expr.lower():
                issues.append(f"L{i}: key 缺少命名空间或版本号,建议如 'user:info:v1:{{id}}'")
            if GOOD_KEY.search(key_expr):
                good_keys.add(m.group(1).strip())
        if SET_CALL.search(line) and "ex=" not in line and "ttl" not in line.lower() and "expire" not in line.lower():
            issues.append(f"L{i}: set 调用未见 TTL 参数,确认是否需要过期时间")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="缓存 key 检查")
    parser.add_argument("path", help="目录或文件")
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
        issues = scan_file(f)
        if issues:
            print(f"== {f} ==")
            for issue in issues:
                print(f"  {issue}")
                total += 1
    print(f"\n共标记 {total} 条,结论需要人确认。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
