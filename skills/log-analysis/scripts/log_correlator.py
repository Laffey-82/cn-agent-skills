"""日志关联辅助脚本:按关联字段(如 request_id / trace_id)把分散日志串起来。

用法:
    python log_correlator.py <日志文件> --field trace_id --value abc123
    cat app.log | python log_correlator.py --field trace_id --value abc123

支持纯文本行(正则提取)和 JSON 行。
"""

import argparse
import fileinput
import json
import re
import sys


def extract_value(line: str, field: str) -> str | None:
    line = line.strip()
    if line.startswith("{"):
        try:
            obj = json.loads(line)
            if isinstance(obj, dict) and field in obj:
                return str(obj[field])
        except json.JSONDecodeError:
            pass
    m = re.search(rf"{re.escape(field)}[=:]\s*([A-Za-z0-9_\-]+)", line)
    return m.group(1) if m else None


def main() -> int:
    parser = argparse.ArgumentParser(description="日志关联")
    parser.add_argument("files", nargs="*", help="日志文件,不填则读 stdin")
    parser.add_argument("--field", required=True, help="关联字段名,如 trace_id")
    parser.add_argument("--value", required=True, help="关联字段值")
    args = parser.parse_args()

    matches = []
    for line in fileinput.input(args.files):
        if extract_value(line, args.field) == args.value:
            matches.append(line.rstrip())

    print(f"== 字段 {args.field} = {args.value} 的日志(共 {len(matches)} 条)==")
    for line in matches:
        print(line)

    if not matches:
        print("没有匹配。检查:字段名是否拼错?日志是否跨文件?时间范围对吗?")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
