# 性能基准示例

一个故意慢的接口(`sleep 0.05`),配合 [scripts/benchmark.py](../scripts/benchmark.py) 演示"先建基线再优化"。

## 运行

```bash
# 终端 1:启动示例服务
python app.py

# 终端 2:跑基准
python ../scripts/benchmark.py http://127.0.0.1:8001/api/items 100 10
```

## 预期

p50 接近 50ms(接口的 sleep 时长)。优化方向:去掉 sleep、加缓存、并行化。

## 怎么用基线

1. 优化前跑一次,记录 p50/p95/p99;
2. 改代码;
3. 用同样的命令再跑一次;
4. 对比两次数字,有提升才算有效。
