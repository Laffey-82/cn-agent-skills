# API 测试用例设计参考

## 每个接口至少覆盖的用例

| 类型 | 覆盖什么 | 例子 |
|---|---|---|
| 正常路径 | 合法输入,验证状态码和响应关键字段 | 正确参数 → 200 + token |
| 边界路径 | 空值、极值、超长、类型不符 | 缺必填字段 → 400 |
| 异常路径 | 未授权、不存在、冲突、服务端错误 | 错密码 → 401 |
| 幂等性(写操作) | 重复提交不产生重复数据 | 同订单号两次 → 只建一单 |
| 鉴权(敏感接口) | 无 token、过期 token、越权 | 未登录访问 → 401 |

## 断言什么

断言行为,不只看状态码:

- 状态码;
- 响应体关键字段(业务数据、错误码、错误信息);
- 副作用(数据是否真的写进去了);
- 响应时间(如果性能是硬指标)。

## 错误响应怎么测

确认三件事:

1. 状态码符合契约;
2. 错误信息可读、不泄露内部细节;
3. 错误码稳定(客户端要依赖它做判断)。

## 用项目已有的测试框架

### curl 冒烟

```bash
curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"wrong"}'
# 预期 401
```

### pytest

```python
def test_login_wrong_password(client):
    resp = client.post("/api/login", json={"username": "admin", "password": "wrong"})
    assert resp.status_code == 401
```

### Jest

```javascript
test("login with wrong password returns 401", async () => {
  const res = await fetch("/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: "admin", password: "wrong" }),
  });
  expect(res.status).toBe(401);
});
```

## 执行前确认清单

- 环境地址(本地 / staging / 线上);
- 认证方式与测试账号;
- 测试数据允许增删改吗;
- 有没有不能碰的接口。

没确认不执行。测试数据用完要清理。
