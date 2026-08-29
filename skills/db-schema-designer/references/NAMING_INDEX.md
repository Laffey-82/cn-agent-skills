# 命名与索引规范参考

## 命名规范(MySQL / PostgreSQL)

| 对象 | 规范 | 例子 |
|---|---|---|
| 库名 | 小写、下划线,业务域前缀 | `shop_order` |
| 表名 | 小写、下划线,单数或复数按团队约定统一 | `orders` |
| 主键 | `id`,BIGINT 自增或 UUID,全库统一 | `id BIGINT UNSIGNED AUTO_INCREMENT` |
| 外键 | `业务_id` | `user_id` |
| 时间 | `created_at`、`updated_at`,统一 TIMESTAMP/TIMESTAMPTZ | `created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP` |
| 布尔 | `is_` 前缀 | `is_active TINYINT(1)` |
| 金额 | 整数分或 DECIMAL,禁止浮点 | `amount_cents INT` |
| 索引名 | `idx_表_列` 或 `uk_表_列`(唯一) | `idx_orders_user_created` |

## 索引设计原则

- 优先覆盖 WHERE、JOIN、ORDER BY 的列;
- 复合索引按查询顺序排,遵守最左前缀;
- 外键列默认建索引;
- 区分度低的列(性别、状态)单独建索引收益小;
- 不要过度索引:写多读少的热表,索引越少越好;
- 大表加索引走迁移评审,避免锁表。

## 查询模式分析模板

```markdown
| 高频查询 | 条件 | 排序 | 对应索引 |
```

每个高频查询都要有索引对应,没有就补,补不上就说明查询本身要改。

## 常见反模式

| 反模式 | 问题 |
|---|---|
| 金额用 FLOAT/DOUBLE | 精度漂移 |
| 状态用裸字符串 | 无约束、易写错 |
| 该加外键不加 | 应用层自觉,数据易脏 |
| 软删除和审计上线后补 | 存量数据难迁移 |
| JSONB 存一切 | 无法约束、查询难优化 |
