# 常见报错速查

## 端口类

| 报错 | 原因 | 处理 |
|---|---|---|
| EADDRINUSE | 端口被占 | 找占用进程结束,或换端口 |
| Address already in use | 端口被占 | 同上 |
| bind: permission denied | 用了 1024 以下端口且非 root | 换高位端口 |

## 依赖类

| 报错 | 原因 | 处理 |
|---|---|---|
| Cannot find module 'x' | 包没装 | npm install / 检查 node_modules |
| ModuleNotFoundError | 包没装或环境不对 | pip install,确认 venv 激活 |
| peer dep conflict | 依赖版本冲突 | 按提示升级/降级,或 --legacy-peer-deps |
| checksum mismatch | 下载损坏或镜像不一致 | 清缓存重装 |

## 数据库连接类

| 报错 | 原因 | 处理 |
|---|---|---|
| ECONNREFUSED | 服务没起或端口不对 | 确认数据库在跑、端口正确 |
| Access denied for user | 账号密码错 | 核对凭据、host 授权 |
| Unknown database | 库名不存在 | 先建库 |
| connection refused (socket) | 连接方式不对 | 确认 TCP 还是 socket |

## 环境变量类

- 变量名写错(和 .env.example 对比);
- .env 没加载(启动方式没走 dotenv);
- 变量值带空格或引号;
- 系统 PATH 里没有对应命令(重启终端/IDE)。

## 网络与代理类

- npm/pip 超时:检查代理,必要时换镜像源;
- localhost 不通但 127.0.0.1 通:DNS 或 hosts 问题;
- 公司内网:确认是否走内网源/代理。

## 缓存类

| 症状 | 处理 |
|---|---|
| 改了代码不生效 | 确认重新编译/重启,清构建缓存 |
| 浏览器拿旧资源 | 硬刷新,检查缓存头 |
| 依赖行为诡异 | 删 node_modules / .venv 重装 |

## 排查顺序速记

服务 → 端口 → 地址 → 依赖 → 配置 → 网络 → 缓存 → 代码

一层一层来,一次只改一个变量。
