---
name: tdd-workflow
description: 测试驱动开发。当用户要求按 TDD 方式开发、修复 Bug,或希望代码有测试保障时,执行红灯-绿灯-重构循环,先写失败测试再实现。Use when developing with test-first discipline, fixing bugs with regression tests, or when the user explicitly asks for TDD.
license: MIT
metadata:
  version: "1.0.0"
---

# 测试驱动开发(TDD)

## 何时使用

- 用户明确要求"按 TDD 来做""先写测试";
- 实现一个逻辑密集的功能(校验、计算、状态转换);
- 修复 Bug,需要防止回归;
- 重构代码,需要测试兜底。

## 使用步骤

### 红灯阶段:先写失败测试

1. 理解需求,确定行为与边界(配合 [requirement-clarifier](../requirement-clarifier/SKILL.md));
2. 为"还没写"的代码写测试;
3. 测试必须覆盖:
   - 主路径(正常输入 → 预期输出);
   - 边界(空值、极值、边界值);
   - 异常路径(非法输入 → 错误/异常)。
4. 运行测试,确认**因为正确的原因失败**(测试失败说明行为未实现,而不是测试本身写错)。

### 绿灯阶段:最小实现

1. 写最少量的代码让测试通过;
2. 不要提前实现未测试的功能;
3. 运行全部测试,确认全绿。

### 重构阶段:保持绿色

1. 在测试全绿的前提下重构:消除重复、改善命名、简化结构;
2. 每完成一次小重构,再跑一遍测试;
3. 重构不改变行为,只改变结构。

### 收尾:全量验证

1. 运行整个测试套件,确认无回归;
2. 补上遗漏的边界测试;
3. 输出:测试清单 + 覆盖率情况 + 遗留风险。

## 测试写法参考

测试命名、框架写法、红灯判断见 [references/TEST_WRITING.md](references/TEST_WRITING.md)。

## 输入与输出

- 输入:功能描述或 Bug 描述 + 技术栈;
- 输出:失败测试 → 实现代码 → 通过的测试套件。

## 示例

**需求:** 一个函数 `validatePassword(pw)`,至少 8 位且包含数字。

**红灯(先写测试):**

```python
def test_valid_password():
    assert validate_password("abc12345") is True

def test_short_password():
    assert validate_password("abc12") is False

def test_no_digit_password():
    assert validate_password("abcdefgh") is False
```

**绿灯(最小实现):**

```python
def validate_password(pw: str) -> bool:
    return len(pw) >= 8 and any(c.isdigit() for c in pw)
```

**重构(示例):** 提取常量 `MIN_LENGTH = 8`,让魔法数字有名字。

## 注意事项

- **测试先于代码**:违反顺序就不是 TDD;
- **验证失败原因**:测试"碰巧失败"(如编译错误)不等于有效红灯;
- **不写无意义测试**:只断言实现细节的测试(如"函数被调用过")价值低;
- 测试名用中文或英文均可,但必须描述行为而非实现(`test_short_password_rejected` 优于 `test_password_1`);
- 若项目没有测试框架,先搭最小测试框架再进入循环。

## 不适用场景

- 纯 UI 视觉调整(无明显可断言行为);
- 一次性脚本(不会复用、无回归风险);
- 用户明确要求"先出原型、不写测试"。

## 验证方式

1. 触发:"按 TDD 做""先写测试";
2. 检查:提交顺序是否为 测试 → 实现 → 重构;
3. 运行:测试套件全绿,且故意改错一处实现,确认有测试变红。

