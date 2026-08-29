# Changelog

## 未发布

### 仓库

- 新增 Windows 一键安装脚本(install.ps1),自动检测已装 Agent 并安装
- 修正 OpenCode 全局技能目录,统一为 ~/.config/opencode/skills

### 技能深化

- skill-style-guide:新增风格检查脚本 style_checker.py 与判断标准参考 REVIEW_GUIDE.md

## v0.7.0(2026-08-29)

技能数量:22,其中 16 个带可执行脚本或示例,18 个带参考资料。

### 技能深化

- tdd-workflow:新增可运行的密码校验器红绿重构示例(pytest,6 用例)
- code-reviewer:新增审查辅助脚本,标记硬编码密钥、裸 except、调试输出等
- api-tester:新增登录接口契约测试示例(自动起停服务,5 用例)
- security-reviewer:新增安全扫描脚本,覆盖注入、密钥、路径穿越等 8 类模式
- performance-profiler:新增基准测量脚本(p50/p95/p99/QPS)与慢接口示例
- bug-diagnoser:新增堆栈解析脚本,提取异常类型与调用链
- log-analysis:新增日志关联脚本,按 trace_id 跨服务串日志
- dev-env-troubleshooter:新增端口占用检查脚本(Windows/macOS/Linux)
- git-workflow:新增提交历史统计脚本与命令速查
- db-schema-designer:新增命名规范检查脚本与命名/索引参考
- ci-cd-setup:新增工作流配置检查脚本与常见问题参考
- db-migration-reviewer:新增迁移模板生成器与数据库差异参考
- cache-governor:新增缓存 key 扫描脚本与三类故障防御参考
- commit-message-writer:新增提交信息草稿生成脚本
- frontend-debug:新增 DevTools 数据提取脚本与面板速查
- code-migrator:新增迁移检查清单生成器与策略参考

### 仓库

- README 中英文版重写,补充技能结构说明与项目徽章
- 技能质量标准写入 skill-creator-cn 与风格指南
- CI 增加 Python 脚本语法检查
- 清理误提交的缓存文件,gitignore 补充 __pycache__

## v0.6.0(2026-08-29)

- 新增代码迁移、缓存治理技能,技能总数 22
- README 技能列表补齐

## v0.5.0(2026-08-29)

- 新增日志分析、前端调试技能,技能总数 20

## v0.4.0(2026-08-29)

- 新增安全评审、性能剖析、数据库表结构设计技能,技能总数 18

## v0.3.0(2026-08-29)

- 新增数据库迁移评审、本地环境排障技能,技能总数 15

## v0.2.0(2026-08-29)

- 新增 API 契约测试、CI/CD 搭建、自然中文写作技能,技能总数 13

## v0.1.0(2026-08-29)

- 初始版本:10 个核心技能,仓库结构,CI 校验
