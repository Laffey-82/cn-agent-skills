---
name: sql-reviewer
description: SQL 审查。扫描 SQL 文件中的常见反模式:高危操作缺 WHERE、SELECT *、前导通配 LIKE、列上套函数、隐式连接、NOT IN 子查询等,只做标记,索引类结论看执行计划。Use to review SQL for common anti-patterns and risky operations.
license: MIT
metadata:
  version: "1.0.0"
---

# SQL 审查

## 何时使用

- 用户说"帮我看下这条 SQL""审一下这个脚本";
- 上线前检查存量 SQL,担心性能或误操作;
- 排查慢查询,先快速扫一遍反模式;
- 数据库脚本迁移、批量执行的 SQL 文件。

## 使用步骤

### 第 1 步:拿到要审的 SQL

- 单个文件、整个目录的 .sql,或粘贴的语句;
- 说明数据库类型(MySQL/PostgreSQL/Oracle 等),影响部分判断;
- 说明用途:线上跑的、迁移脚本、还是临时排查。

### 第 2 步:跑脚本标记

命令见下面的[辅助脚本](#辅助脚本)。脚本按常见反模式标记,分两级:

| 级别 | 范围 |
|---|---|
| 必须 | UPDATE/DELETE 缺 WHERE、DROP/TRUNCATE 等高危操作 |
| 建议 | SELECT *、前导通配 LIKE、列上套函数、隐式连接、NOT IN 子查询、INSERT...SELECT 缺列名、SELECT 缺 LIMIT |

### 第 3 步:人工确认每条标记

- **高危操作先拦**:缺 WHERE 的 UPDATE/DELETE 必须补条件或确认有备份;
- **性能类先看执行计划**:脚本只提示"可能失效",别直接改,跑 EXPLAIN 确认;
- 小表上的全表扫描可能没问题,别为改而改;
- NOT IN 子查询重点核对 NULL 语义,这是正确性问题不是性能问题。

### 第 4 步:输出审查结论

```markdown
# SQL 审查报告:<文件>

## 高危(必须处理)
## 建议(结合执行计划判断)
## 结论
通过 / 修改后通过 / 不通过
```

每条结论给出"现象 → 影响 → 建议",拿不准的标注"需进一步确认"。

## 输入与输出

- 输入:SQL 文件或语句 + 数据库类型(可选)+ 用途;
- 输出:反模式清单 + 人工确认后的审查报告。

## 示例

**脚本标记(节选):**

```text
L13  [必须] UPDATE 没有 WHERE,会全表更新
L5   [建议] LIKE 前导通配符(以 % 开头),索引会失效
```

**审查结论节选:**

```markdown
## 高危
- L13 UPDATE users SET status = 0 缺 WHERE,补条件或确认仅更新目标行
## 建议
- L5 message LIKE '%error%' 索引失效,改为前缀匹配或加全文索引(先看执行计划)
```

## 辅助脚本

[scripts/sql_reviewer.py](scripts/sql_reviewer.py) 扫描 SQL 文件,标记常见反模式:

```bash
# 扫描整个目录的 .sql
python skills/sql-reviewer/scripts/sql_reviewer.py <目录或文件>

# strict 模式:有"必须"级问题就非零退出
python skills/sql-reviewer/scripts/sql_reviewer.py <文件> --strict
```

脚本只做标记,结论需要人确认;涉及索引和性能的,先看执行计划再下。

## 注意事项

- **静态扫描不等于结论**:标记"可能失效"≠"一定失效",执行计划说了算;
- **高危操作别直接执行**:缺 WHERE 的 UPDATE/DELETE 先补条件,确认影响行数;
- 注释里的 SQL 不算,脚本已忽略注释;
- 和 [security-reviewer](../security-reviewer/SKILL.md) 分工:注入、越权归它,性能和正确性归本技能。

## 不适用场景

- 需要的是数据库表结构设计(用 db-schema-designer);
- 需要的是迁移脚本评审(用 db-migration-reviewer);
- 只问安全漏洞,不关心性能。

## 验证方式

1. 触发:"审一下这条 SQL";
2. 跑脚本:sql_reviewer.py 输出与人工抽查一致;
3. 走查:每条"必须"都有处理结论(补 WHERE / 确认影响);
4. 确认:性能类建议都有执行计划依据。
