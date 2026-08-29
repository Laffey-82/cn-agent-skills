"""api-tester 技能示例:基于真实契约生成并执行测试。

运行:
    python test_api.py
"""

import subprocess
import sys
import time

import requests

BASE = "http://127.0.0.1:8000"


CASES = [
    # (场景, 请求体, 预期状态码, 说明)
    ("正常登录", {"username": "admin", "password": "correct-password"}, 200, "返回 token"),
    ("密码错误", {"username": "admin", "password": "wrong"}, 401, "账号或密码错误"),
    ("账号不存在", {"username": "nobody", "password": "x"}, 401, "不暴露账号是否存在"),
    ("缺少密码", {"username": "admin"}, 400, "必填校验"),
    ("空请求体", None, 400, "空 body 处理"),
]


def run_cases():
    failed = []
    for name, payload, expected, note in CASES:
        try:
            resp = requests.post(f"{BASE}/api/login", json=payload, timeout=3)
            actual = resp.status_code
            ok = actual == expected
            print(f"[{'PASS' if ok else 'FAIL'}] {name}: 期望 {expected},实际 {actual} ({note})")
            if not ok:
                failed.append(name)
        except requests.RequestException as exc:
            print(f"[ERROR] {name}: 请求失败 {exc}")
            failed.append(name)
    return failed


def main():
    server = subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        time.sleep(1.5)
        failed = run_cases()
        print(f"\n共 {len(CASES)} 个用例,失败 {len(failed)} 个")
        if failed:
            print("失败用例:", ", ".join(failed))
            return 1
        return 0
    finally:
        server.terminate()
        server.wait()


if __name__ == "__main__":
    raise SystemExit(main())
