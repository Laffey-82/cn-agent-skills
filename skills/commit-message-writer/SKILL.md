---
name: commit-message-writer
description: 提交信息规范。根据暂存区改动生成符合 Conventional Commits 的提交信息,支持中文描述,自动处理类型、范围、破坏性变更。Use to write standardized commit messages from staged git changes.
license: MIT
metadata:
  version: "1.0.0"
---

# 提交信息规范

## 何时使用

- 用户说"写个 commit message""帮我提交";
- 提交信息不规范(整段废话、不写类型、一句"update");
- 需要为改动生成规范且可检索的提交信息。

## 使用步骤

### 第 1 步:查看改动

执行并分析:

```bash
git status
git diff --cached --stat   # 暂存区的改动概况
git diff --cached          # 具体改动
```

若暂存区为空,提示用户先 `git add`,或询问是否查看工作区改动。

### 第 2 步:确定类型与范围

类型(必选):

| 类型 | 含义 |
|---|---|
| feat | 新功能 |
| fix | 修复 Bug |
| docs | 文档 |
| style | 格式(不影响逻辑) |
| refactor | 重构(不改变行为) |
| perf | 性能优化 |
| test | 测试 |
| build | 构建/依赖 |
| chore | 杂项 |
| revert | 回滚 |

范围(可选):模块名,如 `feat(auth): 增加登录接口`。

### 第 3 步:生成提交信息

格式:

```text
<type>(<scope>): <subject>

<body(可选)>

<footer(可选,如 BREAKING CHANGE)>
```

规则:

- subject 一句话概括,≤ 72 字符;
- subject 用祈使句:动词开头(增加、修复、重构);
- 中文描述为主,类型用英文约定词;
- 一个 commit 只做一件事;
- 破坏性变更必须写 `BREAKING CHANGE:` 说明。

### 第 4 步:输出并应用

输出完整提交信息供用户确认,确认后执行:

```bash
git commit -m "<subject>" -m "<body>"
```

## 速查表

详细的类型列表、写法对比和模板见 [references/CHEATSHEET.md](references/CHEATSHEET.md)。

## 速查表

详细的类型列表、写法对比和模板见 [references/CHEATSHEET.md](references/CHEATSHEET.md)。

## 输入与输出

- 输入:git 暂存区改动(或用户描述的改动);
- 输出:规范化的提交信息(可含正文)。

## 示例

```bash
git add src/login.py tests/test_login.py
```

生成:

```text
feat(auth): 增加用户名密码登录接口

- 使用 bcrypt 校验密码
- 登录成功返回 JWT,失败返回 401
- 补充登录接口单元测试
```

修复示例:

```text
fix(cart): 修复购物车满减金额计算错误

满减在四舍五入后多算了 1 分钱。
改为先计算再取整。
```

破坏性变更示例:

```text
feat(api): 移除 v1 登录接口

BREAKING CHANGE: v1 /login 接口移除,请迁移到 v2 /login。
```

## 注意事项

- **不要用"update""修复了一些东西"这类无信息提交**;
- 如果一次改动混杂多个类型,提示用户拆分成多个 commit;
- 未确认前不直接执行 `git commit`(先给用户看);
- 若仓库已有约定(如必须带 issue 号),遵循仓库约定并加入 footer。

## 不适用场景

- 用户要的是提交策略建议(用 [git-workflow](../git-workflow/SKILL.md));
- 改动尚未发生、纯设想场景;
- 用户明确指定了要写的内容。

## 验证方式

1. 触发:"写个 commit message";
2. 检查:格式为 `<type>: <subject>`,subject ≤ 72 字符且动词开头;
3. 抽查:对照 `git diff`,确认描述与改动一致。


