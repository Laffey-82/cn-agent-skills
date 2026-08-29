"""技能风格检查脚本:按 cn-agent-skills 风格约定扫描技能,标记问题位置。

用法:
    python style_checker.py                  # 扫描仓库全部技能
    python style_checker.py api-tester       # 只检查指定技能(名字或目录)
    python style_checker.py --repo <仓库根目录>

脚本只做"标记",问题是否成立、要不要改,由人确认。
判断依据见 ../references/REVIEW_GUIDE.md 和仓库 docs/STYLE_GUIDE.md。
"""

import argparse
import re
import sys
from pathlib import Path

MAX_LINES = 500
REQUIRED_SECTIONS = ["验证方式"]
RECOMMENDED_SECTIONS = ["何时使用", "不适用场景"]

NAME_RE = re.compile(r"^[a-z][a-z0-9-]*$")
GENERIC_DESC_RE = re.compile(
    r"(帮助(用户|开发者|你)|提供(专业|全面|优质|高效)的?(帮助|支持|服务)|"
    r"提升(开发|工作|学习)?效率)"
)
VAGUE_RE = re.compile(
    r"(认真(分析|检查|思考|审查|排查)|仔细(分析|检查|核对|排查)|"
    r"进一步(分析|优化|完善|提升|处理)|更好地|更加(高效|完善|好用|方便)|"
    r"综上所述|总而言之)"
)
EMOJI_RE = re.compile(r"[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F]")
FENCE_RE = re.compile(r"^\s*```")
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
CJK_RE = re.compile(r"[\u4e00-\u9fff]")
QUOTED_RE = re.compile(r'"[^"\n]*"|\'[^\'\n]*\'|“[^”\n]*”|「[^」\n]*」')


def strip_quoted(line: str) -> str:
    """去掉引号内的内容,引号里的往往是引用示例,不参与表述检查。"""
    return QUOTED_RE.sub("", line)


def read_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []


def parse_frontmatter(lines: list[str]) -> tuple[dict[str, str], int]:
    """解析开头的 --- 块,返回 (字段字典, frontmatter 结束行号)。"""
    if not lines or lines[0].strip() != "---":
        return {}, 0
    fm: dict[str, str] = {}
    i = 1
    while i < len(lines) and lines[i].strip() != "---":
        line = lines[i]
        m = re.match(r"^([A-Za-z][A-Za-z0-9_-]*)\s*:\s*(.*)$", line)
        if m:
            key, value = m.group(1), m.group(2).strip()
            fm[key] = value.strip('"').strip("'")
        elif re.match(r"^\s+version\s*:\s*", line):
            fm["version"] = "存在"
        i += 1
    if i >= len(lines):
        return {}, 0
    return fm, i


def sections_of(lines: list[str]) -> set[str]:
    found = set()
    for line in lines:
        m = HEADING_RE.match(line)
        if m:
            found.add(m.group(1).strip())
    return found


