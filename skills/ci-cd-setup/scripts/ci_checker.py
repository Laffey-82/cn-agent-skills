"""CI 工作流配置检查脚本:扫描 GitHub Actions 配置,标记常见问题。

用法:
    python ci_checker.py <目录或文件>

检查项:密钥硬编码、action 未锁版本、缺少 checkout、弃用 Node 版本。
"""

import argparse
import re
import sys
from pathlib import Path

IGNORE_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__"}

SECRET_LIKE = re.compile(r"(?i)(password|token|api[_-]?key|secret)\s*[:=]\s*['\"][^'\"]+['\"]")
ACTION_USE = re.compile(r"uses:\s*([^@\s]+)(?:@([^\s#]+))?")
CHECKOUT = re.compile(r"uses:\s*actions/checkout")


def scan_file(path: Path) -> list[str]:
    issues = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return issues
    has_checkout = False
    for i, line in enumerate(lines, 1):
        if SECRET_LIKE.search(line):
            issues.append(f"L{i}: 疑似硬编码密钥,应改用 secrets 引用或环境变量")
        m = ACTION_USE.search(line)
        if m:
            name = m.group(1)
            version = m.group(2)
            if name.startswith("actions/"):
                if version is None:
                    issues.append(f"L{i}: action '{name}' 未锁版本,建议 '@v4' 或 commit SHA")
                elif re.match(r"^v?\d+$", version):
                    issues.append(f"L{i}: action '{name}@{version}' 是大版本 tag,建议锁小版本或 SHA")
            if name == "actions/checkout":
                has_checkout = True
        if re.search(r"node-version:\s*['\"]?(?:16|18|20)\b", line):
            issues.append(f"L{i}: Node 版本较旧,确认是否已弃用")
    if not has_checkout:
        issues.append("缺少 actions/checkout 步骤(大多数工作流需要先 checkout)")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="CI 配置检查")
    parser.add_argument("path", help="目录或文件")
    args = parser.parse_args()

    target = Path(args.path)
    if target.is_file():
        files = [target]
    else:
        files = [
            p
            for p in target.rglob("*")
            if p.is_file()
            and p.suffix.lower() in {".yml", ".yaml"}
            and not any(part in IGNORE_DIRS for part in p.parts)
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
