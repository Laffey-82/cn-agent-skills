# cn-agent-skills · 中文 Agent 技能库

> 面向中文开发者的 AI 编程 Agent 实战技能库。让 Claude Code / Codex / Cursor / TRAE / OpenCode 更懂中文场景、更守工程纪律。

[English README](./README.en.md) · [技能索引](#-技能索引) · [安装](#-安装) · [贡献](./CONTRIBUTING.md)

## 为什么需要它

大多数英文技能库存在三个"中文开发者痛点":

- **触发不灵**:描述是英文思维,中文表达"帮我理清需求""把这事拆一下"经常触发不了;
- **规范水土不服**:英文提交信息、英文文档、西式代码注释,和中文团队的工程习惯对不上;
- **流程太散**:每个技能各讲各的,没有一条贯穿"需求 → 拆解 → 开发 → 审查 → 发布"的主线。

`cn-agent-skills` 把这套工程工作流做成了**统一标准、开箱即用、中文优先**的技能集。

## ✨ 特性

- 🇨🇳 **中文优先**:所有技能内容中文编写,description 中英双语,触发词覆盖中文表达;
- 📐 **开放标准**:遵循 [Agent Skills 规范](https://agentskills.io),兼容 Claude Code、Codex、Cursor、TRAE、OpenCode;
- 🔗 **流程闭环**:需求澄清 → 任务拆解 → TDD → 代码审查 → 提交规范 → 文档生成,一条主线串起来;
- 🚀 **官方分发**:仓库结构符合 `gh skill` 规范,支持一条命令安装;
- 🧪 **可验证**:每个技能都附触发示例与执行检查清单,宁缺毋滥。

## 📇 技能索引

| 技能 | 解决什么问题 | 触发示例 | 目录 |
|---|---|---|---|
| requirement-clarifier | 需求模糊导致反复返工 | "帮我把这个需求理清楚" | [skills/requirement-clarifier](./skills/requirement-clarifier) |
| task-decomposer | 大任务不知道怎么拆 | "把这个功能拆成任务" | [skills/task-decomposer](./skills/task-decomposer) |
| tdd-workflow | 测试驱动开发纪律 | "按 TDD 来做" | [skills/tdd-workflow](./skills/tdd-workflow) |
| code-reviewer | 代码审查没章法 | "帮我 review 这段代码" | [skills/code-reviewer](./skills/code-reviewer) |
| commit-message-writer | 提交信息不规范 | "写个 commit message" | [skills/commit-message-writer](./skills/commit-message-writer) |
| tech-doc-writer | 文档不会写/不愿写 | "给这个项目写 README" | [skills/tech-doc-writer](./skills/tech-doc-writer) |
| bug-diagnoser | 修 Bug 全靠猜 | "这个报错怎么排查" | [skills/bug-diagnoser](./skills/bug-diagnoser) |
| git-workflow | 提交历史一团乱 | "帮我把提交整理干净" | [skills/git-workflow](./skills/git-workflow) |
| skill-creator-cn | 创建新技能 | "帮我做一个技能" | [skills/skill-creator-cn](./skills/skill-creator-cn) |
| skill-style-guide | 保持技能风格统一 | "这个技能风格对吗" | [skills/skill-style-guide](./skills/skill-style-guide) |

## 🚀 安装

### 方式一:gh skill(推荐)

需要 [GitHub CLI](https://cli.github.com) v2.90.0+。仓库发布后:

```bash
# 安装全部技能到当前默认 Agent
gh skill install <你的用户名>/cn-agent-skills

# 安装单个技能到指定 Agent
gh skill install <你的用户名>/cn-agent-skills requirement-clarifier --agent claude-code
```

### 方式二:一键脚本

```bash
curl -fsSL https://raw.githubusercontent.com/<你的用户名>/cn-agent-skills/main/install.sh | bash
```

脚本会自动检测已安装的 Agent,并把技能复制到对应目录:

| 工具 | 全局目录 | 项目目录 |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex | `~/.codex/skills/` | `.agents/skills/` |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` |
| TRAE | `~/.trae/skills/` | `.trae/skills/` |
| OpenCode | `~/.opencode/skills/` | `.opencode/skills/` |

### 方式三:手动复制

把 `skills/<技能名>/` 整个目录复制到上表对应位置即可。

## 💡 使用示例

安装后,直接说中文即可触发:

```text
"帮我把这个需求理清楚,然后拆成任务"
"按 TDD 的方式实现这个功能"
"提交前帮我 review 一下改动"
"给这个模块写中文技术文档"
"这个报错帮我系统排查一下"
```

## 🤝 贡献

欢迎提 PR 新增技能或改进现有技能。请先阅读 [CONTRIBUTING.md](./CONTRIBUTING.md),并确保新技能通过 [docs/CHECKLIST.md](./docs/CHECKLIST.md) 中的质量门禁。

## 🗺️ Roadmap

见 [docs/ROADMAP.md](./docs/ROADMAP.md)。

## 📄 License

[MIT](./LICENSE)

---

*cn-agent-skills — 让 AI 编程更懂中文,更守纪律。*
