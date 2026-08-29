"""周报素材收集脚本:从 git 历史收集指定时间段的提交,输出周报草稿的事实部分。

用法:
    python collect_worklog.py                            # 本周一至今,当前目录仓库
    python collect_worklog.py --since 2026-08-24 --until 2026-08-30
    python collect_worklog.py --repos <路径1> <路径2> -o 草稿.md

脚本只收集和分组事实(提交、作者、类型、文件数),不替人写结论。
琐碎提交(merge/typo/格式化)单独列出来,不混进正文。
"""

import argparse
import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

COMMIT_FMT = "%h|%an|%s"
TYPE_ORDER = ["feat", "fix", "refactor", "perf", "test", "docs", "build", "ci", "chore", "style", "其他"]
TRIVIAL_RE = re.compile(
    r"(merge|revert|typo|拼写|格式|format|格式化|cleanup|清理|\.gitignore|license|readme|changelog)",
    re.IGNORECASE,
)


def last_monday(today: date) -> date:
    return today - timedelta(days=today.weekday())


def run_git(repo: Path, args: list[str]) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError(f"git 命令失败({repo}):{result.stderr.strip()}")
    return result.stdout


def classify(subject: str) -> str:
    m = re.match(r"^([a-z]+)(\(.*\))?:", subject)
    if m and m.group(1) in TYPE_ORDER:
        return m.group(1)
    return "其他"


def collect_repo(repo: Path, since: str, until: str) -> dict:
    """返回 {commits: [(hash, author, subject)], files: int}"""
    log = run_git(repo, ["log", "--since", since, "--until", until, "--no-merges", f"--pretty=format:{COMMIT_FMT}"])
    commits = []
    for line in log.splitlines():
        parts = line.split("|", 2)
        if len(parts) == 3:
            commits.append((parts[0], parts[1], parts[2]))

    numstat = run_git(repo, ["log", "--since", since, "--until", until, "--no-merges", "--numstat", "--pretty=format:"])
    files = 0
    for line in numstat.splitlines():
        m = re.match(r"^\d+\t\d+\t(.+)$", line)
        if m:
            files += 1
    return {"commits": commits, "files": files}


def render_draft(repos: list[Path], since: str, until: str) -> str:
    lines = [f"# 周报草稿:{since} ~ {until}", ""]
    total_commits = 0
    total_files = 0
    sections: list[str] = []
    trivial: list[str] = []

    for repo in repos:
        data = collect_repo(repo, since, until)
        commits = data["commits"]
        total_commits += len(commits)
        total_files += data["files"]

        grouped: dict[str, list[tuple[str, str, str]]] = {}
        for commit in commits:
            kind = classify(commit[2])
            grouped.setdefault(kind, []).append(commit)

        sections.append(f"## {repo.resolve()}")
        sections.append("")
        if not commits:
            sections.append("- 本周无提交。")
            sections.append("")
            continue
        for kind in TYPE_ORDER:
            group = grouped.get(kind, [])
            if not group:
                continue
            non_trivial = []
            for h, author, subject in group:
                if TRIVIAL_RE.search(subject):
                    trivial.append(f"- {h} {subject}")
                    continue
                non_trivial.append((h, author, subject))
            if not non_trivial:
                continue
            sections.append(f"### {kind} ({len(non_trivial)})")
            for h, author, subject in non_trivial:
                sections.append(f"- [{h}] {subject}({author})")
            sections.append("")

    lines.append("## 数据概览")
    lines.append("")
    lines.append(f"- 时间段:{since} ~ {until},仓库数:{len(repos)}")
    lines.append(f"- 提交总数:{total_commits}(不含 merge),涉及文件:{total_files}")
    lines.append("")
    lines.append("## 本周完成")
    lines.append("")
    lines.extend(sections)
    lines.append("## 琐碎提交(建议不写进周报,可留底)")
    lines.append("")
    if trivial:
        lines.extend(trivial)
    else:
        lines.append("- 无。")
    lines.append("")
    lines.append("## 待补充(由 Agent 结合对话和代码状态填写)")
    lines.append("")
    lines.append("- 进行中事项;")
    lines.append("- 风险与阻塞;")
    lines.append("- 下一步计划。")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="周报素材收集")
    parser.add_argument("--since", default=None, help="起始日期 YYYY-MM-DD,默认本周一")
    parser.add_argument("--until", default=None, help="结束日期 YYYY-MM-DD,默认今天")
    parser.add_argument("--repos", nargs="+", default=None, help="仓库路径,默认当前目录")
    parser.add_argument("-o", "--out", default=None, help="输出文件,默认打印到终端")
    args = parser.parse_args()

    today = date.today()
    since = args.since or last_monday(today).isoformat()
    until = args.until or today.isoformat()
    repos = [Path(p) for p in (args.repos or ["."])]

    for repo in repos:
        if not (repo / ".git").exists() and not (repo / ".git").is_dir():
            print(f"不是 git 仓库:{repo}")
            return 1

    draft = render_draft(repos, since, until)
    if args.out:
        Path(args.out).write_text(draft, encoding="utf-8")
        print(f"草稿已写入:{args.out}")
    else:
        print(draft)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
