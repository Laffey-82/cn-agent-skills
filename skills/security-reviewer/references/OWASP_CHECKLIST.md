# 安全检查清单(OWASP 思路)

## 注入

- SQL:参数化查询,禁止字符串拼接;
- 命令:用户输入不进 shell 命令;
- 路径:文件路径校验,防 `../` 穿越;
- 代码:`eval`、动态 import 不接外部输入。

## 认证与会话

- 密码哈希:bcrypt / argon2,禁止明文和 MD5;
- token:安全存储,过期机制;
- 会话固定:登录后更换会话标识;
- 暴力破解:登录限流或锁定策略。

## 越权

- 水平越权:A 用户能否访问 B 用户的数据;
- 垂直越权:普通用户能否调用管理接口;
- 服务端校验:不信任前端传的 user_id / role。

## XSS 与 CSRF

- 输出编码,不用 `innerHTML` / `v-html` 直接渲染用户输入;
- CSP 头;
- 状态变更请求有 CSRF 防护(token 或 SameSite)。

## 敏感数据

- 日志:不打印密钥、token、手机号;
- 错误信息:不向用户暴露堆栈和内部路径;
- 响应:不返回多余字段(password_hash、内部字段);
- 传输:HTTPS,敏感接口禁止明文。

## 依赖与配置

- 依赖审计:`npm audit` / `pip-audit` / `govulncheck`;
- 密钥走环境变量或 secrets,不进代码库;
- 安全头:Content-Security-Policy、X-Frame-Options、X-Content-Type-Options;
- 框架默认安全配置不要轻易关闭(CSRF 中间件、自动转义)。

## 常见危险写法速认

| 写法 | 风险 |
|---|---|
| `SELECT ... WHERE name = '${input}'` | SQL 注入 |
| `exec("rm " + input)` | 命令注入 |
| `open("/data/" + input)` | 路径穿越 |
| `v-html` / `innerHTML` 渲染用户输入 | XSS |
| 前端判断角色就放行 | 越权 |
| 日志里打 password / token | 数据泄露 |
