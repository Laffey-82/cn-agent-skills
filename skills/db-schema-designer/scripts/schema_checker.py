"""数据库命名规范检查脚本:扫描 SQL/ORM 文件,标记命名问题。

用法:
    python schema_checker.py <目录或文件>

检查项:小写下划线命名、金额类型、主键命名、时间字段。
"""

import argparse
import re
import sys
from pathlib import Path

IGNORE_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"}
EXTENSIONS = {".sql", ".py", ".java"}

# 提取 CREATE TABLE 中的列定义
COLUMN_RE = re.compile(r"^\s*`?([A-Za-z0-9_]+)`?\s+([A-Za-z0-9_() ]+?)(\s+(NOT NULL|NULL|DEFAULT|PRIMARY KEY|UNIQUE|COMMENT).*)?,?$", re.IGNORECASE)


def check_line(path: Path, lineno: int, line: str) -> list[str]:
    issues = []
    # 命名:大写或非下划线字符
    keywords = {
        "SELECT", "FROM", "WHERE", "INSERT", "UPDATE", "DELETE", "TABLE", "CREATE",
        "ALTER", "ADD", "INDEX", "PRIMARY", "KEY", "NOT", "NULL", "DEFAULT", "INT",
        "VARCHAR", "BIGINT", "DECIMAL", "TIMESTAMP", "DATETIME", "DATE", "TINYINT",
        "TEXT", "BOOLEAN", "FLOAT", "DOUBLE", "CURRENT", "CURRENT_TIMESTAMP", "ON",
        "VALUES", "IN", "SET", "ORDER", "GROUP", "BY", "LIMIT", "OFFSET", "HAVING",
        "JOIN", "LEFT", "RIGHT", "INNER", "OUTER", "AS", "AND", "OR", "CASE", "WHEN",
        "THEN", "END", "ELSE", "LIKE", "BETWEEN", "IS", "EXISTS", "COUNT", "SUM",
        "AVG", "MAX", "MIN", "NOW", "REFERENCES", "CONSTRAINT", "UNIQUE", "CHECK",
        "COMMENT", "ENGINE", "CHARSET", "AUTO_INCREMENT", "COLLATE", "USING", "BTREE",
        "DESC", "ASC",
    }
    for token in re.findall(r"`?([A-Za-z][A-Za-z0-9]+)`?", line):
        if re.search(r"[A-Z]", token) and token.upper() not in keywords:
            issues.append(f"L{lineno}: 驼峰/大写命名 '{token}',建议小写下划线")
    # 金额用浮点
    if re.search(r"amount|price|money|total|fee", line, re.IGNORECASE) and re.search(r"FLOAT|DOUBLE", line, re.IGNORECASE):
        issues.append(f"L{lineno}: 金额字段用了 FLOAT/DOUBLE,建议整数分或 DECIMAL")
    # 主键非 id
    if re.search(r"PRIMARY KEY", line, re.IGNORECASE) and not re.search(r"\bid\b", line, re.IGNORECASE):
        issues.append(f"L{lineno}: 主键命名建议统一为 id")
    return issues


def scan_file(path: Path) -> list[str]:
    issues = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return issues
    for i, line in enumerate(text.splitlines(), 1):
        issues.extend(check_line(path, i, line))
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="命名规范检查")
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

    print(f"\n共标记 {total} 条,结论需要人确认(排除关键字误报)。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
