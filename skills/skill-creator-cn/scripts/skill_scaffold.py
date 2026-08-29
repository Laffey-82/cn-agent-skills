"""新技能骨架生成脚本:校验名字和描述,生成符合仓库标准的 SKILL.md 骨架。

用法:
    python skill_scaffold.py weekly-report --description "根据本周提交和工作事项生成周报,周五下班前触发"

生成结果只做起点,章节要按实际情况填充或删除,填充完再跑:
    python skills/skill-style-guide/scripts/style_checker.py weekly-report
    skills-ref validate ./skills/weekly-report

脚本不自动写内容,也不覆盖已存在的技能目录。
"""

import argparse
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z][a-z0-9-]{0,63}$")
GENERIC_RE = re.compile(r"(帮助(用户|开发者|你)|提供(专业|全面|优质|高效)的?(帮助|支持|服务))")
SKILL_MD_TEMPLATE = """---
name: {name}
description: "{description}"
license: MIT
metadata:
  version: "1.0.0"
---

# {title}

<!-- 骨架由 skill_scaffold.py 生成。按章节填充,不需要的章节删掉,完成后删除本注释。 -->

## 何时使用

- 补触发场景:什么情况下用户会用到这个技能。

## 使用步骤

### 第 1 步:补步骤名

- 写出具体可执行的操作,规则配中文例子;
- 步骤多时继续拆"第 2 步""第 3 步",细节多的内容放到 references/。

## 输入与输出

- 输入:说明触发时用户要提供什么。
- 输出:说明技能交付什么。

## 示例

- 补一个真实场景,展示从触发到产出的完整过程。

## 注意事项

- 补容易踩的坑;没有就不写。

## 不适用场景

- 补明确不该用本技能的情形,防止误触发。

## 验证方式

1. 触发:补触发词;
2. 检查:补预期产出;
3. 实测:在 Agent 里跑通一次真实任务。
"""


def yaml_quote(text: str) -> str:
    """description 需要安全放进 YAML 双引号字符串。"""
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return escaped


def main() -> int:
    parser = argparse.ArgumentParser(description="新技能骨架生成")
    parser.add_argument("name", help="技能名,小写连字符,如 api-contract-tester")
    parser.add_argument("--description", required=True, help="技能描述(做什么 + 何时触发),1-1024 字符")
    parser.add_argument("--out", default=None, help="输出目录,默认当前目录下的 skills/(存在时)")
    args = parser.parse_args()

    name = args.name
    desc = args.description.strip()

    if not NAME_RE.match(name):
        print(f"技能名 '{name}' 不合法:应小写字母开头,只含小写字母、数字、连字符,最长 64 字符。")
        return 1
    if not (1 <= len(desc) <= 1024):
        print(f"description 长度 {len(desc)},应在 1-1024 之间。")
        return 1
    if len(desc) < 20:
        print(f"提示:description 只有 {len(desc)} 字符,建议写清场景和触发条件。")
    if GENERIC_RE.search(desc):
        print("提示:description 疑似空泛描述,建议换成具体场景,例如'当需求模糊、缺少验收标准时'。")

    if args.out:
        out_root = Path(args.out)
    else:
        cwd = Path.cwd()
        out_root = cwd / "skills" if (cwd / "skills").is_dir() else cwd
    target = out_root / name
    if target.exists():
        print(f"目标目录已存在,不覆盖:{target}")
        return 1
    target.mkdir(parents=True, exist_ok=False)

    title = name.replace("-", " ")
    title = " ".join(part.capitalize() for part in title.split())
    content = SKILL_MD_TEMPLATE.format(
        name=name,
        description=yaml_quote(desc),
        title=title,
    )
    (target / "SKILL.md").write_text(content, encoding="utf-8")

    print(f"已生成:{target / 'SKILL.md'}")
    print("接下来:")
    print(f"  1. 按章节填充 {name}/SKILL.md,不需要的章节删掉;")
    print("  2. python skills/skill-style-guide/scripts/style_checker.py <name>")
    print("  3. skills-ref validate ./skills/<name>")
    print("  4. 在 Agent 里用真实任务实测一次,再更新 README 技能索引。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
