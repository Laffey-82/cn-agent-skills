"""代码迁移检查清单生成器:生成迁移前的现状评估和分批计划模板。

用法:
    python migration_checklist.py <迁移目标>

示例:
    python migration_checklist.py "Python 2 迁到 Python 3"
"""

import argparse
import datetime
import subprocess
import sys
from pathlib import Path


def git_files() -> list[str]:
    try:
        result = subprocess.run(
            ["git", "ls-files"], capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        return [line for line in result.stdout.splitlines() if line.strip()]
    except FileNotFoundError:
        return []


def count_by_ext(files: list[str]) -> list[tuple[str, int]]:
    from collections import Counter

    counter: Counter[str] = Counter()
    for f in files:
        suffix = Path(f).suffix.lower()
        if suffix:
            counter[suffix] += 1
    return counter.most_common(10)


def main() -> int:
    parser = argparse.ArgumentParser(description="迁移检查清单生成")
    parser.add_argument("target", help="迁移目标,如 'Python 2 迁到 Python 3'")
    args = parser.parse_args()

    files = git_files()
    out = []
    out.append(f"# 迁移检查清单:{args.target}")
    out.append("")
    out.append("## 1. 现状评估")
    out.append("")
    if files:
        out.append(f"- 版本管理文件数:{len(files)}")
        out.append("- 文件类型分布:")
        for ext, count in count_by_ext(files):
            out.append(f"  - {ext}:{count}")
    else:
        out.append("- (未检测到 git 仓库,建议先 git init)")
    out.append("- 测试覆盖:待确认")
    out.append("- 高风险区域:待确认")
    out.append("- 已知行为怪癖:待确认")
    out.append("")
    out.append("## 2. 迁移策略")
    out.append("")
    out.append("- [ ] 绞杀者模式(大系统,逐步替换)")
    out.append("- [ ] 抽象分支(换底层,接口不动)")
    out.append("- [ ] 并行运行(新旧对比)")
    out.append("- [ ] 试点先行(先走通一个模块)")
    out.append("")
    out.append("## 3. 分批计划")
    out.append("")
    out.append("| 批次 | 范围 | 测试 | 行为对照 | 上线/回滚 |")
    out.append("|---|---|---|---|---|")
    out.append("| 1 |  |  |  |  |")
    out.append("")
    out.append("## 4. 每批验证")
    out.append("")
    out.append("- [ ] 迁移前测试全绿")
    out.append("- [ ] 迁移后测试全绿")
    out.append("- [ ] 行为对照清单逐项确认")
    out.append("- [ ] 可独立上线")
    out.append("- [ ] 回滚方案明确")
    out.append("")
    out.append("## 5. 输出")
    out.append("- 行为差异清单")
    out.append("- 遗留风险")
    out.append("")

    ts = datetime.datetime.now().strftime("%Y%m%d")
    filename = f"migration_checklist_{ts}.md"
    Path(filename).write_text("\n".join(out), encoding="utf-8")
    print(f"已生成 {filename}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
