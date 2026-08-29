---
name: skill-creator-cn
description: 创建新技能。当用户想新建一个 Agent 技能、把重复流程固化成技能,或要求符合本仓库标准时,从需求出发引导完成结构设计、SKILL.md 编写、references 拆分、校验与测试。Use to create a new, spec-compliant skill for this library.
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

先用脚本生成骨架(见下面的[辅助脚本](#辅助脚本)),再按章节填充。

质量标准(按重要程度排序):

1. **假设 Agent 已有能力**:只写能改变决策的信息,不写通用建议、重复要求和"要认真仔细"这类空话;
2. **description 有判别性**:说清"做什么 + 什么时候用",能挡住不该触发的请求;
3. **渐进式披露**:正文只留主干流程,细节、模板、长例子放 references,按需读取;
4. **示例必须有信息量**:示例要能澄清任务,不是为了凑章节;
5. **正文越短越好**:500 行是上限,不是目标。

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

### 第 5 步:自检与评审

先跑机器检查:

```bash
# 风格检查(只做标记,结论人工确认)
python skills/skill-style-guide/scripts/style_checker.py <skill-name>

# 官方校验
skills-ref validate ./skills/<skill-name>

# 脚本语法
python -m py_compile skills/<skill-name>/scripts/*.py
```

检查:

- name 与目录名一致;
- frontmatter 合法;
- description 触发词清晰;
- 引用文件路径正确。

然后按 [references/REVIEW_PROCESS.md](references/REVIEW_PROCESS.md) 的"人工评审重点"逐条过:内容原创、示例可运行、验证方式写清。

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

## 辅助脚本

[scripts/skill_scaffold.py](scripts/skill_scaffold.py) 生成符合仓库标准的 SKILL.md 骨架,并校验技能名和描述:

```bash
# 在仓库根目录执行
python skills/skill-creator-cn/scripts/skill_scaffold.py weekly-report --description "根据本周提交和工作事项生成周报,周五触发"
```

生成的是起点,章节按实际情况填充或删除,不覆盖已存在的目录。完整流程见 [references/REVIEW_PROCESS.md](references/REVIEW_PROCESS.md)。

## 注意事项

- **先收敛需求再动手**,避免做出来不是用户要的;
- 技能要"窄而深":一个技能只解决一个问题,不要做万能技能;
- description 是触发核心,写完后用"用户会怎么说"反向检查;
- 内容必须原创。
- 新技能从想法到合并按 [references/REVIEW_PROCESS.md](references/REVIEW_PROCESS.md) 走,不带病入库。

## 不适用场景

- 一次性任务(不需要固化);
- 用户要求批量生成一堆技能(一次聚焦一个);
- 技能涉及敏感操作且无法安全约束(如直接删除生产数据)。

## 验证方式

1. 触发:"帮我做一个技能";
2. 用 skill_scaffold.py 生成骨架,目录通过 `skills-ref validate`;
3. 检查:style_checker.py 无"必须"级问题;
4. 实测:在 Agent 中触发并跑通一次真实任务。

