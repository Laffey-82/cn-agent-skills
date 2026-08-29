"""Git 历史统计脚本:按类型、作者统计提交,列出原子性可疑的提交。

用法:
    python git_stats.py [--count 50]

在当前 git 仓库内运行。
"""

import argparse
import re
import subprocess
from collections import Counter

TYPE_RE = re.compile(r"^(feat|fix|docs|style|refactor|perf|test|build|chore|ci|revert)(\(.+\))?:")


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    return result.stdout


def main() -> int:
    parser = argparse.ArgumentParser(description="Git 历史统计")
    parser.add_argument("--count", type=int, default=50, help="分析的提交数,默认 50")
    args = parser.parse_args()

    log = git("log", f"-{args.count}", "--pretty=%h|%an|%s")
    commits = [line.split("|", 2) for line in log.splitlines() if "|" in line]
    if not commits:
        print("没有提交记录。")
        return 1

    by_type: Counter[str] = Counter()
    by_author: Counter[str] = Counter()
    suspicious = []

    for hash_, author, subject in commits:
        m = TYPE_RE.match(subject)
        if m:
            by_type[m.group(1)] += 1
        else:
            by_type["(不规范)"] += 1
            suspicious.append((hash_, author, subject, "提交信息缺少类型前缀"))
        by_author[author] += 1
        if len(subject) > 72:
            suspicious.append((hash_, author, subject, "提交信息超 72 字"))

    print(f"== 最近 {len(commits)} 条提交 ==")
    print("按类型:")
    for kind, count in by_type.most_common():
        print(f"  {kind:<10} {count}")
    print("按作者:")
    for author, count in by_author.most_common():
        print(f"  {author:<20} {count}")

    if suspicious:
        print("\n需确认的提交:")
        seen = set()
        for hash_, author, subject, note in suspicious:
            key = (hash_, note)
            if key in seen:
                continue
            seen.add(key)
            print(f"  {hash_} [{note}] {subject}")
    else:
        print("\n未发现格式问题。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
