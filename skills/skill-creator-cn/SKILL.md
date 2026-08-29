---
name: skill-creator-cn
description: 创建新技能。引导用户从需求出发创建符合 Agent Skills 开放标准的中文技能,覆盖结构设计、SKILL.md 编写、references 拆分、校验与测试。Use to create a new, spec-compliant skill for this library.
license: MIT
metadata:
  version: "1.0.0"
---

# 技能创建器(中文)

## 何时使用

- 用户说"帮我做一个技能""我想把某个流程做成技能";
- 需要把重复性工作固化为可复用技能;
- 新技能需要符合本仓库标准(见 [skill-style-guide](../skill-style-guide/SKILL.md))。

## 使用步骤

### 第 1 步:明确技能目标

一次对话问清:

1. 这个技能解决什么问题(场景);
2. 什么时候触发(触发词、触发条件);
3. 输入是什么、产出是什么;
4. 谁会用(目标用户);
5. 已有类似技能吗(避免重复)。

### 第 2 步:规划结构

```text
skills/<skill-name>/
├── SKILL.md          # 必需
├── references/       # 可选:详细参考
├── scripts/          # 可选:可执行脚本
└── assets/           # 可选:模板与资源
```

规则:

- SKILL.md ≤ 500 行,复杂内容拆到 references/;
- 技能名用动词短语、小写连字符;
- 只保留必要文件,不塞无关内容。

### 第 3 步:编写 SKILL.md

```yaml
---
name: <skill-name>
description: <做什么 + 何时触发,中英双语>
license: MIT
metadata:
  version: "1.0.0"
---
```

正文统一结构(可增减):

```markdown
## 何时使用
## 使用步骤
## 输入与输出
## 示例
## 注意事项
## 不适用场景
## 验证方式
```

### 第 4 步:补充资源

- 需要确定性执行的操作(如文件解析、数据转换)写成 `scripts/` 脚本,并说明运行环境;
- 需要详细背景或表单模板的放 `references/`,从 SKILL.md 用相对路径引用。

### 第 5 步:校验

```bash
# 官方校验工具
skills-ref validate ./skills/<skill-name>

# 或本地快速检查 frontmatter 与命名
```

检查:

- name 与目录名一致;
- frontmatter 合法;
- description 触发词清晰;
- 引用文件路径正确。

### 第 6 步:实测触发

在至少一种 Agent 环境中,用真实任务测试:

1. 用触发词是否被识别;
2. 执行步骤是否顺畅;
3. 产出是否符合预期。

测试通过后,更新 README 技能索引并提交。

## 输入与输出

- 输入:一个想自动化的流程/任务描述;
- 输出:通过校验与实测的技能目录。

## 示例

**用户:** "我想做一个技能,帮我自动生成周报。"

**对话收敛:**

- 场景:每周五生成周报;
- 触发:"帮我写周报";
- 输入:本周 git 提交记录 + 工作事项;
- 产出:Markdown 周报(本周完成/下周计划/风险);
- 结构:`skills/weekly-report/SKILL.md` + `scripts/collect_git_log.sh`。

## 注意事项

- **先收敛需求再动手**,避免做出来不是用户要的;
- 技能要"窄而深":一个技能只解决一个问题,不要做万能技能;
- description 是触发核心,写完后用"用户会怎么说"反向检查;
- 内容必须原创。

## 不适用场景

- 一次性任务(不需要固化);
- 用户要求批量生成一堆技能(一次聚焦一个);
- 技能涉及敏感操作且无法安全约束(如直接删除生产数据)。

## 验证方式

1. 触发:"帮我做一个技能";
2. 检查:输出目录通过 `skills-ref validate`;
3. 实测:在 Agent 中触发并跑通一次真实任务。
