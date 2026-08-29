# 剖析工具与指标参考

## 按场景选工具

| 场景 | 工具 |
|---|---|
| Python CPU | cProfile、py-spy |
| Python 内存 | tracemalloc、pympler |
| Node.js CPU | --cpu-prof、clinic.js |
| Node.js 内存 | --heap-prof、heapdump |
| Go | pprof(go tool pprof) |
| Java | JFR、async-profiler |
| 数据库 | EXPLAIN ANALYZE、慢日志、pg_stat_statements |
| 前端 | Chrome DevTools Performance、Lighthouse |
| 接口耗时 | curl -w、APM、应用日志 |
| 系统层 | top、htop、iostat、pidstat |

## 关键指标

| 指标 | 含义 |
|---|---|
| p50 / p95 / p99 | 中位 / 95 分位 / 99 分位耗时 |
| QPS | 每秒请求数 |
| CPU 占比 | 热点函数占的 CPU 时间 |
| 内存占用 | 常驻内存、泄漏趋势 |
| 锁等待 | 数据库或并发锁的等待时间 |
| GC / 分配 | 频繁 GC 通常是临时对象过多 |

## profiler 输出怎么读

- 火焰图顶部宽条 = 热点函数;
- 栈很深 = 抽象层过多;
- 顶部是 syscall / epoll_wait = IO 等待,不是 CPU 密集;
- 大量时间花在 json 解析 / 序列化 = 数据量或频率问题;
- 同一函数反复出现 = 循环内重复调用。

## 常见瓶颈模式

| 模式 | 特征 | 典型修法 |
|---|---|---|
| N+1 查询 | 循环里逐行查库 | 批量查询 + 内存关联 |
| 循环内重复计算 | 热点函数在循环里做重活 | 提到循环外、加缓存 |
| 长 SQL | EXPLAIN 显示全表扫描 | 加索引、改写查询 |
| 内存泄漏 | 内存随时间线性涨 | 找引用未释放的对象 |
| 序列化瓶颈 | 大 JSON 反复解析 | 减少体积、流式处理 |
| 锁竞争 | 等待时间长 | 缩小临界区、读写分离 |

## 基线怎么建

1. 固定环境(机器、数据量、并发);
2. 固定请求(同一接口、同一参数);
3. 预热后跑 3-5 次取中位数;
4. 记录:环境、命令、结果,方便复现。

没有基线的优化报告不算数。
