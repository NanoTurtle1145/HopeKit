# HopeKit

> Qt6 桌面应用脚手架 — 九风格主题 · 可折叠侧边栏 · 插件式模块 · Windows 原生模糊 · PyInstaller 友好

注意了，这个项目很大部分是 AI 写的，和原来的代码差异很大。我自己都认不出来了，目前正在学习项目结构，防止它认识我，我不认识它。

HopeKit 是一个**开箱即用的 Qt6 桌面应用脚手架**（支持 PySide6 / PyQt6），源自旧项目 HopeTeams-1.6.8 的复活整理。把多风格主题、侧边栏导航、Windows 原生材质、双模式路径这些反复要写的东西打包好了，拿来就能改。

---

## ✨ 脚手架提供的能力

| 能力 | 说明 |
|------|------|
| 🎨 **九风格主题系统** | MD3 / MD2 / Qt 原生 / WinUI3 / Win10 Fluent / GNOME / KDE / macOS Cupertino / ChromeOS，支持 auto / light / dark 三种深浅模式 |
| 🪟 **Windows 原生模糊** | Win11 Mica + Win10 Acrylic，自动降级链，详见 `hopekit/mica.py` 和 `docs/WINUI3_TRANSPARENCY_GUIDE.md` |
| 📐 **可折叠侧边栏** | Navigation Drawer 风格导航，展开/折叠无缝切换，分类 + 按钮两级导航 |
| 🧩 **插件式模块注册** | 加模块 = 写一个插件文件，主文件零修改（见 `hopekit/registry.py`） |
| 💾 **双模式路径处理** | `resource_path()` / `config_path()` 兼容开发模式与 PyInstaller 打包 |
| ⚙️ **嵌入式设置面板** | 左侧二级菜单 + 右侧内容区，主题实时切换，支持导入导出 |
| 📦 **PyInstaller 打包** | 配置好的 spec 文件，一行命令生成独立 exe |

内置 demo（`examples/` 目录）：

| Demo | 说明 |
|------|------|
| 💬 **TCP 聊天室** | C/S 架构 + QThread 多线程广播，局域网即时通信示例 |
| 🌐 **内嵌浏览器** | QtWebEngine 集成，含加载进度与失败回退 |
| ✨ **最小示例** | 20 行跑起来一个窗口，起步模板 |

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Windows（跟随系统强调色 + 原生模糊效果；其他系统可运行，主题回退默认色）

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行

```bash
python hopekitmain.py
```

### 打包为 exe

```bash
pip install pyinstaller
pyinstaller HopeKit.spec
```

打包产物位于 `dist/HopeKit/HopeKit.exe`。

### 最小起步

想要一个空壳项目？复制 `examples/minimal_app.py` 改改就行，20 行跑起来一个带主题的窗口。

```bash
cp examples/minimal_app.py my_app.py
python my_app.py
```

---

## 🏗️ 项目结构

