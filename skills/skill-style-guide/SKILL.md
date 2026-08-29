---
name: skill-style-guide
description: "技能风格审查。检查技能是否符合 cn-agent-skills 的风格约定:命名、frontmatter、正文结构、语言与质量红线,输出问题清单。Use to review and align skills with this library's style conventions."
license: MIT
metadata:
  version: "1.0.0"
---

# 技能风格指南(本仓库)

## 何时使用

- 创建新技能后检查是否符合仓库标准;
- 收到 PR,需要审查技能质量;
- 技能风格不统一,需要对齐。

## 使用步骤

先跑一遍检查脚本(见下面的[辅助脚本](#辅助脚本)),把机器能标记的项过掉,再按步骤人工核对。

### 第 1 步:检查命名与目录

- 目录名 = `name` = 技能名;
- `name` 小写、连字符、不以下划线或大写开头;
- 动词短语优先(`bug-diagnoser` ✓,`bug-fix-tool` 也可,`Diagnosis` ✗);
- 目录结构:`skills/<name>/SKILL.md` 必须存在。

### 第 2 步:检查 frontmatter

```yaml
name: <必填,与目录一致>
description: "<必填,1-1024 字符,做什么+何时触发>"
license: <推荐>
metadata:
  version: "1.0.0"
```

重点:

- description 是否覆盖中文触发表达;
- 是否包含触发条件关键词;
- 是否为空泛描述("帮助用户"这类)。

### 第 3 步:检查正文结构

推荐章节(可增减):

```markdown
## 何时使用
## 使用步骤
## 输入与输出
## 示例
## 注意事项
## 不适用场景
## 验证方式
```

检查:

- 步骤是否具体可执行(而不是"认真分析"这类空话);
- 是否每条规则配了示例;
- 是否包含"不适用场景",避免误触发;
- 是否包含"验证方式";
- 行数是否 ≤ 500。

### 第 4 步:检查语言与示例

- 正文中文为主,术语保留原文;
- 示例优先中文场景(中文提交信息、中文注释);
- 代码示例格式正确、可运行;
- description 中英双语或至少含英文关键词。

### 第 5 步:输出审查结论

```markdown
# 技能风格审查:<技能名>

## 结论
通过 / 修改后通过 / 不通过

## 问题清单
| 级别 | 位置 | 问题 | 建议 |
|------|------|------|------|
| 必须 | frontmatter | description 无触发词 | 补充"何时使用"描述 |
| 建议 | 正文 | 缺少不适用场景 | 补充,防止误触发 |

## 与仓库一致性
与 STYLE_GUIDE.md 约定:一致 / 不一致项(列出)
```

## 辅助脚本

[scripts/style_checker.py](scripts/style_checker.py) 能扫描技能目录,标记命名、frontmatter、章节、空泛表述、代码围栏等风格问题:

```bash
# 从仓库根目录检查全部技能
python skills/skill-style-guide/scripts/style_checker.py

# 只检查一个技能
python skills/skill-style-guide/scripts/style_checker.py api-tester
```

每条标记的判断标准见 [references/REVIEW_GUIDE.md](references/REVIEW_GUIDE.md)。脚本只做标记,结论需要人确认。
## 注意事项

- 风格审查 ≠ 内容审查:内容问题(逻辑错误、安全风险)也要一并指出;
- 不要为凑章节而加无内容章节;
- 判断标准以 [docs/STYLE_GUIDE.md](../../docs/STYLE_GUIDE.md)、[docs/CHECKLIST.md](../../docs/CHECKLIST.md) 和 [references/REVIEW_GUIDE.md](references/REVIEW_GUIDE.md) 为准。

## 不适用场景

- 审查非技能文件(代码、配置);
- 用户需要的是内容改写而非风格检查。

## 验证方式

1. 触发:"这个技能风格对吗";
2. 跑脚本:`python skills/skill-style-guide/scripts/style_checker.py <技能名>`,确认输出与人工结论一致;
3. 检查:输出包含结论 + 问题清单;
4. 抽查:任选一条意见,对照 STYLE_GUIDE 或 REVIEW_GUIDE 确认有依据。
