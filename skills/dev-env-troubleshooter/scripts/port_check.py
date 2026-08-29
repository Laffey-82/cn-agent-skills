"""端口检查辅助脚本:查看指定端口是否被占用、被谁占用。

用法:
    python port_check.py 8080
    python port_check.py 3000 5173 8000
"""

import argparse
import re
import subprocess
import sys


def check_windows(port: int) -> str | None:
    result = subprocess.run(
        ["netstat", "-ano"], capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    for line in result.stdout.splitlines():
        if f":{port}" in line and "LISTENING" in line:
            parts = line.split()
            pid = parts[-1]
            return f"端口 {port} 被 PID {pid} 占用:{line.strip()}"
    return None


def check_posix(port: int) -> str | None:
    result = subprocess.run(
        ["lsof", "-i", f":{port}"], capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if result.returncode == 0 and result.stdout.strip():
        return f"端口 {port} 被占用:\n{result.stdout.strip()}"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="端口占用检查")
    parser.add_argument("ports", type=int, nargs="+", help="要检查的端口")
    args = parser.parse_args()

    is_windows = sys.platform.startswith("win")
    found = 0
    for port in args.ports:
        info = check_windows(port) if is_windows else check_posix(port)
        if info:
            print(info)
            found += 1
        else:
            print(f"端口 {port} 空闲")

    if found:
        print(f"\n发现 {found} 个端口被占用。确认占用进程是否还在用,再决定结束它或换端口。")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
