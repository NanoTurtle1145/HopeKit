# HopeKit

首先声明，这是我寻找到的一个我之前遗弃的项目，我将其重新整理并发布在这里。有些地方使用了AI进行协助，但是主要还是我自己的代码。

**项目名称**：HopeKit

> 基于 PyQt5 的桌面应用框架代码实例 — Material Design 3 主题 · 可折叠侧边栏 · TCP 聊天室 · 开箱即用

---

## 项目简介

HopeKit 是一个**框架型代码实例**，展示了一套完整的现代桌面应用开发范式。项目以"工具箱"为载体，内置了多个功能模块作为示例，开发者可以在此框架基础上快速构建面向不同领域的桌面应用。

**应用方向**：企业内网工具 · 教学演示 · 团队协作平台 · 系统管理工具 · 自定义工作台

---

## ✨ 特性

| 模块 | 说明 |
|------|------|
| 🎨 **MD3 主题系统** | 跟随 Windows 强调色自动生成调色板，支持 auto / light / dark 三种模式 |
| 📐 **可折叠侧边栏** | Material Design 风格导航菜单，展开/折叠无缝切换 |
| 💬 **TCP 聊天室** | 完整的 C/S 架构示例，多线程广播，局域网即时通信 |
| 🌐 **内嵌浏览器** | QtWebEngine 集成，含加载进度与失败友好回退 |
| 🧩 **插件式模块** | 计算器、彩蛋、系统工具探索等示例模块，按需增删 |
| 💾 **配置持久化** | 主题设置 JSON 持久化，打包后仍可读写 |
| 📦 **PyInstaller 打包** | 一行命令生成独立 exe，开箱即用 |

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Windows 系统（最佳体验，跟随系统强调色）
- 其他系统可运行（主题回退为默认色）

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行程序

```bash
python hopekitmain.py
```

### 打包为 exe

```bash
pip install pyinstaller
pyinstaller HopeTeams.spec
```

打包产物位于 `dist/HopeTeams/HopeTeams.exe`。

---

## 🏗️ 项目架构

```
hopekitmain.py          ← 主入口 · 主题管理 · 主界面 · 工具窗口
chat_room.py            ← 聊天室模块 · TCP 通信 · 浏览器
Styles/
└── styles.py           ← QSS 样式表生成（MD3 风格）
theme.json              ← 主题配置持久化
HopeTeams.spec          ← PyInstaller 打包配置
```

### 核心框架能力

| 能力 | 实现位置 | 说明 |
|------|----------|------|
| 主题引擎 | `ThemeManager` | 动态读取 Windows 注册表，生成 25+ 颜色 token |
| 导航系统 | `MainUi._sidebar` | 可折叠侧边栏 + StackedWidget 多页面 |
| 网络通信 | `Server` / `Client` | TCP C/S 架构，QThread 多线程 |
| 内存管理 | 子窗口引用持有 | 惰性创建 + 实例属性，防止 GC 回收 |
| 打包兼容 | `resource_path()` / `config_path()` | 开发/打包双模式路径处理 |

---

## 📖 文档

- **[CodeWiki.md](CodeWiki.md)** — 完整的代码 Wiki，包含：
  - 项目整体架构与模块详解
  - 关键类与函数说明
  - 主题系统与样式系统原理
  - 网络通信机制
  - 打包部署指南
  - 已知问题与注意事项

---

## 🔧 作为框架使用

### 添加新工具模块

1. 在 `hopekitmain.py` 中继承 `QDialog` 或 `QMainWindow` 创建新窗口类
2. 在 `MainUi.__init__` 中添加窗口引用占位（如 `self._xxx_win = None`）
3. 在 `_build_tools_page()` 的 `tools` 列表中添加按钮配置
4. 添加 `_open_xxx()` 惰性创建方法

### 添加新分类页面

1. 在 `MainUi._build_ui` 的 `categories` 列表中添加新分类
2. 实现 `_build_xxx_page()` 方法
3. 在 `_stack.addWidget()` 中添加新页面

### 自定义主题

修改 `ThemeManager._build_palette()` 中的颜色混合参数，或直接硬编码自定义调色板。

---

## 📄 版权声明

版权所有 © 希望工作室 (Hope Studio)

详见 CodeWiki 第 12 章及应用内版权声明窗口。

---

*HopeKit 2.0.0-revived · 希望工作室出品*
