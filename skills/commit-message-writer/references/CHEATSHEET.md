# 提交信息速查表

## 类型一览

| 类型 | 什么时候用 | 例子 |
|---|---|---|
| feat | 新功能 | feat: 增加登录接口 |
| fix | 修复 Bug | fix: 修复金额计算精度问题 |
| docs | 文档 | docs: 补充安装说明 |
| style | 格式调整,不影响逻辑 | style: 统一缩进 |
| refactor | 重构,不改变行为 | refactor: 提取公共方法 |
| perf | 性能优化 | perf: 列表接口减少 N+1 查询 |
| test | 测试 | test: 补充登录边界用例 |
| build | 构建、依赖 | build: 升级 typescript 到 5.x |
| chore | 杂项 | chore: 更新 .gitignore |
| revert | 回滚 | revert: 回滚登录接口改动 |

## 常见写法对比

| 写法 | 评价 |
|---|---|
| update | 看不出改了什么,不用 |
| 修复了一些问题 | 等于没说,不用 |
| fix: 修复购物车金额多算 1 分钱 | 清楚,可用 |
| feat(auth): 增加短信验证码登录 | 带范围,更清楚 |

## 提交信息模板

```text
<type>(<scope>): <一句话说明>

<为什么改、改了什么(可选)>

<BREAKING CHANGE 说明(可选)>
```

## 规则速记

1. 动词开头,祈使句;
2. 一句话不超过 72 字;
3. 一个 commit 一件事;
4. 破坏性变更必须写 BREAKING CHANGE;
5. 仓库有约定(如必须带 issue 号)就遵循约定。

## 示例

```text
fix(cart): 修复满减金额四舍五入多 1 分钱

先计算后取整,避免浮点误差累积。
```

```text
feat(api): 移除 v1 登录接口

BREAKING CHANGE: v1 /login 已移除,请迁移到 v2 /login。
```
