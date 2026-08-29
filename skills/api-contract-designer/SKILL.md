---
name: api-contract-designer
description: API 契约设计。需求确认后、实现开始前,定义接口的方法、路径、参数、响应与错误码,输出可校验的契约 JSON,前后端按同一份契约并行开发。Use to design an API contract before implementation.
license: MIT
metadata:
  version: "1.0.0"
---

# API 契约设计

## 何时使用

- 用户说"设计一下这个接口""先定个 API 契约";
- 用户说"接口文档怎么写""帮我把接口定下来"——还没有契约,需要先设计;
- 前后端要并行开发,需要先对齐接口;
- 新功能要加接口,想先明确输入输出再动手;
- 接口设计有争议,需要一份可评审的契约。

## 使用步骤

### 第 1 步:确认需求与资源

从需求规格(可先用 [requirement-clarifier](../requirement-clarifier/SKILL.md))明确:

- 这个接口解决什么问题;
- 操作的对象是什么资源(用户、订单、商品…);
- 调用方是谁(前端、第三方、内部服务)。

### 第 2 步:定方法与路径

- URL 面向资源:`/users`、`/users/{id}`,不写动词;
- 方法语义:GET 查、POST 建、PUT/PATCH 改、DELETE 删;
- 集合操作(列表、创建)用复数资源名,单对象操作用 `/资源/{id}`;
- 动作类接口(如"发布")优先用子资源或明确动词:`POST /articles/{id}/publish`。

### 第 3 步:定参数

每个参数明确:

| 要素 | 说明 |
|---|---|
| 位置 | path / query / header / body |
| 类型 | string / int / bool / array / object |
| 必填 | required 是或否 |
| 约束 | 长度、范围、枚举,写具体 |

路径里的 `{id}` 必须对应一个 `in=path` 的参数。

### 第 4 步:定响应与错误码

- 每个接口至少一个成功响应(2xx),语义对应:201 创建成功、200 查询成功、204 删除成功;
- 错误码用语义化状态码:400 参数错、401 未认证、403 无权限、404 不存在、409 冲突、429 限流、5xx 服务端;
- 响应字段写类型,和前端约好关键字段;
- 幂等性:PUT/DELETE 重复调用结果一致,GET 不产生副作用。

### 第 5 步:输出契约并校验

按模板输出契约 JSON(用 contract_checker.py 生成模板见[辅助脚本](#辅助脚本)),校验通过后:

- 和调用方逐条过契约,确认无歧义;
- 契约定稿后,前端按它开发,后端按它实现;
- 实现完成后用 [api-tester](../api-tester/SKILL.md) 按契约生成测试验证。

## 输入与输出

- 输入:需求描述 + 调用方约束;
- 输出:契约 JSON + 人读的接口说明。

## 示例

**用户输入:** "给登录做一个接口契约。"

**契约 JSON(节选):**

```json
{
  "name": "login-api",
  "version": "0.1.0",
  "base_path": "/api",
  "endpoints": [
    {
      "method": "POST",
      "path": "/login",
      "summary": "用户名密码登录",
      "auth": "none",
      "params": [
        {"name": "username", "in": "body", "type": "string", "required": true},
        {"name": "password", "in": "body", "type": "string", "required": true}
      ],
      "responses": {
        "200": {"desc": "成功,返回 token"},
        "400": {"desc": "缺参"},
        "401": {"desc": "账号或密码错误"}
      }
    }
  ]
}
```

## 辅助脚本

[scripts/contract_checker.py](scripts/contract_checker.py) 校验契约 JSON 的完整性:

```bash
# 生成契约模板
python skills/api-contract-designer/scripts/contract_checker.py --new contract.json

# 校验契约
python skills/api-contract-designer/scripts/contract_checker.py contract.json
```

检查:方法白名单、路径以 / 开头、路径参数有对应 path 参数、参数必填项有类型、响应非空、method+path 不重复。脚本只做标记,结论需要人确认。

## 注意事项

- **契约先行,实现后置**:没对齐契约就写代码,返工成本最高;
- 状态码语义化,别一律 200 包业务码(除非团队既有约定);
- 破坏性变更(改路径、改必填参数)要显式评审,别悄悄改;
- 参数约束写具体(最大长度、枚举值),别写"合理范围"。

## 不适用场景

- 接口已实现,需要的是测试(用 api-tester);
- 需求还没澄清,先做需求澄清再设计;
- 纯内部一次性调用,不需要契约化。

## 验证方式

1. 触发:"设计接口契约";
2. 跑脚本:contract_checker.py 无"必须"级问题;
3. 走查:每个路径参数都有 path 参数,每个接口有成功响应;
4. 确认:调用方对契约无异议,前后端按同一份契约开发。
