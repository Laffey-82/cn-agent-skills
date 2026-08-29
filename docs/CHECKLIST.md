# 技能质量门禁 Checklist

每个技能合并前,逐项自检:

## 结构

- [ ] `skills/<name>/SKILL.md` 存在
- [ ] frontmatter 含 `name` 和 `description`
- [ ] `name` 小写、连字符、与目录名一致
- [ ] SKILL.md 主体 ≤ 500 行
- [ ] 复杂内容已拆到 `references/` 或 `scripts/`
- [ ] `skills-ref validate ./skills/<name>` 通过

## 内容

- [ ] 完全原创
- [ ] description 写清"做什么 + 何时触发"
- [ ] 步骤具体到可执行,有中文示例
- [ ] 包含"不适用场景",避免误触发
- [ ] 包含"验证方式"

## 分发

- [ ] README 技能索引表已更新
- [ ] 触发示例覆盖中文表达
- [ ] 在至少一种 Agent 环境中验证过

## 提交信息

- [ ] 遵循 `<type>: <subject>` 规范
