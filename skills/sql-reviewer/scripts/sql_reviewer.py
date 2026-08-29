"""SQL 静态检查脚本:按常见反模式标记 SQL 文件中的可疑点。

用法:
    python sql_reviewer.py <文件或目录>
    python sql_reviewer.py a.sql b.sql

检查项:
- 高危:UPDATE/DELETE 缺 WHERE、DROP/TRUNCATE;
- 性能:SELECT *、前导通配 LIKE、列上套函数、隐式连接、NOT IN 子查询、
  INSERT...SELECT 缺列名、SELECT 缺 LIMIT。

脚本只做标记,结论需要人确认。涉及索引和性能的结论,先看执行计划再下。
"""

import argparse
import re
import sys
from pathlib import Path

FUNC_ON_COLUMN_RE = re.compile(
    r"\b(lower|upper|year|month|day|date|substr|substring|trim|ltrim|rtrim|length|abs|round|cast|convert)\s*\(\s*[a-z_][a-z0-9_.]*\s*\)",
    re.IGNORECASE,
)
LEADING_WILDCARD_RE = re.compile(r"like\s*'%", re.IGNORECASE)
SELECT_STAR_RE = re.compile(r"\bselect\s+\*", re.IGNORECASE)
NOT_IN_RE = re.compile(r"\bnot\s+in\s*\(", re.IGNORECASE)
IMPLICIT_JOIN_RE = re.compile(r"\bfrom\s+\S+\s*,\s*\S+", re.IGNORECASE)
INSERT_SELECT_NO_COLS_RE = re.compile(r"\binsert\s+into\s+\S+\s+select\b", re.IGNORECASE)
UPDATE_NO_WHERE_RE = re.compile(r"^\s*update\b", re.IGNORECASE | re.MULTILINE)
DELETE_NO_WHERE_RE = re.compile(r"^\s*delete\b", re.IGNORECASE | re.MULTILINE)
DROP_TRUNCATE_RE = re.compile(r"^\s*(drop|truncate)\b", re.IGNORECASE | re.MULTILINE)
WHERE_RE = re.compile(r"\bwhere\b", re.IGNORECASE)
LIMIT_RE = re.compile(r"\blimit\b", re.IGNORECASE)
COMMENT_RE = re.compile(r"/\*.*?\*/|--[^\n]*", re.DOTALL)


def strip_comments(text: str) -> str:
    return COMMENT_RE.sub(" ", text)


def analyze_statement(stmt: str, start_line: int, findings: list[tuple[int, str, str]]) -> None:
    lowered_start = stmt.lstrip().lower()
    has_where = bool(WHERE_RE.search(stmt))

    if UPDATE_NO_WHERE_RE.search(stmt) and not has_where:
        findings.append((start_line, "必须", "UPDATE 没有 WHERE,会全表更新"))
    if DELETE_NO_WHERE_RE.search(stmt) and not has_where:
        findings.append((start_line, "必须", "DELETE 没有 WHERE,会清空数据"))
    if DROP_TRUNCATE_RE.search(stmt):
        findings.append((start_line, "必须", "DROP/TRUNCATE 高危操作,确认影响范围后再执行"))

    if SELECT_STAR_RE.search(stmt):
        findings.append((start_line, "建议", "SELECT *,建议显式列出字段"))
    if LEADING_WILDCARD_RE.search(stmt):
        findings.append((start_line, "建议", "LIKE 前导通配符(以 % 开头),索引会失效"))
    if FUNC_ON_COLUMN_RE.search(stmt):
        findings.append((start_line, "建议", "WHERE 条件对列套了函数,索引可能失效,核对执行计划"))
    if NOT_IN_RE.search(stmt):
        findings.append((start_line, "建议", "NOT IN 子查询遇到 NULL 会返回空结果,核对语义"))
    if IMPLICIT_JOIN_RE.search(stmt):
        findings.append((start_line, "建议", "FROM 后用逗号隐式连接,建议显式 JOIN + ON"))
    if INSERT_SELECT_NO_COLS_RE.search(stmt):
        findings.append((start_line, "建议", "INSERT...SELECT 没有显式列名,表结构变化时容易错位"))
    if lowered_start.startswith("select") and not LIMIT_RE.search(stmt):
        findings.append((start_line, "建议", "SELECT 没有 LIMIT,核对是否会返回过大结果集"))


def check_file(path: Path) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        findings.append((0, "必须", f"无法读取文件:{path}"))
        return findings

    text = strip_comments(text)
    pos = 0
    for chunk in text.split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        start = text.find(chunk, pos)
        start_line = text.count("\n", 0, start) + 1
        pos = start + len(chunk)
        analyze_statement(chunk, start_line, findings)
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="SQL 静态检查")
    parser.add_argument("paths", nargs="+", help="SQL 文件或目录")
    parser.add_argument("--strict", action="store_true", help="存在'必须'级问题时以非零码退出(用于 CI)")
    args = parser.parse_args()

    files: list[Path] = []
    for item in args.paths:
        path = Path(item)
        if path.is_dir():
            files.extend(sorted(p for p in path.rglob("*.sql") if p.is_file()))
        elif path.is_file():
            files.append(path)

    if not files:
        print("没有找到 .sql 文件。")
        return 0

    total = 0
    total_must = 0
    for path in files:
        findings = check_file(path)
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

    print(f"\n共检查 {len(files)} 个文件,标记 {total} 项。涉及索引和性能的,先看执行计划再下结论。")
    if args.strict and total_must > 0:
        print("strict 模式:存在'必须'级问题,退出码 1。")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
