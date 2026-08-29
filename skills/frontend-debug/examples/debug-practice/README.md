# 前端调试练习页

一个故意埋了 3 个常见问题的页面,配合 [scripts/devtools_extract.py](../../scripts/devtools_extract.py) 练习排查。

## 问题清单

1. `user.profile` 为 undefined,渲染时读 `.name` 报 TypeError(数据字段没判空);
2. 按钮绑定了未定义的函数,点击没反应(Console 里有 ReferenceError);
3. 请求 `/api/user` 不存在,返回 404。

## 练习步骤

1. 本地起一个静态服务打开页面:
   ```bash
   python -m http.server 8080
   ```
   访问 http://127.0.0.1:8080
2. 打开 DevTools Console,先看红色报错;
3. 到 Network 看 `/api/user` 的状态码;
4. 结合报错定位到具体代码行;
5. 修复:判空、移除错误绑定、接上真实接口。

## 怎么修(参考)

- 问题 1:渲染前判空 `user.profile && user.profile.name`;
- 问题 2:给 `bad-btn` 绑定一个真正存在的处理函数;
- 问题 3:换成真实存在的接口地址。

修完刷新页面,Console 无红色报错、用户信息正常显示,就算过关。
