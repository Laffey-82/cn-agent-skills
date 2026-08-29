# cn-agent-skills · 中文 Agent 技能库

给 Claude Code、Codex、Cursor、TRAE、OpenCode 用的中文技能集。每个技能解决一个具体问题,按"需求 → 拆解 → 开发 → 审查 → 发布"这条线组织,装上就能用。

[English](./README.en.md) · [技能索引](#技能索引) · [安装](#安装) · [贡献](./CONTRIBUTING.md)

## 背景

英文技能库的问题,用过的人都知道:触发词是英文思维,中文说"帮我理下需求""把这事拆开",经常没反应;写出来的提交信息、文档、注释,一股洋味,跟中文团队的工程习惯对不上;技能之间各说各话,没有一个连贯的流程。

这个仓库把日常开发里最常遇到的 15 个场景做成了技能。内容自己写的,不搬运;每个技能都过了官方校验,附触发示例和验证步骤。

## 技能列表

| 技能 | 干什么 | 触发示例 |
|---|---|---|
| requirement-clarifier | 需求模糊时,多轮提问把它理清楚,输出需求规格 | "帮我把这个需求理清楚" |
| task-decomposer | 把大任务拆成带验收标准的小任务,排出依赖顺序 | "把这个功能拆成任务" |
| tdd-workflow | 红灯-绿灯-重构循环,先写测试再实现 | "按 TDD 来做" |
| code-reviewer | 从正确性、安全、性能、可维护性四个维度审查代码 | "帮我 review 这段代码" |
| commit-message-writer | 按 Conventional Commits 生成提交信息,支持中文 | "写个 commit message" |
| tech-doc-writer | 先读代码再写文档,示例全部实测过 | "给这个项目写 README" |
| bug-diagnoser | 先复现、再取证、二分定位根因,修复后补回归测试 | "这个报错怎么排查" |
| git-workflow | 整理提交历史,原子提交,干净分支 | "帮我把提交整理干净" |
| api-tester | 按真实契约生成 API 测试,确认环境后执行并出报告 | "给这个接口写测试" |
| ci-cd-setup | 根据项目现状搭 CI/CD,先生成配置再跑通 | "帮我搭个 CI" |
| natural-chinese-writer | 把 AI 腔的文字改成人话,保留原意 | "这段文字看着别扭,帮我改得像人写的" |
| skill-creator-cn | 从需求出发创建符合规范的新技能 | "帮我做一个技能" |
| skill-style-guide | 检查技能是否符合仓库风格 | "这个技能风格对吗" |

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

```bash
curl -fsSL https://raw.githubusercontent.com/Laffey-82/cn-agent-skills/main/install.sh | bash
```

脚本会检测本机装了的 Agent,把技能复制到对应目录:

| 工具 | 全局目录 | 项目目录 |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex | `~/.codex/skills/` | `.agents/skills/` |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` |
| TRAE | `~/.trae/skills/` | `.trae/skills/` |
| OpenCode | `~/.opencode/skills/` | `.opencode/skills/` |

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

想加技能或者改现有技能,先看 [CONTRIBUTING.md](./CONTRIBUTING.md),新技能要过 [docs/CHECKLIST.md](./docs/CHECKLIST.md) 的质量门禁。

## 计划

见 [docs/ROADMAP.md](./docs/ROADMAP.md)。

## License

[MIT](./LICENSE)



