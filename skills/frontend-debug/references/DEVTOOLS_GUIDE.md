# DevTools 面板速查

## 四个面板怎么用

| 面板 | 什么时候用 | 看什么 |
|---|---|---|
| Console | 报错、警告、日志 | 红色报错、未捕获异常、网络错误 |
| Network | 请求失败、数据不显示 | 状态码、响应体、请求头、时序 |
| Elements | 元素/样式问题 | DOM 结构、计算样式、类名 |
| Sources | 逻辑问题 | 断点、变量值、调用栈 |
| Performance | 卡顿、加载慢 | 长任务、重渲染、瀑布图 |
| Memory | 内存涨、页面越来越卡 | 堆快照、内存分配 |

## 常见症状 → 面板

| 症状 | 先看 |
|---|---|
| 白屏 | Console(报错)+ Network(入口请求) |
| 数据不显示 | Network(请求是否成功、响应结构) |
| 点击没反应 | Console(报错中断)+ Sources(事件绑定) |
| 样式错乱 | Elements(类名、计算样式)+ Network(CSS 是否加载) |
| 卡顿 | Performance(长任务) |
| 内存涨 | Memory(堆快照对比) |

## Console 报错分类

| 报错 | 常见原因 |
|---|---|
| TypeError: Cannot read properties of undefined | 数据字段不存在,没判空 |
| ReferenceError: xxx is not defined | 变量/函数未定义或作用域错 |
| SyntaxError | 语法错,构建没通过 |
| Failed to fetch / NetworkError | 跨域、服务没起、网络 |
| 404 / 500 打印在 Console | 请求失败,去 Network 看详情 |

## 快速验证手段

- 无痕窗口:排除扩展和缓存干扰;
- 换浏览器:排除浏览器特有行为;
- 清缓存强刷:Ctrl+Shift+R;
- 抓接口:Network 里右键 Copy as cURL 复现;
- 对比法:找一个能用的页面/环境对比请求差异。

## 提交报告时附什么

- 报错全文(含堆栈);
- 对应请求的 URL、方法、状态码、响应摘要;
- 复现步骤;
- 截图(白屏、样式问题必附)。
