# HopeKit Code Wiki

> **项目名称**: HopeKit  
> **版本**: 2.0.0-revived  
> **开发团队**: 希望工作室 (Hope Studio)  
> **主入口文件**: [hopekitmain.py](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py)  
> **打包配置**: [HopeTeams.spec](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/HopeTeams.spec)

---

## 目录

1. [项目概述](#1-项目概述)
2. [整体架构](#2-整体架构)
3. [文件结构](#3-文件结构)
4. [模块详解](#4-模块详解)
5. [关键类与函数](#5-关键类与函数)
6. [主题系统](#6-主题系统)
7. [样式系统](#7-样式系统)
8. [网络通信机制](#8-网络通信机制)
9. [依赖关系](#9-依赖关系)
10. [项目运行方式](#10-项目运行方式)
11. [打包部署](#11-打包部署)
12. [已知问题与注意事项](#12-已知问题与注意事项)

---

## 1. 项目概述

HopeKit 是一个**基于 PyQt5 的桌面应用框架代码实例**，展示了一套完整的现代桌面应用开发范式：Material Design 3 主题系统、可折叠侧边栏导航、多模块插件化布局、TCP 网络通信、PyInstaller 打包部署等。项目以"工具箱"为载体，内置了局域网聊天室、计算器、内嵌浏览器、日历等功能模块作为示例，开发者可以在此框架基础上快速构建面向不同领域的桌面应用。

> **定位**: 框架型代码实例 / 桌面应用脚手架 / PyQt5 最佳实践参考
> **应用方向**: 企业内网工具、教学演示、团队协作平台、系统管理工具等

### 1.1 核心特性

| 特性 | 说明 |
|------|------|
| 局域网聊天室 | 基于 TCP Socket 的 C/S 架构，服务端多线程广播，客户端收发消息（网络通信示例） |
| Material Design 3 主题 | 跟随 Windows 强调色自动生成调色板，支持 auto/light/dark 三种模式（主题系统示例） |
| 可折叠侧边栏 | 分类导航菜单（工具/链接/日历），折叠后仅显示图标（导航系统示例） |
| 内嵌浏览器 | 基于 QtWebEngine 的简易浏览器，含加载状态与失败友好错误页（Web 集成示例） |
| 集成工具箱 | 计算器、关机命令、系统工具探索等（功能模块示例） |
| 主题持久化 | 主题选择保存到 `theme.json`，重启后保持（配置持久化示例） |
| PyInstaller 打包 | 支持打包为独立 exe 可执行文件（部署分发示例） |
| 窗口引用管理 | 子窗口惰性创建 + 实例属性持有，防止 GC 回收（内存管理示例） |

### 1.2 版本历史

#### Hope-Teams 时期（原项目）

> 原项目地址：https://github.com/GXBF/Hope-Teams/releases

| 版本 | 发布日期 | 说明 |
|------|----------|------|
| Hope-Teams 1.0.0 | 2023-09-11 | 第一版，功能较少。打开程序后直接点击"登录"即可 |
| Hope-Teams 1.4.2 | 2023-09-17 | 添加了一些没用的东西 |
| Hope-Teams 1.4.7 | 2023-09-19 | 有史以来最大的更新：彩蛋、DiskGenius、Dism++（64/32/Arm64）、硬件检测工具等 |
| Hope-Teams 1.5.6 | 2023-09-23 | 可以看亚运会力（喜 |
| Hope-Teams 1.6.5 | 2023-10-10 | 添加了"更多软件" |
| Hope-Teams 1.6.8 | 2023-11-23 | 小更新，添加了人工智能模型 |

#### HopeKit 时期（当前框架）

| 版本 | 说明 |
|------|------|
| HopeKit 2.0.0-revived | 当前版本：清理死代码与 API Key、拆分模块、MD3 主题系统、侧边栏导航、框架化重构 |

---

## 2. 整体架构

### 2.1 架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                           MainUi (主界面)                            │
│                                                                     │
│  ┌──────────┐  ┌──────────────────────────────────────────────────┐ │
│  │ 侧边栏   │  │              StackedWidget 内容区                 │ │
│  │ (可折叠) │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐            │ │
│  │          │  │  │ 工具页  │ │ 链接页  │ │ 日历页  │            │ │
│  │ · 工具   │  │  │         │ │         │ │         │            │ │
│  │ · 链接   │  │  │ 聊天室  │ │ 网站    │ │ QCalendar│           │ │
│  │ · 日历   │  │  │ 计算器  │ │ 版权    │ │         │            │ │
│  │          │  │  │ 彩蛋    │ │ QQ群    │ │         │            │ │
│  │ · 设置   │  │  │ 屎山    │ │ GitHub  │ │         │            │ │
│  │ · 退出   │  │  └─────────┘ └─────────┘ └─────────┘            │ │
│  └──────────┘  └──────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘

聊天室子系统 (chat_room.py):
┌──────────┐     TCP Socket      ┌──────────┐
│  Server  │ ◄──────────────────► │  Client  │
│  (多线程) │   (广播/单播)        │ (单线程) │
└──────────┘                      └──────────┘
     │                                 │
     ▼                                 ▼
┌──────────────┐                ┌──────────────┐
│ ServerThread │                │ ClientThread │
│  (QThread)   │                │  (QThread)   │
└──────────────┘                └──────────────┘

主题子系统:
┌──────────────┐     读取      ┌─────────────┐
│ ThemeManager │ ◄───────────  │ theme.json  │
│  (MD3 调色板) │ ──────────►  │ (持久化)    │
└──────┬───────┘   保存        └─────────────┘
       │ 读取注册表
       ▼
┌──────────────┐
│ Windows 注册表│
│ (强调色/深浅) │
└──────────────┘
       │ 生成 colors dict
       ▼
┌──────────────┐
│ Styles 模块   │
│ (QSS 样式表)  │
└──────────────┘

路径处理层:
┌──────────────────────────────────────────────────────────────────┐
│  resource_path()  → 只读资源 (logo.jpg)                          │
│                     打包后从 sys._MEIPASS 解压目录加载             │
├──────────────────────────────────────────────────────────────────┤
│  config_path()    → 可读写配置 (theme.json)                      │
│                     打包后放在 exe 同目录                         │
└──────────────────────────────────────────────────────────────────┘
```

### 2.2 架构特点

- **多文件模块化**: 主入口、聊天室、样式分离为独立模块
- **GUI 驱动**: 以 PyQt5 为核心的事件驱动架构
- **信号槽通信**: Qt 信号槽机制实现线程间、组件间通信
- **C/S 模式聊天室**: 服务端多线程 accept，消息广播
- **MD3 主题引擎**: 动态读取 Windows 系统配色，生成完整调色板
- **窗口引用管理**: 子窗口由父窗口实例属性持有，防止 GC 回收
- **打包兼容**: 通过 `resource_path()` / `config_path()` 兼容 PyInstaller 打包

---

## 3. 文件结构

```
Hope-Teams-1.6.8/
├── hopekitmain.py              # 主程序入口（ThemeManager + MainUi + 工具窗口）
├── chat_room.py               # 聊天室模块（Server/Client/Thread/MainWindow）
├── Styles/
│   ├── styles.py              # QSS 样式表生成函数
│   └── __pycache__/
├── theme.json                 # 主题模式持久化配置
├── requirements.txt           # Python 依赖清单
├── HopeTeams.spec             # PyInstaller 打包配置
├── logo.jpg                   # 程序 Logo 图标
├── README.md                  # 项目说明
├── CodeWiki.md                # 本文档
├── __pycache__/
│   ├── hopekitmain.cpython-312.pyc
│   └── chat_room.cpython-312.pyc
└── dist/                      # PyInstaller 打包输出目录
    └── HopeTeams/
        ├── HopeTeams.exe      # 打包后的可执行文件
        └── _internal/         # 打包依赖（PyQt5、Python 运行时等）
```

### 文件职责

| 文件 | 职责 | 类数量 |
|------|------|--------|
| [hopekitmain.py](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py) | 主入口、主题管理、路径处理、工具窗口、主界面 | 7 |
| [chat_room.py](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/chat_room.py) | 聊天室网络通信、聊天窗口、浏览器窗口 | 8 |
| [Styles/styles.py](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/Styles/styles.py) | QSS 样式表字符串生成 | 0 (纯函数) |
| [HopeTeams.spec](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/HopeTeams.spec) | PyInstaller 打包配置 | — |
| [theme.json](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/theme.json) | 主题模式持久化 | — |

---

## 4. 模块详解

### 4.1 主程序入口 (hopekitmain.py)

#### 路径处理函数

**位置**: [hopekitmain.py#L30-L45](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py#L30-L45)

| 函数 | 签名 | 功能 |
|------|------|------|
| `resource_path(relative)` | `str -> str` | 只读资源路径（logo 等），打包后从 `sys._MEIPASS` 解压目录加载 |
| `config_path(filename)` | `str -> str` | 可读写配置文件路径（theme.json），放在 exe 同目录便于持久化 |

**设计意图**: 兼容 PyInstaller 打包后资源路径变化的问题：
- 开发模式：资源在源码同级目录
- 打包模式：资源被嵌入 exe，运行时解压到临时 `_MEIPASS` 目录

#### ThemeManager — 主题管理器

**位置**: [hopekitmain.py#L51-L271](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py#L51-L271)

Material Design 3 风格主题管理器，支持三种模式：
- `auto`: 跟随 Windows 系统强调色 + 深浅色
- `light`: 固定浅色（使用 Windows 强调色生成调色板）
- `dark`: 固定深色（使用 Windows 强调色生成调色板）

**核心机制**:
1. 读取 Windows 注册表获取系统强调色 (`AccentColor`)
2. 读取注册表获取系统深浅色设置 (`AppsUseLightTheme`)
3. 通过强调色 + 明暗混合算法派生出完整 MD3 调色板
4. 配色模式持久化到 `theme.json`

**调色板字段**: 25+ 个颜色 token：`primary`, `on_primary`, `primary_container`, `secondary`, `surface`, `background`, `outline`, `error`, `sidebar_bg`, `sidebar_hover`, `sidebar_active` 等，外加 `card_radius`/`btn_radius`/`nav_radius` 三个圆角常量。

#### MainUi — 主界面

**位置**: [hopekitmain.py#L518-L883](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py#L518-L883)

**继承**: `QMainWindow`  
**固定大小**: 1200×665  
**侧边栏宽度**: 展开 210px / 折叠 48px

**UI 组成**:
- **左侧可折叠侧边栏**
  - 菜单标题（折叠时隐藏）
  - 折叠/展开按钮（◀ 折叠 / ▶）
  - 分类导航按钮（工具/链接/日历，带选中高亮）
  - 设置按钮（打开主题设置对话框）
  - 退出按钮（红色错误风格）
- **右侧主内容区**
  - 顶部：Logo + 标题 "HopeKit 2.0.0-revived" + 问候语
  - `QStackedWidget` 堆叠页面（3 页切换）

**三个分类页面**:

| 页面 | 构建方法 | 内容 |
|------|----------|------|
| 工具 | [_build_tools_page()](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py#L659-L695) | 聊天室、彩蛋、计算器、探索系统屎山、AI机器人(禁用)、查火车票(禁用)、外部工具(禁用) |
| 链接 | [_build_links_page()](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py#L697-L755) | 开发者新闻（网站/版权/QQ群/亚运）+ 联系作者（B站/博客/GitHub） |
| 日历 | [_build_calendar_page()](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py#L757-L772) | QCalendarWidget |

**窗口引用管理**: 所有子窗口通过实例属性持有强引用，采用惰性创建模式：
```python
def _open_xxx(self):
    if self._xxx_win is None:
        self._xxx_win = XxxWindow()
        self._xxx_win.setStyleSheet(MainUi._global_stylestring())
    self._xxx_win.show()
```

#### SettingsDialog — 设置对话框

**位置**: [hopekitmain.py#L439-L513](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py#L439-L513)

**继承**: `QDialog`  
**固定大小**: 420×360

**功能**: 提供 auto/light/dark 三选一单选按钮，点击"应用"后立即切换主题并刷新所有已打开的子窗口样式。

#### 工具窗口类

| 类名 | 继承 | 位置 | 功能 |
|------|------|------|------|
| `CaidanWindow` | `QMainWindow` | [L280-L300](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py#L280-L300) | 彩蛋窗口（程序员打油诗） |
| `ShutWindow` | `QDialog` | [L306-L313](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py#L306-L313) | 关机命令集（执行 `shutdown -i`） |
| `ShitWindow` | `QDialog` | [L318-L351](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py#L318-L351) | 系统工具探索入口（关机命令集 + 简易官网），含 WebEngine 失败回退 |
| `Calculator` | `QDialog` | [L357-L396](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py#L357-L396) | 简易四则运算计算器 |
| `CopyrightWindow` | `QMainWindow` | [L402-L433](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py#L402-L433) | 版权声明查看器 |

### 4.2 聊天室模块 (chat_room.py)

#### MainWin — 聊天室主窗口

**位置**: [chat_room.py#L322-L450](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/chat_room.py#L322-L450)

**继承**: `QMainWindow`

**UI 组成**:
- 聊天记录显示区（只读 QTextEdit，9行2列网格）
- 消息输入框 + 发送按钮
- 连接信息配置区（ConfigBox）
  - 服务器IP（带输入掩码 `000.000.000.000`）
  - 端口（默认 1145）
  - 昵称（默认主机名）
  - 创建服务器 / 加入服务器 单选按钮
- 控制面板（ControlBox）
  - 连接 / 创建 / 退出 / 其他 按钮
- 状态栏

**工作模式**:
1. **服务端模式**: 点击"创建"启动服务器，监听端口，accept 客户端连接并广播消息
2. **客户端模式**: 输入服务器IP和端口，点击"连接"加入服务器

#### Server — 服务端管理

**位置**: [chat_room.py#L215-L274](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/chat_room.py#L215-L274)

**职责**:
- 管理 `serverDict` 客户端连接字典
- 消息广播 (`_broadcast`)
- 连接状态管理（新连接自动 spawn 新线程）

#### Client — 客户端管理

**位置**: [chat_room.py#L279-L317](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/chat_room.py#L279-L317)

**职责**:
- 管理客户端 TCP 连接
- 向服务端发送消息
- 接收并显示服务端广播

#### ServerThread / ClientThread — 网络通信线程

| 类 | 位置 | 继承 | 信号 |
|----|------|------|------|
| `ServerThread` | [L127-L176](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/chat_room.py#L127-L176) | `QThread` | `_signal` / `_text` / `_flag` (均为 `pyqtSignal(str)`) |
| `ClientThread` | [L181-L210](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/chat_room.py#L181-L210) | `QThread` | `_signal` / `_text` / `_flag` (均为 `pyqtSignal(str)`) |

#### WebWindow — 内嵌浏览器

**位置**: [chat_room.py#L22-L55](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/chat_room.py#L22-L55)

**继承**: `QMainWindow`

**功能**: 基于 `QWebEngineView` 的简易浏览器，加载 `https://hopestudio.top/`。

**特性**:
- 状态栏显示加载进度百分比
- 加载失败时显示友好错误页面（替代默认空白页）
- 在 `OtherWindow._open_web` 和 `ShitWindow._open_web` 中有 try/except 回退到系统浏览器

#### OtherWindow — "其他"功能入口

**位置**: [chat_room.py#L83-L122](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/chat_room.py#L83-L122)

**继承**: `QMainWindow`

**功能**: 提供开发日志和简易官网两个入口按钮，子窗口通过实例属性持有引用。

#### LogWindow — 开发日志

**位置**: [chat_room.py#L60-L78](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/chat_room.py#L60-L78)

**继承**: `QMainWindow`，500×300 只读文本窗口。

---

## 5. 关键类与函数

### 5.1 类关系图

```
hopekitmain.py
├── resource_path()             # 资源路径处理
├── config_path()               # 配置路径处理
├── ThemeManager                # MD3 主题管理器（普通类）
├── CaidanWindow(QMainWindow)   # 彩蛋
├── ShutWindow(QDialog)         # 关机命令
├── ShitWindow(QDialog)         # 系统工具探索
├── Calculator(QDialog)         # 计算器
├── CopyrightWindow(QMainWindow)# 版权声明
├── SettingsDialog(QDialog)     # 设置对话框
└── MainUi(QMainWindow)         # 主界面

chat_room.py
├── WebWindow(QMainWindow)      # 内嵌浏览器
├── LogWindow(QMainWindow)      # 开发日志
├── OtherWindow(QMainWindow)    # "其他"功能入口
├── ServerThread(QThread)       # 服务端线程
├── ClientThread(QThread)       # 客户端线程
├── Server                      # 服务端管理（普通类）
├── Client                      # 客户端管理（普通类）
└── MainWin(QMainWindow)        # 聊天室主窗口

Styles/styles.py
├── global_stylesheet(colors)   # 全局 QSS 样式表
├── main_stylesheet(colors)     # 主窗口专属样式表
└── dialog_stylesheet(colors)   # 对话框样式表
```

### 5.2 MainUi 核心方法

| 方法 | 签名 | 功能 |
|------|------|------|
| `__init__` | `()` | 初始化主界面，创建子窗口引用占位 |
| `_build_ui` | `()` | 构建侧边栏 + 堆叠内容区 |
| `_build_tools_page` | `()` | 构建工具分类页 |
| `_build_links_page` | `()` | 构建链接分类页 |
| `_build_calendar_page` | `()` | 构建日历分类页 |
| `_switch_page` | `(idx)` | 切换堆叠页并高亮导航按钮 |
| `_toggle_sidebar` | `()` | 折叠/展开侧边栏 |
| `_open_settings` | `()` | 打开设置对话框，切换后刷新所有子窗口样式 |
| `_apply_style` | `()` | 应用全局 + 主窗口样式表 |
| `_global_stylestring` | `@staticmethod` | 返回全局样式表字符串供子窗口复用 |
| `_open_chat` | `()` | 惰性创建并打开聊天室窗口 |
| `_open_caidan` | `()` | 惰性创建并打开彩蛋窗口 |
| `_open_calc` | `()` | 惰性创建并打开计算器 |
| `_open_shit` | `()` | 惰性创建并打开系统工具探索 |
| `_open_copyright` | `()` | 惰性创建并打开版权声明 |
| `_open_website` | `@staticmethod` | 系统浏览器打开官网 |
| `_open_qq_group` | `@staticmethod` | 系统浏览器打开QQ群 |
| `_open_sports` | `@staticmethod` | 系统浏览器打开亚运 |
| `_open_bilibili` | `@staticmethod` | 系统浏览器打开B站 |
| `_open_blog` | `@staticmethod` | 系统浏览器打开博客 |
| `_open_github` | `@staticmethod` | 系统浏览器打开GitHub |

### 5.3 ThemeManager 核心方法

| 方法 | 签名 | 功能 |
|------|------|------|
| `__init__` | `()` | 初始化为 auto 模式并加载配置 |
| `mode` | `@property` | 返回当前模式 (`auto`/`light`/`dark`) |
| `is_dark` | `@property` | 返回当前是否深色模式 |
| `colors` | `@property` | 返回完整调色板 dict |
| `set_mode` | `(mode)` | 设置模式并保存 |
| `load` | `()` | 从 `theme.json` 加载模式 |
| `save` | `()` | 保存模式到 `theme.json` |
| `_read_windows_accent` | `@staticmethod` | 读取注册表获取 Windows 强调色 (r,g,b) |
| `_read_windows_dark_mode` | `@staticmethod` | 读取注册表判断系统深浅色 |
| `_build_palette` | `@classmethod` | 根据 accent + dark 生成完整 MD3 调色板 |
| `_mix` | `@staticmethod` | 线性混合两个 RGB 颜色 |
| `_luminance` | `@staticmethod` | 计算相对亮度 |
| `_on_color` | `@classmethod` | 根据背景亮度返回黑/白前景色 |

### 5.4 Server / Client 核心方法

#### Server

| 方法 | 签名 | 功能 |
|------|------|------|
| `__init__` | `(widget, ip, host, port)` | 初始化服务端 |
| `_build_socket` | `()` | 创建 Socket、bind、listen |
| `_spawn_thread` | `()` | 创建新 ServerThread 监听连接 |
| `_broadcast` | `(info)` | 广播消息到所有客户端 |
| `btnsend` | `(text)` | 服务端发送消息（本地显示+广播） |
| `closeThread` | `()` | 关闭所有服务线程 |
| `_on_flag` | `(flag)` | 处理连接状态标志 |
| `_on_message` | `(signal)` | 处理状态消息 |
| `_on_text` | `(text)` | 处理收到的文本（显示+广播） |

#### Client

| 方法 | 签名 | 功能 |
|------|------|------|
| `__init__` | `(widget, ip, hostName, port)` | 初始化客户端 |
| `_build_socket` | `()` | 创建 Socket 并连接服务器 |
| `btnsend` | `(text)` | 向服务端发送消息 |
| `closeThread` | `()` | 关闭线程 |
| `_on_flag` | `(flag)` | 处理连接标志 |
| `_on_message` | `(signal)` | 处理状态消息 |
| `_on_text` | `(text)` | 处理收到的文本 |

### 5.5 信号与槽机制

**ServerThread → Server**:
| 信号 | 槽函数 | 格式 |
|------|--------|------|
| `_flag` | `_on_flag()` | `"serverID@@@connect\|disconnect"` |
| `_signal` | `_on_message()` | `"serverID@@@状态消息"` |
| `_text` | `_on_text()` | 聊天文本 |

**ClientThread → Client**:
| 信号 | 槽函数 | 格式 |
|------|--------|------|
| `_flag` | `_on_flag()` | `"connect"` / `"disconnect"` |
| `_signal` | `_on_message()` | 状态消息 |
| `_text` | `_on_text()` | 聊天文本 |

### 5.6 消息格式

| 消息类型 | 格式 | 示例 |
|----------|------|------|
| 连接标志 | `serverID@@@connect/disconnect` | `"0@@@connect"` |
| 状态信号 | `serverID@@@message` | `"0@@@等待用户加入……"` |
| 聊天消息 | `昵称:\n消息内容` | `"张三:\n你好"` |

---

## 6. 主题系统

### 6.1 工作流程

```
1. 程序启动
   │
   ▼
2. ThemeManager.__init__()
   ├── load() → 从 theme.json 读取上次模式
   └── 默认 "auto"
   │
   ▼
3. 用户点击"设置" → SettingsDialog
   ├── 选择 auto / light / dark
   └── 点击"应用"
   │
   ▼
4. theme.set_mode(mode) → save() 写入 theme.json
   │
   ▼
5. MainUi._apply_style()
   ├── theme.colors → 读取 Windows 强调色 + 深浅判断
   ├── _build_palette() → 生成 25+ 颜色 token
   ├── app.setStyleSheet(global_stylesheet) → 全局样式
   └── self.setStyleSheet(main_stylesheet) → 主窗口样式
   │
   ▼
6. 已打开的子窗口也同步刷新样式
```

### 6.2 调色板生成算法

1. **读取 Windows 强调色**: 从注册表 `HKEY_CURRENT_USER\Software\Microsoft\Windows\DWM` 的 `AccentColor` 值（ABGR 格式）提取 RGB
2. **读取深浅色**: 从注册表 `...\Themes\Personalize` 的 `AppsUseLightTheme` 判断
3. **颜色混合**: 通过 `_mix(c1, c2, t)` 线性插值，从 accent 色派生 primary_container、secondary、sidebar 等变体
4. **对比度计算**: 通过 `_luminance()` 计算背景亮度，自动选择黑/白前景色

### 6.3 持久化

主题模式保存在 [theme.json](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/theme.json) 中：
```json
{
  "mode": "auto"
}
```

---

## 7. 样式系统

### 7.1 Styles 模块

**位置**: [Styles/styles.py](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/Styles/styles.py)

三个纯函数，接收 `colors` dict 返回 QSS 字符串：

| 函数 | 位置 | 应用范围 | 覆盖控件 |
|------|------|----------|----------|
| `global_stylesheet(colors)` | [L1-L55](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/Styles/styles.py#L1-L55) | `QApplication` 全局 | QWidget, QGroupBox, QPushButton, QLineEdit, QTextEdit, QLabel, QStatusBar |
| `main_stylesheet(colors)` | [L58-L212](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/Styles/styles.py#L58-L212) | `MainUi` 主窗口 | 侧边栏、导航按钮、退出/设置按钮、页面标题、日历、菜单栏、滚动条 |
| `dialog_stylesheet(colors)` | [L215-L265](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/Styles/styles.py#L215-L265) | `SettingsDialog` | QDialog, QGroupBox, QRadioButton, QPushButton, QLabel |

### 7.2 样式应用策略

```
QApplication (全局样式)  ← global_stylesheet()
     │
     ├── MainUi (主窗口样式)  ← main_stylesheet()
     │    ├── 子窗口 (复用全局样式)  ← _global_stylestring()
     │    └── ...
     │
     └── SettingsDialog (对话框样式)  ← dialog_stylesheet()
```

### 7.3 MD3 样式特点

| 控件 | MD3 风格特点 |
|------|-------------|
| 按钮 | 圆角 20px，hover 使用 primary_container |
| 卡片 | 圆角 16px，surface 背景 |
| 导航按钮 | 圆角 28px，选中时高亮 primary 色 |
| 侧边栏 | 折叠/展开动画，深色模式下带 accent 混合 |
| 退出按钮 | 使用 error 色（红色），hover 提亮 |
| 滚动条 | 细窄 10px，圆角 5px，hover 加深 |

---

## 8. 网络通信机制

### 8.1 通信协议

- **协议**: TCP (SOCK_STREAM)
- **地址族**: IPv4 (AF_INET)
- **编码**: UTF-8
- **缓冲区大小**: 1024 字节

### 8.2 服务端工作流程

```
1. 创建 Socket → bind(ip, port) → listen(5)
   │
   ▼
2. _spawn_thread() → 创建 ServerThread 并 start()
   │
   ▼
3. ServerThread.run() → accept() 阻塞等待连接
   │
   ├── 连接成功 → emit _flag("connect")
   │              └── Server._on_flag → _spawn_thread() (再开一个线程等下一个)
   │
   ▼
4. _receive_loop() → recv(1024) 循环接收
   │
   ├── 收到消息 → emit _text → Server._on_text → _broadcast()
   │                                                └── 遍历所有 client 发送
   │
   └── 连接断开 → emit _flag("disconnect")
                  └── Server._on_flag → runflag = False
```

### 8.3 客户端工作流程

```
1. 创建 Socket → connect(ip, port)
   │
   ├── 成功 → emit _flag("connect") → 启动 ClientThread
   │
   └── 失败 → emit _flag("disconnect") + emit _signal(错误原因)
   │
   ▼
2. ClientThread.run() → recv(1024) 循环接收
   │
   ├── 收到消息 → emit _text → Client._on_text → 显示在聊天框
   │
   └── 连接断开 → emit _flag("disconnect") → runflag = False
```

### 8.4 广播机制

服务端收到任意客户端消息后：
1. 将消息追加到本地聊天记录
2. 遍历 `serverDict` 中所有活跃连接
3. 逐个调用 `sendToClient()` 发送消息
4. 发送失败则标记该客户端断开

---

## 9. 依赖关系

### 9.1 Python 依赖

| 库名 | 用途 | 声明文件 |
|------|------|----------|
| `PyQt5` | GUI 框架（QtWidgets/QtCore/QtGui） | [requirements.txt](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/requirements.txt#L1) |
| `PyQtWebEngine` | 内嵌浏览器 (QWebEngineView) | [requirements.txt](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/requirements.txt#L2) |
| `socket` | TCP 网络通信 (标准库) | — |
| `json` | 主题配置读写 (标准库) | — |
| `os` | 路径操作 (标准库) | — |
| `subprocess` | 执行外部命令 (标准库) | — |
| `sys` | 系统退出、打包检测 (标准库) | — |
| `winreg` | 读取 Windows 注册表 (标准库，仅 Windows) | — |

### 9.2 资源依赖

| 文件 | 用途 |
|------|------|
| [logo.jpg](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/logo.jpg) | 主界面 Logo 图标 |
| [theme.json](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/theme.json) | 主题模式持久化 |

### 9.3 模块间导入关系

```
hopekitmain.py
├── imports → chat_room (MainWin, OtherWindow, WebWindow)
└── imports → Styles.styles (styles 函数)

chat_room.py
└── imports → PyQt5.QtWebEngineWidgets (延迟导入，运行时加载)

Styles/styles.py
└── 无外部依赖（纯函数，接收 dict 返回 str）
```

### 9.4 安装依赖

```bash
pip install -r requirements.txt
```

或手动安装：
```bash
pip install PyQt5>=5.15 PyQtWebEngine>=5.15
```

---

## 10. 项目运行方式

### 10.1 环境要求

- **Python 版本**: Python 3.10+（使用了 `dict[str, ServerThread]` 等类型注解语法）
- **操作系统**: Windows（注册表读取依赖 `winreg`，其他系统需回退默认色）
- **依赖库**: PyQt5, PyQtWebEngine

### 10.2 运行步骤

1. **安装依赖**:
   ```bash
   pip install -r requirements.txt
   ```

2. **运行主程序**:
   ```bash
   python hopekitmain.py
   ```

3. **程序入口**: [hopekitmain.py#L888-L894](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py#L888-L894)

   ```python
   if __name__ == "__main__":
       QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
       app = QtWidgets.QApplication([])
       window = MainUi()
       window.show()
       sys.exit(app.exec_())
   ```

   > **注意**: `AA_ShareOpenGLContexts` 必须在 `QApplication` 创建前设置，否则 QtWebEngineWidgets 无法初始化。

### 10.3 聊天室使用流程

**作为服务端**:
1. 点击主界面"聊天室"按钮
2. 确保选中"创建服务器"
3. 点击"获取本机IP"或手动输入IP
4. 设置端口（默认 1145）和昵称
5. 点击"创建"按钮启动服务器
6. 等待其他客户端连接

**作为客户端**:
1. 点击主界面"聊天室"按钮
2. 选择"加入服务器"
3. 输入服务器 IP、端口、昵称
4. 点击"连接"按钮加入

### 10.4 主题切换

1. 点击侧边栏"设置"按钮
2. 选择 auto / light / dark
3. 点击"应用"立即生效

---

## 11. 打包部署

### 11.1 PyInstaller 配置

**配置文件**: [HopeTeams.spec](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/HopeTeams.spec)

**关键配置**:
- **入口脚本**: `hopekitmain.py`
- **数据文件**: `logo.jpg`, `theme.json`（通过 `datas` 参数打包）
- **UPX 压缩**: 启用（`upx=True`）
- **控制台**: 禁用（`console=False`）
- **输出目录**: `dist/HopeTeams/`

### 11.2 打包命令

```bash
pyinstaller HopeTeams.spec
```

### 11.3 打包输出

```
dist/HopeTeams/
├── HopeTeams.exe              # 主程序可执行文件
└── _internal/
    ├── python312.dll          # Python 运行时
    ├── base_library.zip       # Python 标准库
    ├── PyQt5/                 # PyQt5 依赖（Qt5 动态库、插件等）
    ├── logo.jpg               # 资源文件
    └── theme.json             # 配置文件
```

### 11.4 运行打包后的程序

直接双击 `dist/HopeTeams/HopeTeams.exe` 即可运行。

---

## 12. 已知问题与注意事项

### 12.1 安全问题

1. **eval 注入风险**: 计算器使用 `eval()` 执行用户输入（[hopekitmain.py#L388](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py#L388)），理论上可执行任意 Python 代码
2. **关机命令**: `ShutWindow` 执行 `shutdown -i`，需谨慎使用

### 12.2 功能限制

1. **聊天室无用户名冲突检测**: 多人使用相同昵称会混淆
2. **消息长度限制**: 单条消息最大 1024 字节
3. **不支持文件传输**: 仅支持文本消息
4. **无消息历史持久化**: 关闭程序后聊天记录丢失
5. **三个禁用按钮**: AI机器人、查火车票、外部工具已 `setEnabled(False)`

### 12.3 平台兼容性

- `winreg` 模块仅 Windows 可用，其他系统会回退到默认紫色 `(103, 80, 164)`
- `subprocess.call(["shutdown", ...])` 仅 Windows 可用
- QtWebEngine 在部分 Linux 发行版可能需要额外安装系统依赖

### 12.4 代码质量

1. **混合命名**: 部分类名使用中文拼音（`CaidanWindow`、`ShitWindow`）
2. **消息分隔符脆弱**: 使用 `@@@` 字符串拼接传递多字段信息
3. **网络异常处理简单**: 仅捕获 Exception 显示原因，无重连机制

### 12.5 已移除内容

| 模块 | 移除原因 |
|------|----------|
| `ticket` | 火车票查询（未启用） |
| `ChatGPT` | AI机器人（余额用尽，含泄露的 API Key） |
| `tool_ex` | 外部工具箱（含泄露的 API Key） |
| 一键关机按钮 | 安全风险 |

---

## 附录：类索引

### hopekitmain.py

| 类名 | 行号 | 功能 |
|------|------|------|
| `ThemeManager` | [L51](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py#L51) | MD3 主题管理器 |
| `CaidanWindow` | [L280](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py#L280) | 彩蛋窗口 |
| `ShutWindow` | [L306](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py#L306) | 关机命令集 |
| `ShitWindow` | [L318](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py#L318) | 系统工具探索 |
| `Calculator` | [L357](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py#L357) | 计算器 |
| `CopyrightWindow` | [L402](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py#L402) | 版权声明 |
| `SettingsDialog` | [L439](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py#L439) | 设置对话框 |
| `MainUi` | [L518](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py#L518) | 主界面 |

### chat_room.py

| 类名 | 行号 | 功能 |
|------|------|------|
| `WebWindow` | [L22](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/chat_room.py#L22) | 内嵌浏览器 |
| `LogWindow` | [L60](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/chat_room.py#L60) | 开发日志 |
| `OtherWindow` | [L83](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/chat_room.py#L83) | "其他"功能入口 |
| `ServerThread` | [L127](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/chat_room.py#L127) | 服务端线程 |
| `ClientThread` | [L181](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/chat_room.py#L181) | 客户端线程 |
| `Server` | [L215](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/chat_room.py#L215) | 服务端管理 |
| `Client` | [L279](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/chat_room.py#L279) | 客户端管理 |
| `MainWin` | [L322](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/chat_room.py#L322) | 聊天室主窗口 |

### Styles/styles.py

| 函数 | 行号 | 功能 |
|------|------|------|
| `global_stylesheet` | [L1](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/Styles/styles.py#L1) | 全局 QSS 样式表 |
| `main_stylesheet` | [L58](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/Styles/styles.py#L58) | 主窗口专属样式表 |
| `dialog_stylesheet` | [L215](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/Styles/styles.py#L215) | 对话框样式表 |

---

*文档生成时间: 2026-07-11*  
*基于 HopeKit 2.0.0-revived 版本分析*
