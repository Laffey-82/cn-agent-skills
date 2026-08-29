# cn-agent-skills

Chinese-first agent skills for Claude Code, Codex, Cursor, TRAE and OpenCode. Each skill solves one concrete problem; together they cover the flow from requirements to release. Install a few or install them all.

[简体中文](./README.md) · [Skill list](#skill-list) · [Install](#install) · [Contributing](./CONTRIBUTING.md)

![stars](https://img.shields.io/github/stars/Laffey-82/cn-agent-skills?style=flat-square)
![license](https://img.shields.io/github/license/Laffey-82/cn-agent-skills?style=flat-square)
![skills](https://img.shields.io/badge/skills-29-green?style=flat-square)
![ci](https://img.shields.io/github/actions/workflow/status/Laffey-82/cn-agent-skills/validate-skills.yml?style=flat-square)

## What this is

An agent skill library built for Chinese-speaking teams:

- **Trigger it in Chinese.** Triggers are everyday phrases like "帮我把这个需求理清楚" or "这个报错怎么排查" — no English commands to memorize.
- **One line through the whole workflow.** Requirements, design, task breakdown, coding, testing, review, docs, reports and release each have a skill, and the output of one feeds the next.
- **Quality is enforced.** All 29 skills are written from scratch and pass the official validator. CI runs four gates (format, syntax, style, docs). Scripts are actually tested; they only flag or measure, humans make the call.

## Skill list

Grouped by phase. Pick whatever fits the moment.

### Before you code: think it through

| Skill | What it does | Trigger example |
|---|---|---|
| requirement-clarifier | Clarify vague requirements through rounds of questions, output a spec | "帮我把这个需求理清楚" |
| requirements-reviewer | Review a requirements doc or PRD for gaps | "评审一下这个需求" |
| tech-design-writer | Write a technical design doc with tradeoffs and risks | "写个技术方案" |
| api-contract-designer | Design an API contract before implementation | "设计接口契约" |
| task-decomposer | Split large tasks into small verifiable ones, order by dependencies | "把这个功能拆成任务" |

### Build & review: write it right

| Skill | What it does | Trigger example |
|---|---|---|
| tdd-workflow | Red-green-refactor loop, test first | "按 TDD 来做" |
| code-reviewer | Review code on correctness, security, performance, maintainability | "帮我 review 这段代码" |
| security-reviewer | Review code for injection, auth and data exposure issues | "帮我看下安不安全" |
| api-tester | Generate API tests from the real contract, run and report | "给这个接口写测试" |
| sql-reviewer | Scan SQL for anti-patterns: destructive ops without WHERE, SELECT *, leading-wildcard LIKE | "审一下这条 SQL" |
| db-schema-designer | Design tables, fields, relations and indexes from requirements | "帮我设计数据模型" |
| db-migration-reviewer | Review migrations for safety, rollback and locking risks | "帮我看下这个迁移安不安全" |
| cache-governor | Design keys and TTL, defend against penetration, hot-key and avalanche | "加个缓存" |
| ci-cd-setup | Set up CI/CD based on the project, generate config, run it | "帮我搭个 CI" |
| code-migrator | Migrate codebases in batches, each with tests and rollback | "把项目迁到 X" |

### Debug & performance: find it when it breaks

| Skill | What it does | Trigger example |
|---|---|---|
| bug-diagnoser | Reproduce, gather evidence, bisect the root cause, add a regression test | "这个报错怎么排查" |
| dev-env-troubleshooter | Walk through a ladder of checks when services, ports or databases fail locally | "本地起不来" |
| log-analysis | Rebuild the timeline from logs and correlate by request ID | "帮我查下日志" |
| frontend-debug | Walk Console → Network to debug white screens and failures | "页面白屏了" |
| performance-profiler | Baseline first, then profile to find bottlenecks | "这个接口好慢" |

### Engineering hygiene: commits & history

| Skill | What it does | Trigger example |
|---|---|---|
| commit-message-writer | Conventional Commits messages, Chinese-friendly | "写个 commit message" |
| git-workflow | Clean history, atomic commits, tidy branches | "帮我把提交整理干净" |

### Docs & communication: make it readable

| Skill | What it does | Trigger example |
|---|---|---|
| tech-doc-writer | Read the code first, then write docs; every example is tested | "给这个项目写 README" |
| natural-chinese-writer | Rewrite stiff or formulaic Chinese into natural prose | "这段文字看着别扭,改一下" |
| weekly-report | Turn this week's git history and work items into a Chinese weekly report | "帮我写周报" |
| meeting-minutes | Turn meeting discussions into Chinese minutes with decisions and trackable action items | "记会议纪要" |
| release-note-writer | Draft release notes or changelog entries from git history, breaking changes listed separately | "写 release notes" |

### Meta: skills about skills

| Skill | What it does | Trigger example |
|---|---|---|
| skill-creator-cn | Create a new spec-compliant skill from a need | "帮我做一个技能" |
| skill-style-guide | Check a skill against the repo style | "这个技能风格对吗" |

## Typical flow

Skills chain together. Taking "a product list page with login" as an example:

```text
1.  "帮我把这个需求理清楚"      → requirement-clarifier outputs a spec
2.  "评审一下这个需求"          → requirements-reviewer fills gaps
3.  "写个技术方案"              → tech-design-writer decides the design
4.  "设计接口契约"              → api-contract-designer writes the contract
5.  "把这个功能拆成任务"        → task-decomposer breaks down the work
6.  "按 TDD 实现登录接口"       → tdd-workflow writes the test first
7.  "给这个接口写测试"          → api-tester runs contract cases
8.  "提交前 review 一下"        → code-reviewer reviews on four axes
9.  "写个 commit message"       → commit-message-writer writes the message
10. "帮我搭个 CI"               → ci-cd-setup automates build and test
11. "这个接口好慢"              → performance-profiler finds the bottleneck
12. "发个版,写 release notes"   → release-note-writer drafts release notes
```

The output of each step feeds the next. Use the full chain for a new feature, or trigger a single skill whenever the moment calls for it.

## Skill structure

Skills come in three layers, loaded on demand:

- **Docs + references**: e.g. question templates in requirement-clarifier, case design in api-tester;
- **Executable scripts**: e.g. the scan helper in code-reviewer, the benchmark script in performance-profiler;
- **Runnable examples**: e.g. the red-green-refactor example in tdd-workflow, the contract test in api-tester.

Tool skills include a "辅助脚本" section in their SKILL.md explaining usage. Scripts only flag or measure; conclusions are confirmed by humans.

## Install

### Method 1: gh skill (recommended)

Requires [GitHub CLI](https://cli.github.com) v2.90.0+:

```bash
# install all
gh skill install Laffey-82/cn-agent-skills

# install one, targeting a specific agent
gh skill install Laffey-82/cn-agent-skills requirement-clarifier --agent claude-code
```

### Method 2: install script

macOS / Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/Laffey-82/cn-agent-skills/main/install.sh | bash
```

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

The script detects installed agents and copies skills to their directories:

| Tool | Global directory | Project directory |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex | `~/.codex/skills/` | `.agents/skills/` |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` |
| TRAE | `~/.trae/skills/` | `.trae/skills/` |
| OpenCode | `~/.config/opencode/skills/` | `.opencode/skills/` |

### Method 3: manual

Copy a skill folder under `skills/` into your agent's skill directory (e.g. `~/.claude/skills/`, `~/.codex/skills/`).

## Usage

Just say it in Chinese:

```text
"帮我把这个需求理清楚,然后拆成任务"
"按 TDD 的方式实现这个功能"
"提交前帮我 review 一下改动"
"这个报错帮我系统排查一下"
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). New skills must pass the [CHECKLIST](./docs/CHECKLIST.md); machine checks run automatically in CI.

## Roadmap

See [docs/ROADMAP.md](./docs/ROADMAP.md).

## License

[MIT](./LICENSE)
