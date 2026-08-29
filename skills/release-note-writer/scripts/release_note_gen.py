"""发版说明草稿生成脚本:从 git 历史收集提交,按 Conventional Commits 分组。

用法:
    python release_note_gen.py                            # 上个 tag..HEAD
    python release_note_gen.py --since v0.8.0 --until main
    python release_note_gen.py --changelog --version v0.9.0   # CHANGELOG 条目
    python release_note_gen.py -o notes.md

脚本只收集和分组事实,标题、取舍、要不要写的结论由人定。
破坏性变更(BREAKING CHANGE 或 subject 带 !)单独列出,不混进普通变更。
"""

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

TYPE_ORDER = ["feat", "fix", "docs", "refactor", "perf", "test", "build", "ci", "chore", "style"]
TYPE_LABEL = {
    "feat": "新功能",
    "fix": "修复",
    "docs": "文档",
    "refactor": "重构",
    "perf": "性能",
    "test": "测试",
    "build": "构建",
    "ci": "CI",
    "chore": "杂项",
    "style": "样式",
}
COMMIT_RE = re.compile(r"^([a-zA-Z]+)(\([^)]+\))?(!)?:\s*(.+)$")


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


def last_tag(repo: Path) -> str | None:
    out = run_git(repo, ["describe", "--tags", "--abbrev=0"]).strip()
    return out or None


def parse_commits(repo: Path, since: str, until: str) -> list[dict]:
    out = run_git(
        repo,
        ["log", f"{since}..{until}", "--no-merges", "--pretty=format:%h|%s|%b%x00"],
    )
    commits = []
    for chunk in out.split("\x00"):
        chunk = chunk.strip()
        if not chunk:
            continue
        lines = chunk.splitlines()
        first = lines[0]
        parts = first.split("|", 2)
        if len(parts) < 2:
            continue
        short_hash = parts[0]
        subject = parts[1]
        body = "\n".join(lines[1:])
        commits.append({"hash": short_hash, "subject": subject, "body": body})
    return commits


def classify(subject: str, body: str) -> tuple[str | None, bool]:
    """返回 (类型, 是否破坏性变更)。"""
    m = COMMIT_RE.match(subject)
    breaking = bool(m and m.group(3)) or "BREAKING CHANGE" in body.upper()
    if m and m.group(1).lower() in TYPE_ORDER:
        return m.group(1).lower(), breaking
    return None, breaking


def render(commits: list[dict], since: str, until: str, version: str | None, changelog_mode: bool) -> str:
    grouped: dict[str, list[dict]] = {}
    unparsed: list[dict] = []
    breaking: list[dict] = []
    for commit in commits:
        kind, is_breaking = classify(commit["subject"], commit["body"])
        if is_breaking:
            breaking.append(commit)
        if kind:
            grouped.setdefault(kind, []).append(commit)
        else:
            unparsed.append(commit)

    if changelog_mode:
        version_text = version or "vX.Y.Z"
        lines = [f"## {version_text}({date.today().isoformat()})", ""]
        sections = []
        if breaking:
            sections.append(("破坏性变更", breaking))
        for kind in TYPE_ORDER:
            if kind in grouped:
                items = [c for c in grouped[kind] if c not in breaking]
                if items:
                    sections.append((TYPE_LABEL[kind], items))
        for label, items in sections:
            lines.append(f"### {label}")
            for commit in items:
                lines.append(f"- {commit['subject']}")
            lines.append("")
        if unparsed:
            lines.append("### 待确认")
            for commit in unparsed:
                lines.append(f"- {commit['hash']} {commit['subject']}")
            lines.append("")
        return "\n".join(lines).rstrip()

    lines = [f"# 发布说明草稿:{version or '下一版本'}", ""]
    lines.append(f"## 变更范围")
    lines.append("")
    lines.append(f"- 从 {since} 到 {until},共 {len(commits)} 个提交(不含 merge)。")
    lines.append("")
    if breaking:
        lines.append("## 破坏性变更")
        lines.append("")
        for commit in breaking:
            lines.append(f"- [{commit['hash']}] {commit['subject']}")
        lines.append("")
    for kind in TYPE_ORDER:
        if kind not in grouped:
            continue
        items = [commit for commit in grouped[kind] if commit not in breaking]
        if not items:
            continue
        lines.append(f"## {TYPE_LABEL[kind]}")
        lines.append("")
        for commit in items:
            lines.append(f"- [{commit['hash']}] {commit['subject']}")
        lines.append("")
    if unparsed:
        lines.append("## 待确认(无法按规范解析,人工判断归哪类)")
        lines.append("")
        for commit in unparsed:
            lines.append(f"- [{commit['hash']}] {commit['subject']}")
        lines.append("")
    return "\n".join(lines).rstrip()


def main() -> int:
    parser = argparse.ArgumentParser(description="发版说明草稿生成")
    parser.add_argument("--repo", default=None, help="仓库路径,默认当前目录")
    parser.add_argument("--since", default=None, help="起始 tag 或 commit,默认最近一个 tag")
    parser.add_argument("--until", default="HEAD", help="结束 commit,默认 HEAD")
    parser.add_argument("--version", default=None, help="版本号,用于标题")
    parser.add_argument("--changelog", action="store_true", help="输出 CHANGELOG 条目格式")
    parser.add_argument("-o", "--out", default=None, help="输出文件,默认打印到终端")
    args = parser.parse_args()

    repo = Path(args.repo) if args.repo else Path.cwd()
    if not (repo / ".git").exists() and not (repo / ".git").is_dir():
        print(f"不是 git 仓库:{repo}")
        return 1

    since = args.since or last_tag(repo)
    if not since:
        print("找不到起始 tag,请用 --since 指定(例如 v0.8.0 或某个 commit)。")
        return 1

    try:
        commits = parse_commits(repo, since, args.until)
    except RuntimeError as exc:
        print(exc)
        return 1

    draft = render(commits, since, args.until, args.version, args.changelog)
    if args.out:
        Path(args.out).write_text(draft, encoding="utf-8")
        print(f"草稿已写入:{args.out}")
    else:
        print(draft)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
