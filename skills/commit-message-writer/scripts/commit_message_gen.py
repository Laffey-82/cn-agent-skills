"""提交信息生成辅助脚本:根据暂存区改动生成 Conventional Commits 格式的提交信息草稿。

用法:
    python commit_message_gen.py

在 git 仓库内运行,读取暂存区改动。只生成草稿,不执行 commit。
"""

import subprocess
import sys


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    return result.stdout


def infer_type(changes: str) -> str:
    if any(line.startswith("M ") and line.endswith((".md", ".rst", ".txt")) for line in changes.splitlines()):
        return "docs"
    if any(line.startswith("A ") for line in changes.splitlines()):
        return "feat"
    if any(line.startswith("D ") for line in changes.splitlines()):
        return "feat"
    return "chore"


def infer_scope(files: list[str]) -> str:
    if not files:
        return ""
    first = files[0]
    parts = first.split("/")
    if len(parts) > 1:
        return parts[0]
    return first.split(".")[0] if "." in first else first


def main() -> int:
    status = git("status", "--short")
    if not status.strip():
        print("暂存区没有改动。先 git add 再运行。")
        return 1

    files = [line[3:] for line in status.splitlines() if line.strip()]
    staged = [f for f in files if f[:1] in {"A", "M", "D", "R", "C"}]
    if not staged:
        print("没有已暂存的改动(git add 之后再来)。")
        return 1

    commit_type = infer_type(status)
    scope = infer_scope(staged)
    scope_part = f"({scope})" if scope else ""
    subject_hint = "在此处写一句话说明"

    print("== 提交信息草稿 ==")
    print(f"{commit_type}{scope_part}: {subject_hint}")
    print()
    print("== 改动文件 ==")
    for f in staged:
        print(f"  {f}")
    print()
    print("提示:根据实际改动把 subject 写具体;新增功能用 feat,修 Bug 用 fix。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
