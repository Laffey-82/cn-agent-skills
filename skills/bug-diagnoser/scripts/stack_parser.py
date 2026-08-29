"""堆栈解析辅助脚本:从报错文本中提取调用链与关键信息。

用法:
    python stack_parser.py <报错文件>
    cat error.log | python stack_parser.py

只做提取,结论需要人确认。
"""

import fileinput
import re
import sys

FRAME_RE = re.compile(r'^\s*File "([^"]+)", line (\d+), in (\S+)')
ERROR_RE = re.compile(r'^(\w+(?:\.\w+)*(?:Error|Exception)):?\s?(.*)$')


def parse(text: str) -> dict:
    frames = []
    error_type = ""
    error_msg = ""
    for line in text.splitlines():
        m = FRAME_RE.match(line)
        if m:
            frames.append({"file": m.group(1), "line": int(m.group(2)), "func": m.group(3)})
            continue
        m = ERROR_RE.match(line)
        if m and not error_type:
            error_type = m.group(1)
            error_msg = m.group(2)
    return {"frames": frames, "error_type": error_type, "error_msg": error_msg}


def main() -> int:
    text = "".join(fileinput.input())
    result = parse(text)

    print("== 异常类型 ==")
    print(result["error_type"] or "(未识别)")
    print("== 错误信息 ==")
    print(result["error_msg"] or "(未识别)")
    print("== 调用链(从外层到内层) ==")
    if not result["frames"]:
        print("(未解析到堆栈帧)")
    for i, frame in enumerate(result["frames"], 1):
        marker = "  <- 可能是根因" if i == len(result["frames"]) else ""
        print(f"  {i}. {frame['file']}:{frame['line']} in {frame['func']}{marker}")

    print("\n提示:最后一行是异常抛出点,先看它,再沿调用链往上找谁传了问题数据。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
