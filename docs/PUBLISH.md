# cn-agent-skills 维护发布指南

仓库已发布在 [github.com/Laffey-82/cn-agent-skills](https://github.com/Laffey-82/cn-agent-skills)。本文件说明日常怎么改、什么时候发版。

## 日常迭代

1. 改技能、加资料、补脚本;
2. 本地验证:
   - `npx -y skills-ref validate ./skills/<技能名>`(每个改动的技能);
   - Python 脚本改动跑 `python -m py_compile` 确认语法;
3. 提交,信息按提交规范:
   ```text
   feat: 新增 XX 技能
   docs: 补充 XX 参考
   fix: 修正 XX 步骤
   ```
4. 推送到 main,CI 会自动跑技能校验和脚本语法检查。

## 发版规则

**只有大更新才发版。** 小迭代(文档、单个技能微调)只提交不发布。

满足以下任一情况算大更新:

- 新增了技能;
- 一批技能有实质性深化(新脚本、新示例);
- 仓库结构或工作流有大的调整。

发版步骤:

```bash
git tag v0.8.0
git push origin v0.8.0
gh release create v0.8.0 --title "cn-agent-skills v0.8.0" --notes "一句话说明本次更新"
```

同时更新 CHANGELOG.md。

## 技能质量标准

- 原创,不搬运;
- frontmatter 含 name + description,name 与目录名一致;
- SKILL.md ≤ 500 行,复杂内容拆 references/;
- 脚本只做标记或测量,结论由人确认;
- 文案自然,不出现空泛套话和 emoji 堆砌;
- 每个技能能说清:何时用、怎么用、产出什么、怎么验证。
