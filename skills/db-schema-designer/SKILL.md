---
name: db-schema-designer
description: "数据库表结构设计。从需求出发设计表、字段、关系和索引,覆盖命名规范、数据类型、约束与查询模式分析,输出建表脚本和设计说明。Use to design or review relational database schemas from requirements."
license: MIT
metadata:
  version: "1.0.0"
---

# 数据库表结构设计

## 何时使用

- 新功能需要建表;
- 用户说"帮我把数据模型设计一下";
- 现有表结构混乱,想梳理;
- 查询慢,需要结合查询模式优化索引。

## 使用步骤

### 第 1 步:明确需求

先问清楚:

1. 核心实体有哪些(用户、订单、商品…);
2. 实体之间什么关系(一对多、多对多、一对一);
3. 主要查询是什么(按什么条件查、查多频繁);
4. 数据量预期和写入频率;
5. 要不要历史记录、软删除、多租户。

### 第 2 步:设计表与字段

命名规范(以 MySQL/PostgreSQL 为例):

- 表名、字段名小写,下划线分隔;
- 表名用复数或单数按团队约定,全仓库统一;
- 主键用自增或 UUID 按业务定,不要混用;
- 时间字段统一 `created_at`、`updated_at`;
- 布尔字段用 `is_` 前缀(`is_active`);
- 金额用整数分或 DECIMAL,禁止浮点。

字段设计检查:

- 类型匹配:长度、精度、时区是否合适;
- 可空性:哪些字段必须 NOT NULL,默认值是什么;
- 冗余:能拆的就拆,别为省事存重复数据;
- 枚举:固定取值用枚举或字典表,别裸存字符串。

### 第 3 步:设计索引

命名规范、索引原则和反模式清单见 [references/NAMING_INDEX.md](references/NAMING_INDEX.md)。

原则:

- 索引优先覆盖 WHERE、JOIN、ORDER BY 的列;
- 外键列默认建索引;
- 复合索引按查询顺序排,最左前缀优先;
- 区分度低的列(性别、状态)单独建索引意义不大;
- 不要过度索引,写入多、索引多会拖慢;
- 大表加索引走迁移评审流程。

### 第 4 步:输出设计交付物

```markdown
# 数据模型:<名称>

## 实体关系
(文字描述或 ER 图)

## 表定义
表名 | 字段 | 类型 | 约束 | 说明

## 索引
表名 | 索引名 | 列 | 类型 | 理由

## 查询模式分析
高频查询与对应索引

## 建表脚本
SQL

## 待确认
```

## 输入与输出

- 输入:需求描述 + 查询模式;
- 输出:表定义、索引方案、建表脚本、设计说明。

## 示例

**需求:** 用户下单,订单里有商品。

**表设计节选:**

| 表 | 字段 | 类型 | 约束 |
|---|---|---|---|
| users | id / email / password_hash / created_at | BIGINT / VARCHAR / VARCHAR / TIMESTAMP | id 主键,email 唯一 |
| orders | id / user_id / amount_cents / status / created_at | BIGINT / BIGINT / INT / VARCHAR / TIMESTAMP | user_id 外键 |
| order_items | id / order_id / product_name / price_cents / qty | BIGINT | order_id 外键 |

**索引:**

- `orders(user_id, created_at)` — 查用户订单列表;
- `orders(status)` — 按状态筛选(数据量大了再考虑);
- `order_items(order_id)` — 外键列。

## 注意事项

- 先问查询模式再定索引,索引是给查询服务的;
- 数据一致性:外键、唯一约束该加就加,别依赖应用层自觉;
- 软删除、审计字段要在设计阶段定好,别上线后再补;
- 大表加列/加索引的锁表风险交给迁移评审把关;
- 设计完和用户过一遍核心查询,确认能覆盖。

## 不适用场景

- 需求还没理清(先走 [requirement-clarifier](../requirement-clarifier/SKILL.md));
- 只需要评审现有迁移(走 [db-migration-reviewer](../db-migration-reviewer/SKILL.md));
- NoSQL 文档模型(本技能面向关系型数据库)。

## 验证方式

1. 触发:"帮我设计数据模型""建几张表";
2. 检查:交付物含表定义、索引、建表脚本、查询模式分析;
3. 走查:用核心查询语句跑 EXPLAIN,确认索引命中。

