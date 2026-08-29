"""接口性能基准脚本:测量 p50/p95/p99 耗时与成功率。

用法:
    python benchmark.py <URL> [请求次数] [并发]

示例:
    python benchmark.py http://127.0.0.1:8000/api/login 100 10
"""

import argparse
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import requests


def hit_once(url: str) -> tuple[int, float, bool]:
    start = time.perf_counter()
    try:
        resp = requests.get(url, timeout=10)
        ok = 200 <= resp.status_code < 500
        return resp.status_code, (time.perf_counter() - start) * 1000, ok
    except requests.RequestException:
        return 0, (time.perf_counter() - start) * 1000, False


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    idx = min(len(values) - 1, int(len(values) * p))
    return values[idx]


def main() -> int:
    parser = argparse.ArgumentParser(description="接口基准")
    parser.add_argument("url")
    parser.add_argument("count", nargs="?", type=int, default=50)
    parser.add_argument("concurrency", nargs="?", type=int, default=5)
    args = parser.parse_args()

    # 预热 5 次,排除冷启动
    for _ in range(5):
        hit_once(args.url)

    latencies: list[float] = []
    ok_count = 0
    statuses: dict[int, int] = {}
    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        for status, ms, ok in pool.map(lambda _: hit_once(args.url), range(args.count)):
            latencies.append(ms)
            if ok:
                ok_count += 1
            statuses[status] = statuses.get(status, 0) + 1

    elapsed = time.perf_counter() - start
    print("== 基准结果 ==")
    print(f"目标: {args.url}")
    print(f"请求数: {args.count},并发: {args.concurrency},总耗时: {elapsed:.2f}s")
    print(f"成功率: {ok_count}/{args.count} ({ok_count / args.count * 100:.1f}%)")
    print(f"QPS: {args.count / elapsed:.1f}")
    print(f"p50: {percentile(latencies, 0.50):.1f}ms")
    print(f"p95: {percentile(latencies, 0.95):.1f}ms")
    print(f"p99: {percentile(latencies, 0.99):.1f}ms")
    print(f"最慢: {max(latencies):.1f}ms")
    print(f"状态码分布: {statuses}")

    if ok_count < args.count:
        print("提示:存在失败请求,先确认服务状态再谈优化。")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
