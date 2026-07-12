# HopeKit Changelog

## 2.1.0 (2026-07-12)

### 🎉 新增

- **9 种设计风格主题系统** — MD3、MD2、Qt、WinUI3、Win10 Fluent、GNOME、KDE、cupertino、ChromeOS，每种风格都有独立的深浅色调色板、圆角和选中态策略
- **Windows 原生模糊材质** — Win11 Mica / Win10 Acrylic 三级降级链，首次启动即可自动生效
- **主窗口框架** — 240px 可折叠侧边栏 + 分类导航 + QStackedWidget 内容区 + 嵌入式设置面板
- **插件注册协议** — `@ModuleRegistry.register()` 装饰器，支持 `window` / `page` / 无返回值三种模式，一行接入
- **PySide6 / PyQt6 兼容层** — 优先 PySide6，自动回退 PyQt6，统一导出全部常用类
- **集中版本管理** — `hopekit/version.py` 为版本号唯一源，自动提交脚本同步读取
- **WinUI3 透明效果调试指南** — `docs/WINUI3_TRANSPARENCY_GUIDE.md`，覆盖常见翻车场景与排查步骤

### 🔧 内置插件 (8 个)

| 插件 | 分类 | 说明 |
|------|------|------|
| 彩蛋 | tools | 开发者致敬诗 |
| 简易计算器 | tools | eval 计算器 |
| 日历 | calendar | QCalendarWidget 页面 |
| 聊天室 | tools | TCP C/S 聊天 + QThread |
| 版权声明 | tools | 希望工作室版权 |
| 链接 | links | 开发者网站/QQ群/体育/哔哩哔哩/博客/GitHub |
| 探索系统屎山 | tools | 关机命令 + 内置浏览器 |
| 关机命令集 | tools | shutdown -i |

### 🐛 修复

- **首次启动主题不生效** — 打包后 `theme.json` 位于 `_MEIPASS`（只读资源区），首次启动时自动检测并从内置配置回退加载，同时复制到 exe 同目录持久化
- **WinUI3 / Win10Fluent 透明效果在打包后丢失** — spec 补充 `ctypes`/`ctypes.wintypes` 隐藏导入，过滤系统 DLL 避免冲突
- **插件在打包后无法加载** — `discover_plugins()` 增加 frozen 模式兜底，直接 import 硬编码列表
- **自动版本提交脚本读取错误文件** — 从 `hopekitmain.py` 改为读取 `hopekit/version.py`

### 📦 打包

- PyInstaller spec 全量收集模式：递归发现 `hopekit/`、`plugins/`、`Styles/`、`examples/` 所有模块
- `Tree()` 递归打包四个源码目录到 `datas`
- 自动排除 `api-ms-win-*` 等系统 DLL，确保 `ctypes.windll` 正常调用

### 📝 文档

- **CodeWiki.md** — 10 章详尽技术文档，覆盖主题系统、DWM 材质、主窗口架构、双模式路径、插件协议、QSS 系统等
- **README.md** — 更新为 9 风格主题介绍 + 真实项目结构 + 快速开始示例

---

## 2.0.0 (2026-07-11)

- 从 HopeTeams-1.6.8 重构复兴
- 初始架构：主题管理器 + 模块注册中心 + 主窗口框架
