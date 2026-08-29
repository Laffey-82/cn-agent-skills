# Git 命令速查

## 分支命名

```text
feature/登录功能
fix/修复金额计算
docs/补充安装说明
refactor/提取公共方法
```

规则:类型/一句话说明,小写连字符,不用中文以外的特殊字符。

## 原子提交

一个 commit 只做一件事,判断标准:

- 能不能单独回滚?
- 提交信息能不能一句话说清?
- 出问题时能不能准确定位?

## 整理历史

```bash
# 合并最近 N 个提交
git rebase -i HEAD~N

# 只暂存部分改动
git add -p

# 修改最近一次提交信息
git commit --amend
```

## rebase 还是 merge

| 场景 | 用 |
|---|---|
| 个人分支,想保持历史线性 | rebase |
| 共享分支,不想改写历史 | merge |
| 合入主干,功能开发完 | squash 合并 |

## 冲突处理

1. 逐个文件看冲突标记;
2. 保留双方合理逻辑;
3. 解决后 `git add`,继续 rebase/merge;
4. 跑测试确认无回归。

## 危险操作

```bash
# 以下操作会丢历史/改历史,先确认再用
git reset --hard
git clean -f
git push -f
```

## 提交信息速查

```text
<type>(<scope>): <subject>
```

类型:feat / fix / docs / style / refactor / perf / test / build / chore / ci / revert

subject ≤ 72 字,动词开头,一句话说清。
