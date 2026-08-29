---
name: release-note-writer
description: 发版说明生成。收集自上个 tag 以来的提交,按 Conventional Commits 分组,生成发版说明草稿或 CHANGELOG 条目,破坏性变更单独标出。Use to draft release notes or changelog entries from git history.
license: MIT
metadata:
  version: "1.0.0"
---

# 发版说明生成

## 何时使用

- 用户说"发个版""写 release notes""更新 CHANGELOG";
- 发版前要把这段时间的改动整理成对外的说明;
- 上个大版本之后改了很多,想快速知道改了啥。

## 使用步骤

### 第 1 步:确认发版范围

- 上个 tag 是什么(脚本默认自动找最近的 tag);
- 这次发版从哪到哪(默认上个 tag..HEAD);
- 版本号是多少(结合是否有破坏性变更,按 semver 判断升几级)。

### 第 2 步:收集提交并分组

跑脚本收集提交,命令见下面的[辅助脚本](#辅助脚本)。脚本按 Conventional Commits 分组,破坏性变更(BREAKING CHANGE 或 subject 带 !)单独列出,解析不了的提交进"待确认"。

### 第 3 步:整理成对外文案

- 草稿只是素材,要按实际影响重写:对外说明讲"用户能感知的变化",不逐条罗列 commit;
- 破坏性变更必须写清楚"以前什么样、现在什么样、怎么迁移";
- 内部改动(docs、chore)对外可以合并成一条;
- 拿不准的放进"待确认",和用户一起定。

### 第 4 步:确认后落盘

- release notes 写到文件或直接给文本;
- 仓库用 CHANGELOG 的,用 --changelog 模式生成条目,核对后并入 CHANGELOG.md;
- 版本号、日期以实际发布为准。

## 输入与输出

- 输入:git 仓库路径 + 版本范围(可选)+ 版本号(可选);
- 输出:发版说明草稿或 CHANGELOG 条目。

## 示例

**用户输入:** "准备发 v0.9.0,写一下 release notes。"

**脚本输出(节选):**

```text
## 破坏性变更
- [05fcdd1] fix!: 修正接口返回结构,调用方需适配
## 新功能
- [5dff88b] feat(api): 新增登录接口
```

**对外文案节选:**

```markdown
## 新功能
- 登录接口上线,支持用户名密码换取 token
## 破坏性变更
- 接口返回结构调整:data 从数组改为对象,老调用方需迁移(见迁移说明)
```

## 辅助脚本

[scripts/release_note_gen.py](scripts/release_note_gen.py) 从 git 历史收集提交,按类型分组,破坏性变更单独列出:

```bash
# 上个 tag..HEAD,输出草稿
python skills/release-note-writer/scripts/release_note_gen.py --repo <仓库路径>

# 生成 CHANGELOG 条目
python skills/release-note-writer/scripts/release_note_gen.py --repo <仓库路径> --changelog --version v0.9.0
```

脚本只做收集和分组,对外文案由人写。

## 注意事项

- **草稿不等于文案**:commit 是给开发者看的,release notes 是给用户看的,要重写;
- 破坏性变更单独成段,别埋在"修复"里;
- 没按 Conventional Commits 写的提交进"待确认",人工归类;
- 版本号按 semver 判断:破坏性变更升主版本,新功能升次版本,修复升补丁。

## 不适用场景

- 还没有版本范围和版本号,纯聊天;
- 仓库没有 tag 也没有明确起始点(用 --since 指定 commit 可以兜底);
- 用户要的是周报或个人总结(用 weekly-report)。

## 验证方式

1. 触发:"写 release notes""更新 CHANGELOG";
2. 跑脚本:release_note_gen.py 输出与 git log 抽查结果一致;
3. 走查:破坏性变更全部单独列出,没有漏;
4. 确认:用户对对外文案无异议。
