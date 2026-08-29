"""任务清单检查脚本:检查任务拆解表的结构问题。

用法:
    python task_checker.py <任务清单.md>

检查项:
- 是否包含任务表格,必需列是否齐全(任务/依赖/交付物/验收标准);
- 任务编号是否重复;
- 依赖是否引用不存在的任务编号、是否自依赖;
- 依赖关系是否有环;
- 验收标准是否为空或含糊;
- 是否残留占位符。

脚本只做标记,结论需要人确认。模板见 references/DECOMPOSE_TEMPLATE.md。
"""

import argparse
import re
import sys
from pathlib import Path

REQUIRED_COLUMNS = ["任务", "依赖", "交付物", "验收标准"]
FENCE_RE = re.compile(r"^\s*```")
VAGUE_RE = re.compile(r"(做好就行|完成功能|能跑|没问题|差不多|之后再说)")
PLACEHOLDER_RE = re.compile(r"(TODO|TBD|待补充|【[^】]*】)")


def in_fence(lines: list[str], idx: int) -> bool:
    count = 0
    for line in lines[: idx + 1]:
        if FENCE_RE.match(line):
            count += 1
    return count % 2 == 1


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(line: str) -> bool:
    cells = split_row(line)
    return bool(cells) and all(re.fullmatch(r":?-+:?", cell.strip()) for cell in cells)


def parse_tables(lines: list[str]) -> list[tuple[int, list[str], list[tuple[int, list[str]]]]]:
    """返回 [(表头行号, 表头, [(数据行号, 单元格)])]"""
    tables = []
    i = 0
    while i < len(lines):
        if i + 1 >= len(lines):
            i += 1
            continue
        if not in_fence(lines, i) and lines[i].strip().startswith("|") and is_separator(lines[i + 1]):
            header = split_row(lines[i])
            rows = []
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append((j + 1, split_row(lines[j])))
                j += 1
            tables.append((i + 1, header, rows))
            i = j
            continue
        i += 1
    return tables


def find_cycle(edges: dict[int, list[int]]) -> list[int] | None:
    """返回依赖环的路径,没有环返回 None。"""
    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[int, int] = {}

    def dfs(node: int, path: list[int]) -> list[int] | None:
        color[node] = GRAY
        path.append(node)
        for nxt in edges.get(node, []):
            if color.get(nxt, WHITE) == GRAY:
                start = path.index(nxt)
                return path[start:] + [nxt]
            if color.get(nxt, WHITE) == WHITE:
                result = dfs(nxt, path)
                if result:
                    return result
        path.pop()
        color[node] = BLACK
        return None

    for node in edges:
        if color.get(node, WHITE) == WHITE:
            result = dfs(node, [])
            if result:
                return result
    return None


def check_tasks(path: Path) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        findings.append((0, "必须", f"无法读取文件:{path}"))
        return findings

    tables = parse_tables(lines)
    if not tables:
        findings.append((0, "必须", "未找到任务表格(应为 Markdown 表格)"))
        return findings

    for header_lineno, header, rows in tables:
        col_index = {name: header.index(name) for name in header if name in REQUIRED_COLUMNS}
        for name in REQUIRED_COLUMNS:
            if name not in col_index:
                findings.append((header_lineno, "必须", f"缺少必需列 '{name}'"))
        if "预估" not in header:
            findings.append((header_lineno, "建议", "建议补'预估'列,方便排期"))

        ids: dict[int, tuple[int, list[str]]] = {}
        for lineno, cells in rows:
            if len(cells) < len(header):
                cells = cells + [""] * (len(header) - len(cells))
            try:
                task_id = int(cells[col_index["#"]]) if "#" in col_index else int(cells[0])
            except (ValueError, IndexError):
                findings.append((lineno, "必须", "任务编号应为数字"))
                continue

            if task_id in ids:
                findings.append((lineno, "必须", f"任务编号 {task_id} 重复"))
                continue
            ids[task_id] = (lineno, cells)

        for task_id, (lineno, cells) in ids.items():
            accept = cells[col_index["验收标准"]] if "验收标准" in col_index else ""
            if not accept:
                findings.append((lineno, "必须", f"任务 {task_id} 缺验收标准"))
            elif VAGUE_RE.search(accept):
                findings.append((lineno, "建议", f"任务 {task_id} 验收标准含糊,换成可验证表述"))

            if "依赖" in col_index:
                deps = cells[col_index["依赖"]]
                for token in re.split(r"[,、\s]+", deps):
                    if not token or token == "-":
                        continue
                    try:
                        dep_id = int(token)
                    except ValueError:
                        findings.append((lineno, "必须", f"任务 {task_id} 的依赖 '{token}' 不是任务编号"))
                        continue
                    if dep_id == task_id:
                        findings.append((lineno, "必须", f"任务 {task_id} 不能依赖自己"))
                    elif dep_id not in ids:
                        findings.append((lineno, "必须", f"任务 {task_id} 依赖不存在的任务 {dep_id}"))

            for cell in cells:
                if PLACEHOLDER_RE.search(cell):
                    findings.append((lineno, "建议", f"任务 {task_id} 残留占位符,确认是否已填"))
                    break

        edges = {}
        for task_id, (lineno, cells) in ids.items():
            if "依赖" not in col_index or col_index["依赖"] >= len(cells):
                continue
            deps = []
            for token in re.split(r"[,、\s]+", cells[col_index["依赖"]]):
                if token and token != "-":
                    try:
                        deps.append(int(token))
                    except ValueError:
                        pass
            edges[task_id] = deps

        cycle = find_cycle(edges)
        if cycle:
            chain = " → ".join(str(t) for t in cycle)
            findings.append((header_lineno, "必须", f"依赖存在环:{chain}"))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="任务清单检查")
    parser.add_argument("files", nargs="+", help="任务清单 Markdown 文件")
    args = parser.parse_args()

    total = 0
    for file_arg in args.files:
        path = Path(file_arg)
        findings = check_tasks(path)
        must = sum(1 for _, level, _ in findings if level == "必须")
        suggest = len(findings) - must
        total += len(findings)

        print(f"\n== {path} ==")
        if not findings:
            print("  未发现问题")
            continue
        for lineno, level, note in findings:
            loc = f"L{lineno}" if lineno else "结构"
            print(f"  {loc:<6} [{level}] {note}")
        verdict = "不通过" if must else ("修改后通过" if suggest else "通过")
        print(f"  结论:{verdict}(必须 {must} 项,建议 {suggest} 项)")

    print(f"\n共检查 {len(args.files)} 个清单,标记 {total} 项。请逐条人工确认后再开工。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
