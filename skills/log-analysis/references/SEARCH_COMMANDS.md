# 日志检索命令与常见模式

## 常用命令

### 按关键字搜

```bash
grep -iE "error|exception|timeout|failed|oom|panic" app.log
grep -c "ERROR" app.log        # 统计条数
grep -A 5 "exception" app.log  # 带下文 5 行
```

### 按时间窗过滤

```bash
# 文本日志
sed -n '/2026-08-29 14:00/,/2026-08-29 14:30/p' app.log

# 时间在后的用 awk
awk '$1 >= "14:00" && $1 <= "14:30"' app.log
```

### 结构化日志(JSON)

```bash
cat app.log | jq 'select(.level == "ERROR")'
cat app.log | jq 'select(.trace_id == "abc123")'
cat app.log | jq -r '[.time, .service, .level, .message] | @tsv'
```

### 按关联字段提取

```bash
# 提取某请求 ID 的全链路日志
grep "req_8f3a2c" app-*.log

# 统计每个 trace_id 的错误数
cat app.log | jq -r '.trace_id // empty' | sort | uniq -c | sort -rn | head
```

## 常见日志模式速认

| 模式 | 含义 | 下一步 |
|---|---|---|
| Connection refused | 下游服务没起/端口错 | 查服务状态与地址配置 |
| Timeout / deadline exceeded | 下游响应超时 | 查下游负载、慢查询、网络 |
| OOM / memory limit | 内存耗尽 | 查泄漏与内存配置 |
| Deadlock detected | 锁死锁 | 查事务顺序与锁范围 |
| NullPointer / TypeError | 空值/类型错 | 查上游返回结构 |
| 429 Too Many Requests | 被限流 | 查限流策略与调用频率 |
| 401 / 403 | 鉴权失败 | 查 token、权限配置 |

## 关联日志的通用字段

- request_id / trace_id / span_id;
- 业务主键:order_id、user_id;
- 服务名 + 实例 IP + 时间。

没有关联字段的日志,先建议补充,否则跨服务排查只能靠时间窗硬对齐。

## 报告脱敏规则

- 手机号、身份证、token 打码;
- 内部 IP、内网地址按需脱敏;
- 粘贴日志时去掉无关的长堆栈。
