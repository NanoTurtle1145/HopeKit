# examples/

内置 demo 集合，展示如何基于 HopeKit 脚手架构建不同类型的模块。

| Demo | 说明 |
|------|------|
| `minimal_app.py` | 最小可运行示例，20 行跑起带主题的空窗口 |
| `chat_room/` | TCP 局域网聊天室（C/S 架构 + QThread 多线程） |
| `browser/` | 内嵌浏览器（QtWebEngine 集成） |

每个 demo 都是独立可运行的，也可以作为插件注册到主程序中。
