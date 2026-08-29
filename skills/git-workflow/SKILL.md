---
name: git-workflow
description: "Git 工作流规范。整理提交历史、规范分支命名、拆分过大的 commit、处理冲突,产出干净可回滚的提交记录。Use to keep git history clean: atomic commits, proper branch naming, rebase, and conflict resolution."
license: MIT
metadata:
  version: "1.0.0"
---

# Git 工作流规范

## 何时使用

- 提交历史混乱(一次提交塞了很多改动);
- 分支命名随意("test""123""new");
- 用户说"帮我把提交整理干净""squash 一下";
- 冲突需要处理,或需要规划合并策略。

## 使用步骤

### 第 1 步:检查现状

```bash
git status
git log --oneline --graph -20   # 最近的提交历史
git branch -a                   # 分支情况
```

### 第 2 步:规划目标历史

确定:

1. 哪些改动应该合并成一个 commit;
2. 每个 commit 的提交信息(遵循 [commit-message-writer](../commit-message-writer/SKILL.md) 规范);
3. 是否要拆分成多个 commit。

### 第 3 步:整理历史

常用操作:

```bash
# 合并最近 N 个提交
git rebase -i HEAD~N

# 拆分暂存内容
git add -p

# 修改最近一次提交信息
git commit --amend
```

原则:

- **原子提交**:一个 commit 只做一件事,可独立回滚;
- 提交信息遵循 `<type>: <subject>` 规范;
- 功能分支命名:`feature/<说明>`、`fix/<说明>`、`docs/<说明>`;
- 个人分支上优先 `rebase` 保持线性历史;共享分支禁止改写已推送历史;
- 合入主干推荐 squash 合并或 rebase 合并,保持主干整洁。

### 第 4 步:处理冲突

1. 冲突时逐个文件解决,保留双方合理逻辑;
2. 解决后执行 `git add` 并继续 rebase/merge;
3. 冲突解决后运行测试确认无回归;
4. 输出冲突解决说明(哪些取舍、依据是什么)。

### 第 5 步:验证

```bash
git log --oneline --graph
git status
```

确认:历史线性、commit 原子、信息规范、工作区干净。

## 输入与输出

- 输入:当前仓库状态 + 期望整理目标;
- 输出:整理后的提交历史 + 操作记录说明。

## 示例

**用户:** "帮我 squash 最近 3 个提交。"

**执行:**

```bash
git rebase -i HEAD~3
# 将后两个 pick 改为 squash
```

**结果:**

```text
feat(api): 增加用户注册接口
```

## 辅助脚本

[scripts/git_stats.py](scripts/git_stats.py) 统计最近提交的类型分布、作者分布,标出信息不规范或超长的提交:

```bash
python scripts/git_stats.py --count 50
```

脚本只做统计,结论需要人确认。

## 注意事项

- **改写已推送的共享分支历史前必须确认**,未经确认不做 `push -f`;
- 不执行 `git reset --hard`、`git clean -f` 等破坏性命令,除非用户明确要求;
- 操作前建议备份:记录当前 HEAD 的 hash;
- 整理历史不等于掩盖问题,提交信息要如实描述改动。

## 不适用场景

- 仓库历史是共享且不可改写的(只给建议不动手);
- 用户只需要一次提交(用 [commit-message-writer](../commit-message-writer/SKILL.md));
- 尚未初始化的仓库(先 `git init`)。

## 验证方式

1. 触发:"整理一下提交历史";
2. 检查:每个 commit 只包含一件事,信息规范,历史线性;
3. 验证:工作区干净,测试通过。

