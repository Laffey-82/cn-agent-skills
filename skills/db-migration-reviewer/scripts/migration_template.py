"""数据库迁移模板生成器:生成 up/down 迁移骨架和评审清单。

用法:
    python migration_template.py <迁移名> --db postgres

输出到当前目录:<迁移名>_up.sql / <迁移名>_down.sql / <迁移名>_review.md
"""

import argparse
import datetime
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="迁移模板生成")
    parser.add_argument("name", help="迁移名,如 add_user_email")
    parser.add_argument("--db", default="postgres", choices=["postgres", "mysql"])
    args = parser.parse_args()

    ts = datetime.datetime.now().strftime("%Y%m%d%H%M")
    base = f"{ts}_{args.name}"

    if args.db == "postgres":
        up = f"""-- {base} up
-- 评审要点:
-- 1. 大表加索引用 CREATE INDEX CONCURRENTLY(不能放在事务里)
-- 2. 新加 NOT NULL 列必须带默认值
-- 3. 数据回填单独成一步,不混在结构变更里

-- BEGIN;
-- ALTER TABLE your_table ADD COLUMN your_column ...;
-- COMMIT;
"""
        down = f"""-- {base} down
-- BEGIN;
-- ALTER TABLE your_table DROP COLUMN IF EXISTS your_column;
-- COMMIT;
"""
    else:
        up = f"""-- {base} up
-- 评审要点:
-- 1. 大表加索引用 ALTER TABLE ... ADD INDEX ... ALGORITHM=INPLACE, LOCK=NONE
-- 2. 新加 NOT NULL 列必须带默认值
-- 3. 数据回填单独成一步

-- ALTER TABLE your_table ADD COLUMN your_column ...;
"""
        down = f"""-- {base} down
-- ALTER TABLE your_table DROP COLUMN IF EXISTS your_column;
"""

    review = f"""# 迁移评审清单:{args.name}

## 基本信息
- 数据库:{args.db}
- 涉及表:
- 预估数据量:
- 上线窗口:

## 评审问题
- [ ] 大表操作是否锁表?(索引用在线方式了吗)
- [ ] 新列 NOT NULL 是否有默认值?
- [ ] DDL 和 DML 是否分开?
- [ ] 有 down 脚本吗?回滚步骤验证过吗?
- [ ] 在类生产环境验证过吗?

## 回滚方案
运行 down 脚本,确认数据与结构还原。
"""

    for suffix, content in [("_up.sql", up), ("_down.sql", down), ("_review.md", review)]:
        path = Path(base + suffix)
        path.write_text(content, encoding="utf-8")
        print(f"已生成 {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
