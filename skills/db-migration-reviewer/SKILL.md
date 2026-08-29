---
name: db-migration-reviewer
description: "数据库迁移评审。审查迁移脚本的安全性、可回滚性、锁表风险与数据一致性,输出带严重级别的评审报告。Use to review database migrations for safety, rollback, locking and data integrity before deployment."
license: MIT
metadata:
  version: "1.0.0"
---

# 数据库迁移评审

## 何时使用

- 合并前要评审迁移脚本(up/down、SQL 文件);
- 大表变更上线前,想确认会不会锁表、会不会丢数据;
- 迁移经常在生产环境出问题,想建立检查流程;
- 用户明确说"帮我看下这个迁移安不安全"。

## 使用步骤

### 第 1 步:定位迁移与数据库类型

先确认:

1. 迁移文件位置与框架(Alembic、Flyway、golang-migrate、prisma migrate 等);
2. 目标数据库(PostgreSQL、MySQL、SQLite…),规则有差异;
3. 涉及的表和已有数据量(表大不大,线上有没有流量)。

### 第 2 步:逐项检查安全红线

以下问题按严重级别处理:

| 级别 | 问题 |
|---|---|
| P0 阻断 | 大表上普通 `CREATE INDEX`(阻塞写入,应改用 CONCURRENTLY 或在线变更) |
| P0 | 删除/更新语句没有 WHERE,或 WHERE 明显错误 |
| P0 | 新加列 `NOT NULL` 且无默认值(大表会重写并锁表) |
| P0 | 生产环境没有备份或回滚方案就执行破坏性操作 |
| P1 严重 | 同一次迁移里混了 DDL 和 DML(改结构 + 回填数据) |
| P1 | 加 volatile 默认值(如 `DEFAULT now()`)导致整表重写 |
| P1 | 迁移不可回滚且没有标注原因 |
| P2 一般 | 缺少索引或索引冗余、约束缺失 |
| P3 建议 | 命名、格式、注释问题 |

### 第 3 步:检查可回滚性

- 有 down 迁移吗?down 是否真的能还原;
- 不可逆的迁移(如删列)是否显式标注,并确认数据已备份;
- 回滚顺序和 up 是否完全相反。

### 第 4 步:检查数据一致性

- 回填数据是否单独成步,不塞进结构变更里;
- 批量操作是否分批(避免长事务和日志膨胀);
- 约束(外键、唯一)加上前,线上存量数据是否已校验;
- 变更后 ORM 模型与 schema 是否对齐(有没有 drift)。

### 第 5 步:输出评审报告

PostgreSQL/MySQL 差异对照与锁阻塞速查见 [references/DB_DIFFERENCES.md](references/DB_DIFFERENCES.md)。

```markdown
# 迁移评审报告:<文件名>

## 结论
通过 / 修改后通过 / 不通过

## 问题清单
| 级别 | 位置 | 问题 | 证据 | 建议 |

## 风险说明
涉及的表、预估数据量、上线窗口

## 回滚方案
```

## 输入与输出

- 输入:迁移文件(或 diff)+ 数据库类型;
- 输出:评审报告 + 修改建议。

## 示例

**迁移内容(节选):**

```sql
ALTER TABLE orders ADD COLUMN discount DECIMAL NOT NULL;
```

**评审发现:**

- P0:大表上新增 `NOT NULL` 无默认值,会全表重写并锁表;
- 建议:改为可空 + 默认值,回填单独成一步,再收紧约束:

```sql
ALTER TABLE orders ADD COLUMN discount DECIMAL NOT NULL DEFAULT 0;
-- 数据回填(单独迁移)
UPDATE orders SET discount = 0;
-- 收紧(确认存量数据后,单独迁移)
```

## 辅助脚本

[scripts/migration_template.py](scripts/migration_template.py) 生成 up/down 迁移骨架和评审清单:

```bash
python scripts/migration_template.py add_user_email --db postgres
```

生成三个文件:up 脚本、down 脚本、评审清单。

## 注意事项

- 不同数据库规则不同:PostgreSQL 用 `CREATE INDEX CONCURRENTLY`,MySQL 用 `ALGORITHM=INPLACE, LOCK=NONE`;
- 不确定线上数据量就问用户或看监控,不要假设表很小;
- 只评审、不替用户执行生产迁移;
- 评审意见要带证据(哪一行、会有什么后果),不能只说"有风险"。

## 不适用场景

- 迁移还没写,需要的是生成迁移(那是另一件事);
- 用户没有提供迁移文件和数据库信息;
- 数据库未上线、无生产数据(重点应放在设计上)。

## 验证方式

1. 触发:"帮我看下这个迁移安不安全";
2. 检查:报告覆盖锁表、回滚、数据一致性,问题带级别和证据;
3. 抽查:任选一条 P0/P1 意见,对照迁移文件确认问题真实存在。


