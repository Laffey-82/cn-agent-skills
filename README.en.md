# cn-agent-skills · Chinese Agent Skills Library

> Practical agent skills for Chinese-speaking developers. Make Claude Code / Codex / Cursor / TRAE / OpenCode understand Chinese workflows and follow engineering discipline.

[简体中文](./README.md) · [Skill Index](#-skill-index) · [Install](#-install) · [Contributing](./CONTRIBUTING.md)

## Why this project

Most English-first skill libraries miss three things Chinese developers need:

- **Weak triggers for Chinese input**: phrases like "帮我把需求理清楚" often don't trigger English-written skills;
- **Local conventions ignored**: commit messages, docs, and code comments that don't fit Chinese team habits;
- **Fragmented workflows**: no end-to-end line connecting requirements → planning → development → review → release.

`cn-agent-skills` provides a unified, ready-to-use, Chinese-first skill set covering the whole engineering workflow.

## Features

- 🇨🇳 Chinese-first content with bilingual descriptions
- 📐 Follows the open [Agent Skills spec](https://agentskills.io)
- 🔗 Closed-loop workflow: clarify requirements → decompose tasks → TDD → review → commit → document
- 🚀 `gh skill` compatible distribution
- 🧪 Every skill ships with trigger examples and a verification checklist

## Skill Index

| Skill | Problem it solves | Trigger example | Directory |
|---|---|---|---|
| requirement-clarifier | Vague requirements cause rework | "帮我把这个需求理清楚" | [skills/requirement-clarifier](./skills/requirement-clarifier) |
| task-decomposer | Hard to split large tasks | "把这个功能拆成任务" | [skills/task-decomposer](./skills/task-decomposer) |
| tdd-workflow | No TDD discipline | "按 TDD 来做" | [skills/tdd-workflow](./skills/tdd-workflow) |
| code-reviewer | Unstructured code review | "帮我 review 这段代码" | [skills/code-reviewer](./skills/code-reviewer) |
| commit-message-writer | Messy commit messages | "写个 commit message" | [skills/commit-message-writer](./skills/commit-message-writer) |
| tech-doc-writer | Docs are hard to write | "给这个项目写 README" | [skills/tech-doc-writer](./skills/tech-doc-writer) |
| bug-diagnoser | Bug fixing by guessing | "这个报错怎么排查" | [skills/bug-diagnoser](./skills/bug-diagnoser) |
| git-workflow | Messy git history | "帮我把提交整理干净" | [skills/git-workflow](./skills/git-workflow) |
| skill-creator-cn | Creating new skills | "帮我做一个技能" | [skills/skill-creator-cn](./skills/skill-creator-cn) |
| skill-style-guide | Consistent skill style | "这个技能风格对吗" | [skills/skill-style-guide](./skills/skill-style-guide) |

## Install

### Method 1: gh skill (recommended)

Requires [GitHub CLI](https://cli.github.com) v2.90.0+:

```bash
gh skill install Laffey-82/cn-agent-skills
gh skill install Laffey-82/cn-agent-skills requirement-clarifier --agent claude-code
```

### Method 2: One-liner script

```bash
curl -fsSL https://raw.githubusercontent.com/Laffey-82/cn-agent-skills/main/install.sh | bash
```

### Method 3: Manual copy

Copy each folder under `skills/` into your agent's skill directory (e.g. `~/.claude/skills/`, `~/.codex/skills/`, `~/.cursor/skills/`, `~/.trae/skills/`, `~/.opencode/skills/`).

## Usage

After installation, just say it in Chinese:

```text
"帮我把这个需求理清楚,然后拆成任务"
"按 TDD 的方式实现这个功能"
"提交前帮我 review 一下改动"
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). Every skill must pass the [CHECKLIST](./docs/CHECKLIST.md) quality gate.

## Roadmap

See [docs/ROADMAP.md](./docs/ROADMAP.md).

## License

[MIT](./LICENSE)

