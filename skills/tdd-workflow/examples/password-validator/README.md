# TDD 示例:密码校验器

这是一个完整的"红灯 → 绿灯 → 重构"循环示例,可以直接运行。

## 步骤还原

1. **红灯**:先写 `test/test_password_validator.py`,此时 `validate_password` 还不存在,运行测试会失败;
2. **绿灯**:实现 `src/password_validator.py` 的最简版本,让测试通过;
3. **重构**:把魔法数字 `8` 提取为常量 `MIN_LENGTH`,行为不变。

## 运行

```bash
pip install pytest
python run_tests.py
```

预期输出:`6 passed`。

## 故意破坏验证

把 `len(password) >= MIN_LENGTH` 改成 `>` 再跑,`test_exact_min_length_accepted` 应该变红——这证明测试真的在守护行为。
