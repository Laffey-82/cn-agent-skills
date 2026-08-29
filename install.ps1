<#
.SYNOPSIS
  cn-agent-skills 一键安装脚本(Windows PowerShell)

.DESCRIPTION
  检测本机已安装的 Agent,把 skills/ 复制到对应的技能目录。
  支持 Claude Code、Codex、Cursor、TRAE、OpenCode。

.PARAMETER Agent
  只安装到指定的 Agent。可选值:claude、codex、cursor、trae、opencode。

.PARAMETER BaseDir
  技能安装根目录,默认取当前用户主目录。一般不用改。

.PARAMETER DryRun
  只打印将要安装的位置,不实际复制。

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File install.ps1

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File install.ps1 -Agent codex
#>
[CmdletBinding()]
param(
  [string]$Agent = "",
  [string]$BaseDir = $HOME,
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$RepoDir = $PSScriptRoot
$SkillsSrc = Join-Path $RepoDir "skills"

if (-not (Test-Path $SkillsSrc)) {
  Write-Error "未找到 skills/ 目录,请在仓库根目录运行本脚本。"
  exit 1
}

$AgentDirs = [ordered]@{
  claude   = @{ Name = "Claude Code"; Cmd = "claude";   Path = Join-Path $BaseDir ".claude\skills" }
  codex    = @{ Name = "Codex";       Cmd = "codex";    Path = Join-Path $BaseDir ".codex\skills" }
  cursor   = @{ Name = "Cursor";      Cmd = "cursor";   Path = Join-Path $BaseDir ".cursor\skills" }
  trae     = @{ Name = "TRAE";        Cmd = "trae";     Path = Join-Path $BaseDir ".trae\skills" }
  opencode = @{ Name = "OpenCode";    Cmd = "opencode"; Path = Join-Path $BaseDir ".config\opencode\skills" }
}

$installed = 0

foreach ($key in $AgentDirs.Keys) {
  $info = $AgentDirs[$key]
  if ($Agent -ne "" -and $Agent -ne $key) { continue }
  if (-not (Get-Command $info.Cmd -ErrorAction SilentlyContinue)) { continue }

  $dest = $info.Path
  if ($DryRun) {
    Write-Host "[预览] $($info.Name):将安装到 $dest"
    $installed++
    continue
  }

  if (-not (Test-Path $dest)) {
    New-Item -ItemType Directory -Path $dest -Force | Out-Null
  }
  Copy-Item -Path (Join-Path $SkillsSrc "*") -Destination $dest -Recurse -Force
  Write-Host "[OK] $($info.Name):已安装到 $dest"
  $installed++
}

Write-Host ""

if ($DryRun) {
  if ($installed -eq 0) {
    Write-Host "没有检测到已安装的 Agent,或指定 Agent 不在 PATH 中。"
  } else {
    Write-Host "以上是准备安装的位置,未执行任何复制。"
  }
  exit 0
}

if ($installed -eq 0) {
  Write-Host "没有检测到已安装的 Agent。如果工具不在 PATH 里,请手动复制:" -ForegroundColor Yellow
  Write-Host "  Copy-Item -Path .\skills\* -Destination $HOME\.claude\skills -Recurse -Force"
  Write-Host "  Copy-Item -Path .\skills\* -Destination $HOME\.codex\skills -Recurse -Force"
  Write-Host "  Copy-Item -Path .\skills\* -Destination $HOME\.cursor\skills -Recurse -Force"
  Write-Host "  Copy-Item -Path .\skills\* -Destination $HOME\.trae\skills -Recurse -Force"
  Write-Host "  Copy-Item -Path .\skills\* -Destination $HOME\.config\opencode\skills -Recurse -Force"
  exit 0
}

Write-Host "安装完成,重启 Agent 后技能生效。"
Write-Host "也可以直接用 gh skill install Laffey-82/cn-agent-skills 安装到指定 Agent。"
