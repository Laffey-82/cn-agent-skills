"""DevTools 数据提取脚本:从 HAR 文件或 Console 导出文本中提取调试信息。

用法:
    python devtools_extract.py <har文件> [--errors-only]
    python devtools_extract.py <console导出.txt>

输出:失败请求、4xx/5xx、慢请求、Console 错误。
"""

import argparse
import json
import re
import sys
from pathlib import Path


def scan_har(path: Path, errors_only: bool) -> int:
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"HAR 解析失败:{exc}")
        return 1

    entries = data.get("log", {}).get("entries", [])
    issues = 0
    slow = []
    for entry in entries:
        req = entry.get("request", {})
        resp = entry.get("response", {})
        url = req.get("url", "")
        status = resp.get("status", 0)
        duration = entry.get("time", 0)
        if status >= 400:
            print(f"[{status}] {url}")
            issues += 1
        elif status == 0:
            print(f"[网络错误] {url}")
            issues += 1
        if duration > 1000:
            slow.append((url, duration))
        if errors_only and status == 0 and resp.get("_error"):
            print(f"[{resp['_error']}] {url}")
            issues += 1

    if slow:
        print(f"\n== 慢请求(>1s,共 {len(slow)} 个)==")
        for url, duration in sorted(slow, key=lambda x: -x[1])[:10]:
            print(f"  {duration:.0f}ms {url}")
    print(f"\n失败/异常请求 {issues} 个,HAR 共 {len(entries)} 条。")
    return 0


def scan_console(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    errors = [line for line in text.splitlines() if re.search(r"\b(error|exception|failed)\b", line, re.IGNORECASE)]
    print(f"== Console 疑似错误(共 {len(errors)} 条)==")
    for line in errors[:50]:
        print(f"  {line.strip()[:200]}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="DevTools 数据提取")
    parser.add_argument("file", help="HAR 文件或 Console 导出文本")
    parser.add_argument("--errors-only", action="store_true", help="HAR 只输出错误请求")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"文件不存在:{path}")
        return 1
    is_har = path.suffix.lower() in {".har", ".json"}
    if is_har and path.suffix.lower() == ".json":
        try:
            json.loads(path.read_text(encoding="utf-8", errors="replace"))
            is_har = True
        except json.JSONDecodeError:
            is_har = False
    if is_har:
        return scan_har(path, args.errors_only)
    return scan_console(path)


if __name__ == "__main__":
    raise SystemExit(main())
