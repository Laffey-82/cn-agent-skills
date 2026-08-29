# CI 常见问题与模板

## 常见失败原因

| 现象 | 原因 | 处理 |
|---|---|---|
| 依赖装不上 | 网络、源、锁文件不一致 | 检查源和 lockfile,固定版本 |
| 构建失败 | 本地能过 CI 不过 | 对比 Node/Python 版本,检查平台差异 |
| 测试偶发失败 | 测试依赖顺序或时序 | 隔离测试、修竞态 |
| 权限失败 | 密钥没配或过期 | 检查 secrets、权限 |
| 部署失败 | 环境差异 | 确认部署脚本和环境一致 |

## 最小可用流水线

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

## 逐步加内容

1. 先构建 + 测试,跑通;
2. 加 lint、类型检查;
3. 加覆盖率报告;
4. 最后加部署(受保护分支 + 手动确认)。

## 密钥管理

- 一律走平台 secrets,不进配置文件;
- 不用 `${{ secrets.XXX }}` 之外的方式传敏感值;
- 定期轮换;
- 日志里禁止打印密钥。

## 检查清单

- 命令本地跑通过;
- 密钥走 secrets;
- 部署有保护;
- 失败有明确错误信息;
- 缓存、并行是跑通之后的事。
