---
name: ci-cd-setup
description: "CI/CD 搭建。先摸清项目构建和测试命令,规划最小可用流水线,生成 CI 配置,跑通后再逐步加步骤。Use to set up or fix CI/CD pipelines based on the project's actual build and test commands."
license: MIT
metadata:
  version: "1.0.0"
---

# CI/CD 搭建

## 何时使用

- 用户说"帮我搭个 CI""配一下 GitHub Actions";
- 项目没有自动化测试/构建,每次发布靠手动;
- 现有流水线经常挂,想查为什么;
- 需要加部署步骤,但不确定怎么接。

## 使用步骤

### 第 1 步:摸清项目现状

先回答三个问题,答不上来就先查:

1. 用什么语言和包管理器(读 `package.json`、`pyproject.toml`、`go.mod` 等);
2. 构建命令是什么(能不能本地跑通);
3. 测试和 lint 命令是什么(有没有现成脚本)。

### 第 2 步:确认平台与目标

- 平台:GitHub Actions、GitLab CI、Jenkins,还是别的;
- 目标:只要构建+测试,还是要部署;
- 触发:push 到 main 就跑,还是 PR 也要跑。

### 第 3 步:规划最小流水线

先从最简开始,跑通了再加:

```text
checkout → 装依赖 → 构建 → 测试 → lint(可选)
```

部署单独作为最后一步,并且:

- 部署到生产前必须有手动确认或受保护分支;
- 密钥走平台的 secrets,不写进配置文件;
- 先部署到 staging,验证通过再推生产。

### 第 4 步:生成配置

以 GitHub Actions 为例:

```yaml
name: ci
on:
  push:
    branches: [main]
  pull_request:

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run build
      - run: npm test
```

其他平台给出对应格式。

### 第 5 步:本地验证配置

- 配置里的命令逐条在本地跑一遍,确认能过;
- 无法本地验证的部分(如部署),写明前置条件和验证方式;
- 把配置提交给用户 review,说明每一步的作用。

### 第 6 步:跑通并迭代

1. 推送后看 CI 结果,红了就定位修复;
2. 绿了再考虑加步骤(缓存、并行、覆盖率);
3. 输出一份简短说明:流水线做什么、怎么改、密钥怎么配。

## 输入与输出

- 输入:项目目录 + 平台选择;
- 输出:CI 配置文件 + 说明文档。

## 示例

**用户输入:** "给这个 Python 项目搭 GitHub Actions。"

**现状:** `pyproject.toml` 存在,`pytest` 可用,无 lint 脚本。

**最小配置节选:**

```yaml
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[dev]"
      - run: pytest
```

**说明:** 先只跑测试;后续要加 lint 先补 `ruff check` 脚本再进流水线。

## 注意事项

- 不要一次塞太多步骤,跑不通的流水线比没有更糟;
- 密钥一律走平台 secrets,禁止写死;
- 命令必须本地验证过,不能照抄模板;
- 构建慢的问题等跑通后再优化,别一开始就上缓存。

## 不适用场景

- 项目连构建命令都没有,需要先补工程基础;
- 用户没有 CI 平台账号或权限;
- 纯本地项目,短期没有自动化需求。

## 验证方式

1. 触发:"帮我搭个 CI";
2. 检查:配置中的每条命令本地跑通过,密钥走 secrets;
3. 走查:推送后 CI 首次运行变绿,或失败的步骤有明确修复记录。
