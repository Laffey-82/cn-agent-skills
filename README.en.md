# cn-agent-skills

Chinese-first agent skills for Claude Code, Codex, Cursor, TRAE and OpenCode. Each skill solves one concrete problem; together they cover the flow from requirements to release.

[简体中文](./README.md) · [Skill list](#skill-list) · [Install](#install) · [Contributing](./CONTRIBUTING.md)

## Why

English-first skill libraries miss how Chinese developers actually work. Triggers are written in English, so phrases like "帮我理下需求" often do nothing. Commit messages, docs and comments come out in a style that does not fit Chinese teams. Skills are scattered, with no coherent workflow between them.

This repo turns the 18 most common development scenarios into skills. Content is written from scratch, not copied. Every skill passes the official validator and ships with trigger examples and verification steps.

## Skill list

| Skill | What it does | Trigger example |
|---|---|---|
| requirement-clarifier | Clarify vague requirements through rounds of questions, output a spec | "帮我把这个需求理清楚" |
| task-decomposer | Split large tasks into small verifiable ones, order by dependencies | "把这个功能拆成任务" |
| tdd-workflow | Red-green-refactor loop, test first | "按 TDD 来做" |
| code-reviewer | Review code on correctness, security, performance, maintainability | "帮我 review 这段代码" |
| commit-message-writer | Conventional Commits messages, Chinese-friendly | "写个 commit message" |
| tech-doc-writer | Read the code first, then write docs; every example is tested | "给这个项目写 README" |
| bug-diagnoser | Reproduce, gather evidence, bisect the root cause, add a regression test | "这个报错怎么排查" |
| dev-env-troubleshooter | Walk through a ladder of checks when services, ports or databases fail locally | "本地起不来" |
| git-workflow | Clean history, atomic commits, tidy branches | "帮我把提交整理干净" |
| api-tester | Generate API tests from the real contract, run and report | "给这个接口写测试" |
| db-migration-reviewer | Review migrations for safety, rollback and locking risks | "帮我看下这个迁移安不安全" |
| ci-cd-setup | Set up CI/CD based on the project, generate config, run it | "帮我搭个 CI" |
| natural-chinese-writer | Rewrite stiff or formulaic Chinese into natural prose | "这段文字看着别扭,帮我改得像人写的" |
| security-reviewer | Review code for injection, auth and data exposure issues | "帮我看下安不安全" |
| performance-profiler | Baseline first, then profile to find bottlenecks | "这个接口好慢" |
| db-schema-designer | Design tables, fields, relations and indexes from requirements | "帮我设计数据模型" |
| skill-creator-cn | Create a new spec-compliant skill from a need | "帮我做一个技能" |
| skill-style-guide | Check a skill against the repo style | "这个技能风格对吗" |

## Install

### Method 1: gh skill (recommended)

Requires [GitHub CLI](https://cli.github.com) v2.90.0+:

```bash
gh skill install Laffey-82/cn-agent-skills
gh skill install Laffey-82/cn-agent-skills requirement-clarifier --agent claude-code
```

### Method 2: one-liner

```bash
curl -fsSL https://raw.githubusercontent.com/Laffey-82/cn-agent-skills/main/install.sh | bash
```

### Method 3: manual

Copy a skill folder under `skills/` into your agent's skill directory (e.g. `~/.claude/skills/`, `~/.codex/skills/`).

## Usage

Just say it in Chinese:

```text
"帮我把这个需求理清楚,然后拆成任务"
"按 TDD 的方式实现这个功能"
"提交前帮我 review 一下改动"
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). New skills must pass the [CHECKLIST](./docs/CHECKLIST.md).

## Roadmap

See [docs/ROADMAP.md](./docs/ROADMAP.md).

## License

[MIT](./LICENSE)