def check_skill(skill_dir: Path) -> tuple[list[tuple[int, str, str]], int]:
    """返回 (问题列表, 检查出的行数)。问题格式:(行号, 级别, 说明)。"""
    findings: list[tuple[int, str, str]] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        findings.append((0, "必须", "缺少 SKILL.md"))
        return findings, 0

    lines = read_lines(skill_md)
    name = skill_dir.name

    if not NAME_RE.match(name):
        findings.append((0, "必须", f"目录名 '{name}' 应小写、连字符、以字母开头"))

    fm, _ = parse_frontmatter(lines)
    fm_name = fm.get("name", "")
    if not fm_name:
        findings.append((0, "必须", "frontmatter 缺少 name"))
    elif fm_name != name:
        findings.append((0, "必须", f"frontmatter name '{fm_name}' 与目录名 '{name}' 不一致"))

    desc = fm.get("description", "")
    if not desc:
        findings.append((0, "必须", "frontmatter 缺少 description(写清做什么 + 何时触发)"))
    else:
        if not (1 <= len(desc) <= 1024):
            findings.append((0, "必须", f"description 长度 {len(desc)},应在 1-1024 之间"))
        if GENERIC_DESC_RE.search(desc):
            findings.append((0, "建议", "description 疑似空泛描述,应写具体场景而非套话"))
        if not CJK_RE.search(desc):
            findings.append((0, "建议", "description 建议以中文为主"))
        if not re.search(r"[A-Za-z]", desc):
            findings.append((0, "建议", "description 建议带英文关键词,方便检索"))

    if "license" not in fm:
        findings.append((0, "建议", "frontmatter 建议补 license"))
    if "metadata" not in fm:
        findings.append((0, "建议", "frontmatter 建议补 metadata.version"))
    elif "version" not in fm:
        findings.append((0, "建议", "metadata 里建议写明 version"))

    if len(lines) > MAX_LINES:
        findings.append((0, "必须", f"SKILL.md {len(lines)} 行,超过 {MAX_LINES} 行上限,内容拆到 references/"))

    sections = sections_of(lines)
    for sec in REQUIRED_SECTIONS:
        if sec not in sections:
            findings.append((0, "必须", f"缺少章节 '## {sec}'"))
    for sec in RECOMMENDED_SECTIONS:
        if sec not in sections:
            findings.append((0, "建议", f"建议补章节 '## {sec}',避免误触发或缺少产出说明"))

    fence_count = 0
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            fence_count += 1
        plain = strip_quoted(line)
        if VAGUE_RE.search(plain) and len(findings) < 40:
            findings.append((i, "建议", "疑似空泛表述,请确认是否具体到可执行"))
        emojis = EMOJI_RE.findall(plain)
        if emojis and not line.strip().startswith("|"):
            if line.startswith("#") or len(emojis) >= 3:
                findings.append((i, "建议", "标题或连续 emoji,与仓库文案风格不符"))

    if fence_count % 2 == 1:
        findings.append((0, "必须", f"代码围栏数量为奇数({fence_count}),Markdown 会渲染错乱"))

    return findings, len(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="技能风格检查")
    parser.add_argument("skills", nargs="*", help="技能名或技能目录,默认扫描全部")
    parser.add_argument("--repo", default=None, help="仓库根目录,默认取脚本所在仓库")
    args = parser.parse_args()

    repo = Path(args.repo) if args.repo else Path(__file__).resolve().parents[3]
    skills_dir = repo / "skills"
    if not skills_dir.is_dir():
        print(f"未找到技能目录:{skills_dir}")
        return 1

    if args.skills:
        targets: list[Path] = []
        for item in args.skills:
            p = Path(item)
            if p.is_dir():
                targets.append(p)
            else:
                targets.append(skills_dir / item)
        targets = [t for t in targets if t.is_dir()]
    else:
        targets = sorted(skills_dir.iterdir())

    total_must = 0
    total_suggest = 0
    checked = 0

    for target in targets:
        if not target.is_dir():
            continue
        if not (target / "SKILL.md").exists():
            print(f"\n== {target.name} ==\n  L0 [必须] 缺少 SKILL.md")
            total_must += 1
            checked += 1
            continue
        findings, line_count = check_skill(target)
        checked += 1
        must = sum(1 for _, level, _ in findings if level == "必须")
        suggest = len(findings) - must
        total_must += must
        total_suggest += suggest

        print(f"\n== {target.name}({line_count} 行)==")
        if not findings:
            print("  未发现问题")
            continue
        for lineno, level, note in findings:
            loc = f"L{lineno}" if lineno else "结构"
            print(f"  {loc:<6} [{level}] {note}")
        verdict = "不通过" if must else ("修改后通过" if suggest else "通过")
        print(f"  结论:{verdict}(必须 {must} 项,建议 {suggest} 项)")

    print(f"\n共检查 {checked} 个技能,标记 {total_must + total_suggest} 项"
          f"(必须 {total_must} 项,建议 {total_suggest} 项)。")
    print("脚本只做标记,请逐条对照 references/REVIEW_GUIDE.md 人工确认。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
