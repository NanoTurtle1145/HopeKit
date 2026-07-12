# HopeKit

> Qt6 桌面应用脚手架 — MD3 主题 · 可折叠侧边栏 · 插件式模块 · PyInstaller 友好

注意了，这个项目很大部分是AI写的，和原来的代码差异很大。我自己都认不出来了，目前正在学习项目结构，防止它认识我，我不认识它。

HopeKit 是一个**开箱即用的 Qt6 桌面应用脚手架**（支持 PySide6 / PyQt6），源自旧项目 HopeTeams-1.6.8 的复活整理。
把 MD3 主题、侧边栏导航、双模式路径这些反复要写的东西打包好了，拿来就能改。

---

## ✨ 脚手架提供的能力

| 能力 | 说明 |
|------|------|
| 🎨 **MD3 主题系统** | 跟随 Windows 强调色自动生成调色板，支持 auto / light / dark 三种模式 |
| 📐 **可折叠侧边栏** | Material Design 风格导航，展开/折叠无缝切换，分类 + 按钮两级导航 |
| 🧩 **插件式模块注册** | 加模块 = 写一个插件文件，主文件零修改（见 `hopekit/registry.py`） |
| 💾 **双模式路径处理** | `resource_path()` / `config_path()` 兼容开发模式与 PyInstaller 打包 |
| 📦 **PyInstaller 打包** | 配置好的 spec 文件，一行命令生成独立 exe |

内置 demo（`examples/` 目录）：

| Demo | 说明 |
|------|------|
| 💬 **TCP 聊天室** | C/S 架构 + QThread 多线程广播，局域网即时通信示例 |
| 🌐 **内嵌浏览器** | QtWebEngine 集成，含加载进度与失败回退 |
| 🔢 **计算器** | 简易四则运算，演示工具窗口注册 |

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Windows（跟随系统强调色；其他系统可运行，主题回退默认色）

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
hopekitmain.py          ← 主入口
hopekit/
├── __init__.py
├── registry.py         ← ModuleRegistry 插件注册器
└── theme.py            ← ThemeManager（待拆分）
Styles/
└── styles.py           ← QSS 样式表生成（MD3 风格）
plugins/                ← 你的插件放这里
examples/
├── minimal_app.py      ← 最小可运行示例
├── chat_room/          ← TCP 聊天室 demo
└── browser/            ← 内嵌浏览器 demo
theme.json              ← 主题配置持久化
HopeKit.spec            ← PyInstaller 打包配置
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

**页面型**（`kind="page"`）：factory 返回 QWidget，直接嵌入主区域，像 VS Code 的 Editor 面板。

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

3. 启动程序，对应分类页自动出现按钮/面板。实例由 `ModuleRegistry.get_or_create()` 缓存，关闭再开状态不丢。

### 添加新分类页面

1. 在 `plugins/` 中注册时指定新的 `category`
2. 侧边栏自动出现新分类，内容页自动生成

### 自定义主题

修改 `ThemeManager._build_palette()` 中的颜色混合参数，或直接硬编码调色板。
详见 [CodeWiki.md](CodeWiki.md) 第 1 章。

---

## 📖 文档

- **[CodeWiki.md](CodeWiki.md)** — 三个核心主题的深入说明：
  1. MD3 主题系统（配色原理、调色板生成）
  2. 双模式路径处理（resource_path / config_path）
  3. 模块注册协议（插件开发指南）

---

## 📄 版权

版权所有 © 希望工作室 (Hope Studio)

---

*HopeKit 2.0.0 · 不是框架，是好用的脚手架。* （这不是奶糖，这是压缩毛巾，遇水变大变高）
