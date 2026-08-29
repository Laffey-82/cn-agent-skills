#!/usr/bin/env bash
#
# cn-agent-skills 一键安装脚本
# 自动检测本机已安装的 Agent,并把 skills/ 复制到对应技能目录。
# 用法:
#   curl -fsSL https://raw.githubusercontent.com/<owner>/cn-agent-skills/main/install.sh | bash
#   bash install.sh                     # 安装到所有检测到的 Agent
#   bash install.sh --agent codex       # 仅安装到指定 Agent
#

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="${REPO_DIR}/skills"

if [ ! -d "${SKILLS_SRC}" ]; then
  echo "[错误] 未找到 skills/ 目录,请在仓库根目录运行本脚本。" >&2
  exit 1
fi

AGENT_FILTER=""
if [ "${1:-}" = "--agent" ] && [ -n "${2:-}" ]; then
  AGENT_FILTER="$2"
fi

install_to() {
  local agent="$1"
  local dest="$2"
  if [ -n "${AGENT_FILTER}" ] && [ "${AGENT_FILTER}" != "${agent}" ]; then
    return
  fi
  if [ ! -d "${dest}" ]; then
    mkdir -p "${dest}"
  fi
  cp -R "${SKILLS_SRC}"/* "${dest}/"
  echo "[OK] ${agent}: 已安装到 ${dest}"
}

detect_and_install() {
  # Claude Code
  if command -v claude >/dev/null 2>&1; then
    install_to "claude" "${HOME}/.claude/skills"
  fi

  # Codex CLI
  if command -v codex >/dev/null 2>&1; then
    install_to "codex" "${HOME}/.codex/skills"
  fi

  # Cursor
  if command -v cursor >/dev/null 2>&1; then
    install_to "cursor" "${HOME}/.cursor/skills"
  fi

  # TRAE
  if command -v trae >/dev/null 2>&1; then
    install_to "trae" "${HOME}/.trae/skills"
  fi

  # OpenCode
  if command -v opencode >/dev/null 2>&1; then
    install_to "opencode" "${HOME}/.config/opencode/skills"
  fi
}

detect_and_install

echo ""
echo "安装完成。如果某些 Agent 未检测到,请手动复制:"
echo "  cp -R ${SKILLS_SRC}/* ~/.claude/skills/"
echo "  cp -R ${SKILLS_SRC}/* ~/.codex/skills/"
echo "  cp -R ${SKILLS_SRC}/* ~/.cursor/skills/"
echo "  cp -R ${SKILLS_SRC}/* ~/.trae/skills/"
echo "  cp -R ${SKILLS_SRC}/* ~/.config/opencode/skills/"
echo ""
echo "重启你的 Agent 后,技能即生效。仓库发布到 GitHub 后,也推荐用:"
echo "  gh skill install <owner>/cn-agent-skills"
