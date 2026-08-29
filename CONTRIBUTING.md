# 贡献指南

感谢你愿意为 `cn-agent-skills` 做贡献。这个仓库的质量标准是:**质量不合格的技能,宁可不收录。**

## 新增一个技能

1. 先看 [docs/STYLE_GUIDE.md](./docs/STYLE_GUIDE.md),理解仓库的风格约定;
2. 在 `skills/<技能名>/` 下创建 `SKILL.md`,frontmatter 必须包含 `name` 和 `description`:
   - `name`:小写、连字符,必须与目录名完全一致;
   - `description`:中英双语或中文为主,写清"做什么 + 何时触发";
3. SKILL.md 主体控制在 500 行以内,复杂内容拆到 `references/` 或 `scripts/`;
4. 用官方校验工具检查格式:`skills-ref validate ./skills/<技能名>`;
5. 在至少一种 Agent 环境中用真实任务验证触发与执行,把结果写进 PR 描述;
6. 更新 README 的技能索引表和 [docs/ROADMAP.md](./docs/ROADMAP.md)。

## 修改现有技能

- 保持原有风格与结构,不破坏触发词兼容性;
- 修改后必须重新验证,并在 PR 中说明改动前后行为差异;
- 涉及脚本时,说明运行环境与依赖。

## PR 质量门禁

每个 PR 必须通过 [docs/CHECKLIST.md](./docs/CHECKLIST.md) 的检查项:

- 结构合规:SKILL.md 存在、frontmatter 合法、目录名与 name 一致;
- 内容原创:不搬运、不抄袭、不改写他人成品;
- 可执行:步骤具体到 Agent 能直接执行,附触发示例;
- 可验证:有明确的"验证方式"说明(在哪个工具、用什么触发词、产出是什么);
- 风格一致:符合 STYLE_GUIDE 的约定。

## 提交信息

遵循本仓库 [commit-message-writer](./skills/commit-message-writer) 技能定义的规范:

```text
feat: 新增 requirement-clarifier 技能
fix: 修正 tdd-workflow 第 3 步的表述歧义
docs: 更新技能索引表
```

## 行为准则

- 友善、具体、对事不对人;
- 不收录来源不明或涉及版权风险的内容;
- 大改动先开 Issue 讨论,避免重复劳动。
