# 测试写法参考

## 测试命名

用"行为"命名,不用"实现":

| 写法 | 评价 |
|---|---|
| test_password_1 | 看不出测什么 |
| test_short_password_rejected | 清楚,可用 |
| test_valid_password_accepted | 清楚,可用 |

中文项目可用中文描述测试意图:

```python
def test_密码少于8位被拒绝():
    ...
```

## 一个用例覆盖三件事

1. 主路径:正常输入 → 预期输出;
2. 边界:空、零、极值、超长;
3. 异常:非法输入 → 报错或异常。

## 常见框架写法

### pytest

```python
import pytest

def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
```

### Jest

```javascript
test("divide by zero throws", () => {
  expect(() => divide(1, 0)).toThrow();
});
```

### Go

```go
func TestDivideByZero(t *testing.T) {
	if _, err := divide(1, 0); err == nil {
		t.Fatal("expected error")
	}
}
```

## 红灯要"真的红"

测试失败可能因为:

- 行为未实现(有效红灯);
- 测试本身写错(无效);
- 编译/导入错误(无效)。

无效红灯要修测试,不是写实现。

## 别写这些测试

- 只断言"函数被调用过"的测试;
- 断言实现细节(内部变量名、调用顺序)的测试;
- 和实现一起改才能过的"假测试";
- 只测快乐路径、从不失败的测试。
