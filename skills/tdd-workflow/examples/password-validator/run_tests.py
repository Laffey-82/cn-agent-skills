"""一键运行 TDD 示例测试。"""

import subprocess
import sys


def main() -> int:
    result = subprocess.run([sys.executable, "-m", "pytest", "test", "-q"])
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