```
hopekitmain.py              ← 主入口（创建 QApp + 加载插件 + 显示主窗口）
demo_acrylic.py             ← Win10 Acrylic 独立测试 Demo
auto_version_commit.py      ← Git 版本变化自动提交/推送脚本
auto_commit.bat             ← 批处理快捷方式
HopeKit.spec                ← PyInstaller 打包配置
requirements.txt            ← 依赖: PySide6>=6.5
theme.json                  ← 主题配置持久化 {"style":"winui3","mode":"light"}
logo.jpg                    ← Logo 图片

hopekit/                    ← 核心框架包
├── __init__.py             ← 统一导出，从 version.py 取版本号
├── version.py              ← ★ 版本号唯一来源 VERSION = "2.1.0"
├── qt_compat.py            ← PySide6 / PyQt6 兼容层
├── paths.py                ← resource_path / config_path 双模式路径
├── theme.py                ← ThemeManager: 9 种风格 + 3 种深浅模式
├── registry.py             ← ModuleRegistry 装饰器式插件注册 + 自动发现
├── main_window.py          ← MainUi 主窗口（侧边栏 + 分类页 + 设置页 + Mica 材质）
├── settings_page.py        ← SettingsPage 嵌入式设置面板（二级菜单: 主题/关于）
├── settings_dialog.py      ← SettingsDialog 旧版弹窗设置（仅 MD3/MD2/Qt）
└── mica.py                 ← Windows DWM 材质管理（Mica/Acrylic/降级全链路）

Styles/
└── styles.py               ← QSS 样式生成（9 种风格 × 3 组: global/main/dialog）

plugins/                    ← 插件目录（自动发现）
├── caidan.py               ← 彩蛋（开发者致敬诗）
├── calculator.py           ← 简易计算器
├── calendar.py             ← 日历控件（页面型 plugin）
├── chat_room_plugin.py     ← TCP 聊天室 / AI 机器人(未启用) / 火车票(未启用) / 外部工具(未启用)
├── copyright.py            ← 版权声明
├── links.py                ← 网站 / QQ群 / 哔哩哔哩 / 博客 / GitHub 等链接
├── shit_window.py          ← 探索系统屎山（关机命令集 + 内置浏览器）
└── shutdown.py             ← 关机命令集

examples/
├── minimal_app.py          ← 最小可运行示例
├── chat_room/              ← TCP 聊天室 demo
├── browser/                ← 内嵌浏览器 demo
└── README.md

docs/
└── WINUI3_TRANSPARENCY_GUIDE.md  ← WinUI3 透明链路防崩指南（超详细）

screenshots/                ← 11 张截图
```

---

## 🔧 作为脚手架使用

### 添加新工具模块

1. 在 `plugins/` 下新建 `my_tool.py`
2. 用 `@ModuleRegistry.register` 装饰工厂函数

**弹窗型**（`kind="window"`，默认）：点击按钮弹出独立窗口，关闭后状态保留。

```python
from hopekit.qt_compat import QDialog, QLabel
from hopekit.registry import ModuleRegistry

@ModuleRegistry.register("my_tool", icon="🔧", title="我的工具", category="tools")
def my_tool_factory(main_window):
    dlg = QDialog()
    dlg.setWindowTitle("我的工具")
    dlg.setFixedSize(300, 200)
    QLabel("Hello from plugin!", dlg).move(80, 80)
    return dlg
```

**页面型**（`kind="page"`）：factory 返回 QWidget，直接嵌入主区域。

```python
from hopekit.qt_compat import QWidget, QVBoxLayout, QLabel
from hopekit.registry import ModuleRegistry

@ModuleRegistry.register("dashboard", icon="📊", title="面板", category="dashboard", kind="page")
def dashboard_factory(main_window):
    panel = QWidget()
    layout = QVBoxLayout(panel)
    layout.addWidget(QLabel("嵌入式面板，不弹窗"))
    return panel
```

3. 启动程序，对应分类页自动出现按钮/面板。实例由 `ModuleRegistry.get_or_create()` 缓存。

### 添加新分类页面

在 `plugins/` 中注册时指定新的 `category`，侧边栏自动出现新分类，内容页自动生成。

### 自定义主题

- **新增风格**：在 `theme.py` 添加 `_build_xxx_palette()` 方法，在 `Styles/styles.py` 添加对应 `_xxx_global/main/dialog()` 三个函数
- **调整配色**：修改现有 `_build_*_palette()` 中的颜色混合参数

详见 [CodeWiki.md](CodeWiki.md)。

---

## 📖 文档

- **[CodeWiki.md](CodeWiki.md)** — 工程深入说明：
  1. 多风格主题系统（9 种风格配色原理）
  2. Windows 原生模糊材质（Mica / Acrylic 全链路）
  3. 主窗口架构（侧边栏 / 分类页 / 设置面板）
  4. 双模式路径处理
  5. 插件注册协议与自动发现
  6. 版本管理与自动提交

- **[docs/WINUI3_TRANSPARENCY_GUIDE.md](docs/WINUI3_TRANSPARENCY_GUIDE.md)** — WinUI3 透明链路防崩指南，含 9 条 AI 高频幻觉禁令 + 翻车对照表 + 正确时序

---

## 📄 版权

版权所有 © 希望工作室 (Hope Studio)

---

*HopeKit 2.1.0 · 不是框架，是好用的脚手架。* （这不是奶糖，这是压缩毛巾，遇水变大变高）
