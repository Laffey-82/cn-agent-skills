---
name: frontend-debug
description: "前端调试。页面报错、白屏、请求失败、交互异常时,按 Console → Network → Elements/Sources → Performance 的路径排查,输出带证据的调试结论。Use to debug frontend issues in the browser with DevTools evidence."
license: MIT
metadata:
  version: "1.0.0"
---

# 前端调试

## 何时使用

- 页面白屏、报错、样式错乱;
- 接口请求失败、数据不显示;
- 交互异常(点按钮没反应、跳转不对);
- 页面卡顿、内存一直涨。

## 使用步骤

### 第 1 步:复现并打开 DevTools

1. F12 打开 DevTools;
2. 复现问题,保持 Console 面板可见;
3. 记下控制台报错(红色)和警告(黄色)。

### 第 2 步:Console 优先

- 红色报错是最高优先级,先解决;
- 点击报错可跳到 Sources 对应行;
- 区分"业务报错"和"第三方脚本报错"(第三方问题先确认是否影响功能);
- 有 sourcemap 时看源码行,没有就按编译后代码推断。

### 第 3 步:Network 查请求

当数据不显示、提交失败时:

- 找到对应请求,看状态码;
- 4xx:看请求参数、鉴权头是否对;
- 5xx:问题在服务端,提供请求信息给后端;
- 看响应体,是结构变了还是真报错;
- 对比"能用的页面"和"坏掉的页面"的请求差异。

### 第 4 步:Elements / Sources 查渲染与逻辑

- 元素没出现:查条件渲染、数据是否真的到了前端;
- 样式不对:查类名、CSS 加载、选择器优先级;
- 点击没反应:查事件绑定、报错是否中断了脚本;
- 在 Sources 打断点,单步看变量值。

### 第 5 步:Performance / Memory 查性能

面板用法、症状对照和 Console 报错分类见 [references/DEVTOOLS_GUIDE.md](references/DEVTOOLS_GUIDE.md)。

- 卡顿:Performance 录制,看长任务和重渲染;
- 内存涨:Memory 面板做堆快照对比;
- 网络慢:Network 里看资源大小和加载时序;
- 结合 [performance-profiler](../performance-profiler/SKILL.md) 深入。

### 第 6 步:输出调试报告

```markdown
# 前端调试报告

## 现象与复现步骤
## 证据(报错信息、请求、截图)
## 根因
## 修复
## 验证方式
```

## 输入与输出

- 输入:页面现象 + 可访问的地址(或本地服务);
- 输出:根因 + 修复 + 验证方式。

## 示例

**现象:** 登录后跳首页白屏。

**Console:** `Uncaught TypeError: Cannot read properties of undefined (reading 'name')`。

**定位:** 报错行在用户信息渲染处,`user.profile` 为 undefined。

**根因:** 接口返回结构里没有 profile 字段,前端没做空值保护。

**修复:** 渲染前判空,接口返回结构对齐。

**验证:** 登录跳转后页面正常,Console 无红色报错。

## 辅助脚本

[scripts/devtools_extract.py](scripts/devtools_extract.py) 从 HAR 文件或 Console 导出文本中提取失败请求、4xx/5xx、慢请求和错误行:

```bash
python scripts/devtools_extract.py network.har
python scripts/devtools_extract.py console.txt
```

脚本只做提取,结论需要人确认。

## 注意事项

- 结论要有证据:报错、请求、截图都算,不能"看起来是";
- 先 Console 后 Network,先定位再动手改;
- 区分前端问题和后端问题,别在前端修后端该修的;
- 第三方脚本报错不影响功能时先记录,不追着修;
- 修复后要回到复现步骤验证,确认问题真的没了。

## 不适用场景

- 纯后端问题(走 [bug-diagnoser](../bug-diagnoser/SKILL.md));
- 本地环境起不来(走 [dev-env-troubleshooter](../dev-env-troubleshooter/SKILL.md));
- 没有浏览器访问条件,只有代码。

## 验证方式

1. 触发:"页面白屏""前端报错""按钮没反应";
2. 检查:报告含 Console/Network 证据和根因;
3. 复核:按修复后的步骤重走一遍,Console 干净、功能正常。


