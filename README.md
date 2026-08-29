# cn-agent-skills · 中文 Agent 技能库

给 Claude Code、Codex、Cursor、TRAE、OpenCode 用的中文技能集。每个技能解决一个具体问题,按"需求 → 方案 → 开发 → 验证 → 发布"整条线组织,装上就能用,单独用也行。

[English](./README.en.md) · [技能索引](#技能索引) · [安装](#安装) · [贡献](./CONTRIBUTING.md)

![stars](https://img.shields.io/github/stars/Laffey-82/cn-agent-skills?style=flat-square)
![license](https://img.shields.io/github/license/Laffey-82/cn-agent-skills?style=flat-square)
![skills](https://img.shields.io/badge/skills-29-green?style=flat-square)
![ci](https://img.shields.io/github/actions/workflow/status/Laffey-82/cn-agent-skills/validate-skills.yml?style=flat-square)

## 这是什么

一个面向中文团队的 Agent 技能仓库:

- **说中文就能触发**:触发词就是日常说法,"帮我把这个需求理清楚""这个报错怎么排查",不用记英文命令;
- **一条线贯穿开发全流程**:从需求澄清、方案设计、任务拆解,到编码、测试、审查,再到文档、周报、发版,每个环节有对应技能,产出能衔接;
- **质量有保证**:29 个技能全部原创,逐个过官方校验;CI 四道闸(格式、语法、风格、文档)自动检查;带脚本的技能都实测过,脚本只做标记或测量,结论由人确认。

## 技能索引

按开发阶段分组,哪个场景需要就触发哪个。

### 开发前置:想清楚再动手

| 技能 | 干什么 | 触发示例 |
|---|---|---|
| requirement-clarifier | 需求模糊时多轮提问理清楚,输出需求规格 | "帮我把这个需求理清楚" |
| requirements-reviewer | 评审需求文档/PRD,输出缺口清单 | "评审一下这个需求" |
| tech-design-writer | 产出技术方案:方案对比与选型、架构、数据、风险与上线 | "写个技术方案" |
| api-contract-designer | 实现前定义 API 契约:方法、路径、参数、响应与错误码 | "设计接口契约" |
| task-decomposer | 把大任务拆成带验收标准的小任务,排出依赖顺序 | "把这个功能拆成任务" |

### 实现与质量:写对、写好

| 技能 | 干什么 | 触发示例 |
|---|---|---|
| tdd-workflow | 红灯-绿灯-重构循环,先写测试再实现 | "按 TDD 来做" |
| code-reviewer | 从正确性、安全、性能、可维护性四维审查代码 | "帮我 review 这段代码" |
| security-reviewer | 按 OWASP 思路查注入、越权、数据泄露等风险 | "帮我看下安不安全" |
| api-tester | 按真实契约生成 API 测试,确认环境后执行并出报告 | "给这个接口写测试" |
| sql-reviewer | 扫描 SQL 反模式:高危操作缺 WHERE、SELECT *、前导通配 LIKE 等 | "审一下这条 SQL" |
| db-schema-designer | 从需求出发设计表、字段、关系和索引 | "帮我设计数据模型" |
| db-migration-reviewer | 审查迁移脚本的安全性、可回滚性和锁表风险 | "帮我看下这个迁移安不安全" |
| cache-governor | 设计 key 与 TTL,防御穿透、击穿、雪崩 | "加个缓存" |
| ci-cd-setup | 根据项目现状搭 CI/CD,先生成配置再跑通 | "帮我搭个 CI" |
| code-migrator | 分批迁移老项目,每批有测试兜底和回滚 | "把项目迁到 X" |

### 排障与性能:出问题能定位

| 技能 | 干什么 | 触发示例 |
|---|---|---|
| bug-diagnoser | 先复现、再取证、二分定位根因,修复后补回归测试 | "这个报错怎么排查" |
| dev-env-troubleshooter | 服务起不来、端口被占、连不上数据库时按阶梯逐层排查 | "本地起不来" |
| log-analysis | 按时间线重建故障过程,用请求 ID 关联日志定位根因 | "帮我查下日志" |
| frontend-debug | 白屏、报错、请求失败时,按 Console → Network 逐层排查 | "页面白屏了" |
| performance-profiler | 先建基线再用 profiler 取证,定位性能瓶颈 | "这个接口好慢" |

### 工程规范:提交与历史

| 技能 | 干什么 | 触发示例 |
|---|---|---|
| commit-message-writer | 按 Conventional Commits 生成提交信息,支持中文 | "写个 commit message" |
| git-workflow | 整理提交历史,原子提交,干净分支 | "帮我把提交整理干净" |

### 文档与沟通:人看得懂

| 技能 | 干什么 | 触发示例 |
|---|---|---|
| tech-doc-writer | 先读代码再写文档,示例全部实测过 | "给这个项目写 README" |
| natural-chinese-writer | 把僵硬套话改成自然表达,保留原意 | "这段文字看着别扭,改一下" |
| weekly-report | 收集本周 git 提交,整理成"完成/进行中/风险/下一步"结构的中文周报 | "帮我写周报" |
| meeting-minutes | 把会议讨论整理成含结论与待办的中文纪要,待办有负责人和截止时间 | "记会议纪要" |
| release-note-writer | 从 git 历史生成发版说明或 CHANGELOG 条目,破坏性变更单独列出 | "写 release notes" |

### 元技能:造技能的技能

| 技能 | 干什么 | 触发示例 |
|---|---|---|
| skill-creator-cn | 从需求出发创建符合规范的新技能 | "帮我做一个技能" |
| skill-style-guide | 检查技能是否符合仓库风格 | "这个技能风格对吗" |

## 典型使用流程

技能按一条线串起来用,拿"做一个带登录的商品列表页"举例:

```text
1.  "帮我把这个需求理清楚"      → requirement-clarifier 输出需求规格
2.  "评审一下这个需求"          → requirements-reviewer 补缺口
3.  "写个技术方案"              → tech-design-writer 定方案
4.  "设计接口契约"              → api-contract-designer 出契约
5.  "把这个功能拆成任务"        → task-decomposer 拆任务清单
6.  "按 TDD 实现登录接口"       → tdd-workflow 先写测试再实现
7.  "给这个接口写测试"          → api-tester 按契约跑用例
8.  "提交前 review 一下"        → code-reviewer 四维审查
9.  "写个 commit message"       → commit-message-writer 规范提交
10. "帮我搭个 CI"               → ci-cd-setup 自动化构建测试
11. "这个接口好慢"              → performance-profiler 定位瓶颈
12. "发个版,写 release notes"   → release-note-writer 生成发版说明
```

每步的产出是下一步的输入,和平时开发节奏一致。完整流程适合从零开始的新功能;单独用也可以,哪个场景需要就触发哪个。

## 技能结构

技能按深度分三层,按需加载:

- **文档 + 参考资料**:如 requirement-clarifier 的提问模板、api-tester 的用例设计参考;
- **可执行脚本**:如 code-reviewer 的扫描脚本、performance-profiler 的基准脚本;
- **完整示例**:如 tdd-workflow 的可运行红绿重构示例、api-tester 的契约测试示例。

工具型技能(SKILL.md 里的"辅助脚本"章节)都会说明用法。脚本只做标记或测量,结论由人确认。

## 安装

### 方式一:gh skill(推荐)

需要 [GitHub CLI](https://cli.github.com) v2.90.0+:

```bash
# 装全部
gh skill install Laffey-82/cn-agent-skills

# 只装一个,指定 Agent
gh skill install Laffey-82/cn-agent-skills requirement-clarifier --agent claude-code
```

### 方式二:一键脚本

macOS / Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/Laffey-82/cn-agent-skills/main/install.sh | bash
```

Windows(PowerShell):

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

脚本会检测本机装了的 Agent,把技能复制到对应目录:

| 工具 | 全局目录 | 项目目录 |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex | `~/.codex/skills/` | `.agents/skills/` |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` |
| TRAE | `~/.trae/skills/` | `.trae/skills/` |
| OpenCode | `~/.config/opencode/skills/` | `.opencode/skills/` |

### 方式三:手动

把 `skills/` 下对应的技能目录整个复制到上表的位置。

## 用法

装完直接说中文:

```text
"帮我把这个需求理清楚,然后拆成任务"
"按 TDD 的方式实现这个功能"
"提交前帮我 review 一下改动"
"这个报错帮我系统排查一下"
```

## 贡献

想加技能或者改现有技能,先看 [CONTRIBUTING.md](./CONTRIBUTING.md)。新技能要过 [docs/CHECKLIST.md](./docs/CHECKLIST.md) 的质量门禁,机器检查由 CI 自动执行。

## 计划

见 [docs/ROADMAP.md](./docs/ROADMAP.md)。

## License

[MIT](./LICENSE)
