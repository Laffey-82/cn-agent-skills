# cn-agent-skills 发布清单

本地仓库已初始化并完成首个提交,只差"推到 GitHub"这一步。按顺序执行:

## 1. 创建 GitHub 远程仓库

在 GitHub 新建仓库,名称:`cn-agent-skills`,描述建议:

```text
中文 Agent 技能库 · Chinese Agent Skills Library for Claude Code / Codex / Cursor / TRAE / OpenCode
```

- License 选择 MIT;
- **不要**勾选 README/.gitignore(本地已有),否则推送会冲突。

## 2. 替换 README 中的占位用户名

README.md / README.en.md 中所有 `<你的用户名>` / `<your-username>` 替换为你的 GitHub 用户名。

## 3. 推送

```bash
git remote add origin https://github.com/<你的用户名>/cn-agent-skills.git
git push -u origin main
```

## 4. 官方校验与发布

```bash
gh skill publish        # 校验技能并建议开启安全设置
gh skill publish --fix  # 自动修复元数据问题(如有)
```

## 5. 打首个 Release

```bash
git tag v0.1.0
git push origin v0.1.0
```

在 GitHub 页面创建 Release,勾选 immutable releases(不可变发布,供应链安全)。

## 6. 冷启动推广(0 → 500 星)

- Linux.do(资源荟萃 + 公益推广标签)、V2EX(分享创造)、NodeSeek;
- Reddit:r/ClaudeAI、r/codex、r/ChatGPTCoding;
- X/Twitter 发演示 GIF;
- 投稿:阮一峰周刊、HelloGitHub、GitHubDaily;
- 向 awesome-* 技能清单提 PR(互相导流)。
