# 贡献指南

这个仓库的东西可以随便拿去用,但往仓库里加内容,标准只有一条:能用、原创、像人写的。

## 加一个新技能

1. 先读 [docs/STYLE_GUIDE.md](./docs/STYLE_GUIDE.md) 和 [docs/CHECKLIST.md](./docs/CHECKLIST.md),搞清仓库的规矩;
2. 动手前想清楚三件事:解决什么问题、什么时候触发、产出是什么。想不清楚就先开个 Issue 讨论;
3. 生成骨架再填充(推荐),也可以手动写 `skills/<技能名>/SKILL.md`:

   ```bash
   python skills/skill-creator-cn/scripts/skill_scaffold.py <技能名> --description "<做什么 + 什么时候用>"
   ```

   frontmatter 要有 `name` 和 `description`:
   - `name` 小写、连字符,和目录名一致;
   - `description` 写清"做什么 + 什么时候用",中文为主,附英文关键词方便搜索;
4. SKILL.md 控制在 500 行内,内容多了拆到 `references/` 或 `scripts/`;
5. 跑机器自检,全过再进人工评审:

   ```bash
   python skills/skill-style-guide/scripts/style_checker.py <技能名>
   skills-ref validate ./skills/<技能名>
   ```
6. 在至少一种 Agent 里用真实任务试一遍,能触发、能跑完、产出对,才算完成;
7. 更新 README 技能列表和 [docs/ROADMAP.md](./docs/ROADMAP.md),然后在 PR 里写清楚验证过程。

## 改现有技能

- 保持原有风格,别破坏已经能用的触发词;
- 改完重新验证,PR 里说明改了什么、为什么改;
- 涉及脚本的,写清运行环境和依赖。

## 什么内容不收

- 抄来的、改写的、来源不明的;
- 只有一两句话、没有步骤的"假技能";
- 描述含糊,说不清什么时候触发的;
- 没人验证过能不能用的。

## 提交信息

按 [commit-message-writer](./skills/commit-message-writer) 的规范:

```text
feat: 新增 api-tester 技能
fix: 修正 tdd-workflow 第三步的表述
docs: 更新技能列表
```

## 沟通

- 讨论问题就事论事;
- 大改动先开 Issue,别闷头写完才发现方向不对;
- 有争议的先讲依据,再讲立场。
