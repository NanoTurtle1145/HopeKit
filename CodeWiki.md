# HopeKit Code Wiki

> **项目名称**: HopeKit
> **版本**: 2.1.0
> **主入口**: [hopekitmain.py](hopekitmain.py)
> **打包配置**: [HopeKit.spec](HopeKit.spec)
> **版本文件**: [hopekit/version.py](hopekit/version.py)

---

## 1. 多风格主题系统

### 1.1 概述

`ThemeManager`（`hopekit/theme.py`）是 HopeKit 最核心的模块，支持 **9 种 UI 风格** × **3 种深浅模式**。配置持久化到 `theme.json`。

### 1.2 风格列表

| 风格 | 常量值 | 设计语言 | 视觉特征 |
|------|--------|----------|----------|
| Material Design 3 | `md3` | Google MD3 (2021+) | 动态强调色 + 大圆角 (20/16/28px) + tonal palette |
| Material Design 2 | `md2` | Google MD2 (2014) | Indigo 500 主色 + 扁平 4px 圆角 + Pink A200 强调色 |
| Qt 原生 | `qt` | Qt 默认控件外观 | 几乎不写 QSS，仅侧边栏/退出按钮有样式 |
| WinUI3 / Fluent | `winui3` | Microsoft WinUI3 | 系统强调色 + 分层圆角 (4/8/16px) + Mica/Acrylic 背景 + Segoe UI Variable 字体 |
| Win10 Fluent | `win10fluent` | 早期 Fluent (2017) | 静态色板 + 4px 圆角 + 左侧主题色竖条选中态 |
| GNOME / libadwaita | `gnome` | GNOME 桌面 | Cantarell 字体 + 纯色背景 + 6/12px 圆角 + 无边框按钮 |
| KDE Plasma / Breeze | `kde` | KDE 桌面 | Noto Sans + 半透明 sidebar + 4/8px 圆角 + 带边框按钮 |
| macOS / Cupertino | `cupertino` | Apple HIG | SF Pro 字体 + 8/12px 圆角 + 系统灰按钮 + 实心选中态 |
| ChromeOS / Material | `chromeos` | Google ChromeOS | Google Sans + 8/12px 圆角 + 类似 MD3 但圆角更小 |

### 1.3 深浅模式

| 模式 | 说明 |
|------|------|
| `auto` | 跟随 Windows 系统主题（读取注册表 `AppsUseLightTheme`） |
| `light` | 固定浅色模式 |
| `dark` | 固定深色模式 |

### 1.4 生命周期

```
程序启动
  → ThemeManager.__init__()
    → load() 从 theme.json 读取上次 style/mode
    → 默认: style="md3", mode="auto"

用户操作
  → SettingsPage 选中新 style/mode
    → ThemeManager.set_style() / set_mode()
      → save() 写入 theme.json
      → MainUi._apply_style()
        → app.setStyleSheet( global QSS )
        → self.setStyleSheet( main QSS )
        → _refresh_child_window_styles() 刷新所有子窗口
```

### 1.5 Windows 系统色读取

在 `auto` 模式下，从注册表读取用户的系统配色：

**强调色**（所有风格共用）：
- 路径：`HKEY_CURRENT_USER\Software\Microsoft\Windows\DWM`
- 键：`AccentColor`（ABGR 格式）
- 提取：`R = value & 0xFF`, `G = (value >> 8) & 0xFF`, `B = (value >> 16) & 0xFF`
- 回退值：`(33, 150, 243)` — Material Blue 500

**深浅色**（`auto` 模式专用）：
- 路径：`HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize`
- 键：`AppsUseLightTheme`
- 0 = 深色，1 = 浅色

非 Windows 系统回退到浅色模式。

### 1.6 颜色算法

所有风格的调色板通过 3 个基础算法从 accent 色派生：

**`_mix(c1, c2, t)`** — 线性插值混合
```python
def _mix(c1, c2, t):
    return (
        round(c1[0] + (c2[0] - c1[0]) * t),
        round(c1[1] + (c2[1] - c1[1]) * t),
        round(c1[2] + (c2[2] - c1[2]) * t),
    )
```

**`_luminance(rgb)`** — 相对亮度（WCAG 标准）
```python
def _luminance(rgb):
    def chan(v):
        v = v / 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * chan(rgb[0]) + 0.7152 * chan(rgb[1]) + 0.0722 * chan(rgb[2])
```

**`_on_color(bg)`** — 自动选择黑/白前景色
```python
def _on_color(bg):
    return "#FFFFFF" if _luminance(bg) < 0.5 else "#000000"
```

**`_rgba(rgb, alpha)`** — 生成 `rgba()` 字符串（用于半透明效果）
```python
def _rgba(rgb, alpha):
    r, g, b = int(rgb[0]), int(rgb[1]), int(rgb[2])
    return f"rgba({r},{g},{b},{alpha})"
```

### 1.7 调色板 Token 说明

每个风格生成的 `colors` 字典包含以下 25+ 个 token：

| Token | 用途 | 示例值 (MD3 Light) |
|-------|------|-------------------|
| `primary` | 主色（强调色） | `#2196F3` |
| `on_primary` | 主色上文字 | `#FFFFFF` 或 `#000000` |
| `primary_container` | 主色容器（选中态背景） | 混合 accent + white 78% |
| `on_primary_container` | 容器上文字 | 暗色 accent |
| `secondary` | 次要色 | 混合 accent + grey |
| `on_secondary` | 次要色上文字 | auto |
| `secondary_container` | 次要容器（hover 背景） | 混合 accent + grey |
| `on_secondary_container` | 次要容器文字 | grey |
| `surface` | 卡片/控件表面色 | `#FFFBFA` |
| `on_surface` | 表面文字色 | `#1C1B1F` |
| `surface_variant` | 变体表面色（次要卡片） | `#E7E0EC` |
| `on_surface_variant` | 变体表面文字 | `#49454F` |
| `background` | 窗口背景色 | `#FFFBFA` |
| `on_background` | 背景上文字色 | `#1C1B1F` |
| `outline` | 边框色 | `#79747E` |
| `outline_variant` | 变体边框色 | `outline` + `surface` 50% 混合 |
| `error` | 错误/危险操作色 | 红色系 |
| `on_error` | 错误色上文字 | `#FFFFFF` |
| `shadow` | 阴影色 | `#000000` |
| `sidebar_bg` | 侧边栏背景 | accent 混合背景 |
| `sidebar_text` | 侧边栏文字 | `on_surface` |
| `sidebar_hover` | 侧边栏 hover | 半透明混合 |
| `sidebar_active` | 侧边栏选中 | 半透明混合 |
| `sidebar_active_border` | 侧边栏选中边框 | `primary` |
| `exit_btn_bg` | 退出按钮背景 | `error` |
| `exit_btn_hover` | 退出按钮 hover | `error` + 混合 |
| `card_radius` | 卡片圆角 | 风格相关 |
| `btn_radius` | 按钮圆角 | 风格相关 |
| `nav_radius` | 导航项圆角 | 风格相关 |

### 1.8 各风格配色差异

| 特性 | MD3 | MD2 | Qt | WinUI3 | Win10Fluent | GNOME | KDE | Cupertino | ChromeOS |
|------|-----|-----|----|--------|-------------|-------|-----|-----------|-----------|
| 动态强调色 | ✅ | ❌ 固定 Indigo | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 主色来源 | DWM accent | `#3F51B5` | DWM accent | DWM accent | DWM accent | DWM accent | DWM accent | DWM accent | DWM accent |
| sidebar 选中 | primary_container 半透明 | primary_light 实色 | accent 40% | accent 60% 半透明 | 左侧边框+文字色 | accent 15% | accent 20% | 实心 accent | accent 15% |
| 按钮背景 | primary 实心 | primary 实心 | 系统默认 | surface + 边框 | primary 实心 | 透明无边框 | surface + 边框 | surface_variant | primary 实心 |
| 按钮圆角 | 20px | 4px | 0px | 4px | 4px | 6px | 4px | 8px | 8px |
| 卡片圆角 | 16px | 4px | 0px | 8px | 4px | 12px | 8px | 12px | 12px |
| 导航圆角 | 28px | 4px | 0px | 16px | 4px | 12px | 8px | 12px | 12px |
| 字体 | 默认 | 默认 | 系统默认 | Segoe UI Variable | Segoe UI | Cantarell | Noto Sans | SF Pro | Google Sans |
| 材质效果 | ❌ | ❌ | ❌ | Mica/Acrylic | Acrylic | ❌ | 半透明 sidebar | ❌ | ❌ |

---

## 2. Windows 原生模糊材质

### 2.1 概述

`hopekit/mica.py` 封装了 Windows DWM（桌面窗口管理器）材质 API，为 WinUI3 主题提供原生模糊背景。支持 Win11 新路径和 Win10 老路径自动降级。

### 2.2 材质分工（WinUI3 规范）

| 材质 | 用途 | 效果 |
|------|------|------|
| **Mica** | 主窗口背景 | 模糊桌面壁纸，仅绘制一次（性能友好） |
| **Mica Alt** | Tabbed 标题栏 | Mica 变体，色调更深 |
| **Acrylic** | 弹窗/Flyout/Toast | 实时模糊应用后方内容（性能敏感） |
| **Smoke** | 模态遮罩 | 纯 QSS `rgba(0,0,0,0.3)`，不涉及 DWM |

### 2.3 系统版本路径

```
系统检测
  ├─ Win11 build ≥ 22621  → DWMWA_SYSTEMBACKDROP_TYPE=38 (新 API)
  │    val=2 → Mica (DWMSBT_MAINWINDOW)
  │    val=3 → Acrylic (DWMSBT_TRANSIENT)
  │    val=4 → MicaAlt (DWMSBT_TABBED)
  │
  ├─ Win11 build 22000~22620 → DWMWA_MICA=1029 (老接口，仅 Mica)
  │
  ├─ Win10 build ≥ 1803  → SetWindowCompositionAttribute (老路径)
  │    state=4 → ACCENT_ENABLE_ACRYLICBLURBEHIND (优先)
  │    state=5 → 备用值（部分版本）
  │    state=3 → ACCENT_ENABLE_BLURBEHIND (退化)
  │
  └─ 更老 / 非 Windows → 纯色降级
```

### 2.4 关键 API

**新路径（Win11 22621+）**：
```python
val = DWORD(2)  # DWMSBT_MAINWINDOW = Mica
dwm.DwmSetWindowAttribute(hwnd, 38, val, sizeof(val))
```

**老路径（Win10）**：
```python
policy = AccentPolicy(
    AccentState=4,  # ACCENT_ENABLE_ACRYLICBLURBEHIND
    AccentFlags=2,  # 全窗口
    GradientColor=ARGB(a, r, g, b),
)
user32.SetWindowCompositionAttribute(hwnd, data)
```

**暗色标题栏**：
```python
val = DWORD(1 if dark else 0)
dwm.DwmSetWindowAttribute(hwnd, 20, val, sizeof(val))  # DWMWA_USE_IMMERSIVE_DARK_MODE
```

**扩展 Frame**（Acrylic 需要）：
```python
margins = MARGINS(-1, -1, -1, -1)  # 全窗口
dwm.DwmExtendFrameIntoClientArea(hwnd, margins)
```

### 2.5 统一入口

```python
from hopekit.mica import apply_backdrop, apply_to_window

# 底层入口
ok, msg = apply_backdrop(hwnd, kind="mica", dark=True)

# QWidget 便捷入口
apply_to_window(window, kind="acrylic", dark=False)
```

### 2.6 MainUi 中的正确时序

```
__init__()
  ├─ 检测 theme.style == "winui3"
  ├─ setAttribute(WA_TranslucentBackground, True)    ← show() 前！
  └─ _build_ui()
       └─ central.setAttribute(WA_NoSystemBackground, True)
       └─ central.setAttribute(WA_StyledBackground, True)

show()
  ↓
showEvent(e)
  ├─ if e.spontaneous(): return          ← 过滤系统触发
  ├─ if _mica_applied: return            ← 防重复
  ├─ hwnd = int(self.winId())             ← 拿到真 HWND
  ├─ mica.apply_backdrop(hwnd, kind="acrylic", dark=theme.is_dark)
  └─ _mica_applied = True
```

### 2.7 常见翻车对照

| 现象 | 根因 | 修法 |
|------|------|------|
| 窗口黑底 | 没设 `WA_TranslucentBackground` | show 前 `setAttribute(WA_TranslucentBackground)` |
| 窗口灰底/蒙灰 | `autoFillBackground` 还在填 palette | `central.setAutoFillBackground(False)` |
| 材质效果溢出边界 | 没设 `WA_TranslucentBackground` | 确保 show 前设置 |
| Win10 上 Mica 不可用 | Win10 没有 Mica API | 自动降级 Acrylic |

详见完整文档：[docs/WINUI3_TRANSPARENCY_GUIDE.md](docs/WINUI3_TRANSPARENCY_GUIDE.md)

---

## 3. 主窗口架构

### 3.1 MainUi 布局

`hopekit/main_window.py` 的 `MainUi` 类实现完整的主窗口：

```
┌─────────────────────────────────────────────────┐
│ ┌───────────┐ ┌──────────────────────────────┐  │
│ │  Sidebar  │ │    Content Area               │  │
│ │           │ │  ┌─────────────────────────┐  │  │
│ │  HopeKit  │ │  │  Header (Logo + 标题)   │  │  │
│ │  [◀]     │ │  └─────────────────────────┘  │  │
│ │           │ │  ┌─────────────────────────┐  │  │
│ │  🛠 tools │ │  │  QStackedWidget         │  │  │
│ │  🔗 links│ │  │  ├─ tools page          │  │  │
│ │  📅 cal  │ │  │  ├─ links page          │  │  │
│ │  ─────── │ │  │  ├─ calendar page       │  │  │
│ │  ▼ 设置  │ │  │  └─ SettingsPage        │  │  │
│ │    ● 主题│ │  │                         │  │  │
│ │    ○ 关于│ │  │                         │  │  │
│ │           │ │  └─────────────────────────┘  │  │
│ │  退出     │ │                               │  │
│ └───────────┘ └──────────────────────────────┘  │
│ ┌──────────────────────────────────────────────┐  │
│ │  StatusBar                                   │  │
│ └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

### 3.2 侧边栏结构

- **展开宽度**: 240px，**折叠宽度**: 56px
- **顶部**: 标题 "HopeKit" + 折叠按钮 `◀`/`▶`
- **中部**: 可滚动导航区域
  - 分类按钮（从 ModuleRegistry 动态生成）
  - 分割线
  - 设置二级菜单（可折叠）：主题 / 关于
- **底部**: 退出按钮

### 3.3 分类页面生成

每个分类对应一个 `_build_category_page()` 构建的页面：

- **page 型插件**（`kind="page"`）：直接嵌入页面内
- **window 型插件**: 
  - `tools` / 普通分类：2 列按钮网格 `_build_tools_grid()`
  - `links` 分类：带标题+查看按钮的列表 `_build_links_list()`

### 3.4 设置面板架构

`hopekit/settings_page.py` 实现嵌入式设置面板：

```
┌──────────────────────────────────────────┐
│ ┌──────────┐ ┌─────────────────────────┐ │
│ │ 设置      │ │  主题风格               │ │
│ │          │ │  ○ MD3  ○ MD2  ○ Qt     │ │
│ │ ● 主题   │ │  ○ WinUI3  ○ GNOME      │ │
│ │ ○ 关于   │ │  ○ KDE  ○ Cupertino     │ │
│ │          │ │  ○ ChromeOS              │ │
│ │          │ │  深浅模式                │ │
│ │          │ │  ○ auto  ○ 浅  ○ 深      │ │
│ │          │ │  当前: winui3 / light     │ │
│ │          │ │              [+] 导入主题 │ │
│ └──────────┘ └─────────────────────────┘ │
└──────────────────────────────────────────┘
```

子页面：
- **ThemePage**: 主题风格（8 个 RadioButton 实时切换）+ 深浅模式 + 导入主题文件
- **AboutPage**: 关于页面（预留）

### 3.5 样式应用链

```
theme 切换
  → MainUi._apply_style()
    → app.setStyleSheet(styles.global_stylesheet(colors))   ← 全局控件
    → self.setStyleSheet(styles.main_stylesheet(colors))     ← 侧边栏/导航/日历
    → _refresh_child_window_styles()                         ← 所有子窗口
       → 遍历 ModuleRegistry._instances
       → 逐个刷新 setStyleSheet()
```

---

## 4. 双模式路径处理

### 4.1 为什么需要双模式

PyInstaller 打包后，资源路径变化：

| 模式 | 执行文件位置 | 资源位置 |
|------|-------------|----------|
| 开发 | 源码目录 | 源码同级目录 |
| 打包 | `dist/HopeKit/HopeKit.exe` | 临时解压到 `sys._MEIPASS` |

### 4.2 resource_path() — 只读资源

```python
def resource_path(relative: str) -> str:
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS       # 打包后：临时解压目录
    else:
        base = 项目根目录          # 开发时：hopekitmain.py 所在目录
    return os.path.join(base, relative)
```

**用途**: logo.jpg 等只读资源文件。这些文件通过 PyInstaller 的 `datas` 配置打包进 exe。

### 4.3 config_path() — 可读写配置

```python
def config_path(filename: str) -> str:
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)  # 打包后：exe 同目录
    else:
        base = 项目根目录                         # 开发时：源码目录
    return os.path.join(base, filename)
```

**用途**: theme.json 等需要持久化的配置文件。打包后会放在 exe 同目录，方便用户手动修改。

### 4.4 PyInstaller 配置（HopeKit.spec）

```python
a = Analysis(
    ['hopekitmain.py'],
    datas=[('logo.jpg', '.'), ('theme.json', '.')],  # 打包进 exe
    ...
)
exe = EXE(..., name='HopeKit', console=False, upx=True)
```

`console=False` 表示窗口程序（无控制台），`upx=True` 使用 UPX 压缩减小体积。

---

## 5. 插件注册协议

### 5.1 ModuleRegistry

`hopekit/registry.py` 提供装饰器式插件注册。

**注册一个模块**：
```python
from hopekit.registry import ModuleRegistry

@ModuleRegistry.register(
    name="my_tool",        # 唯一标识
    icon="🔧",             # 按钮图标（emoji 或文字）
    title="我的工具",       # 按钮显示文本
    category="tools",      # 所属分类
    kind="window",         # "window"（弹窗）或 "page"（嵌入）
    enabled=True,          # 是否启用
)
def my_tool_factory(main_window):
    # main_window: 主窗口引用
    # 返回: QWidget 实例，或 None（仅执行副作用）
    from my_module import MyDialog
    return MyDialog()
```

### 5.2 注册字段详解

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `name` | `str` | 必填 | 唯一标识符，用于路由和缓存 key |
| `icon` | `str` | `"📦"` | 按钮图标，支持 emoji |
| `title` | `str` | `name` | 按钮显示文本 |
| `category` | `str` | `"tools"` | 所属分类，侧边栏自动分组 |
| `kind` | `str` | `"window"` | `"window"` 弹窗模式 / `"page"` 嵌入模式 |
| `enabled` | `bool` | `True` | 是否启用，`False` 则按钮置灰不可点击 |

### 5.3 两种模块模式

**弹窗型（`kind="window"`）**：
- factory 返回 `QDialog` / `QMainWindow` / `QWidget`
- 点击按钮 → 调用 `_open_module()` → 弹出窗口 → 关闭后实例缓存
- 再次点击 → 复用缓存的实例 → `show()` + `raise_()` + `activateWindow()`

**页面型（`kind="page"`）**：
- factory 返回 `QWidget`
- 直接嵌入分类页的 QStackedWidget 中
- 实例缓存，切换分类时状态保留

**仅执行副作用**：
- factory 返回 `None`
- 适合"打开浏览器链接"等操作（如 `links.py` 中的网站链接）

### 5.4 自动发现机制

```python
def discover_plugins(plugins_dir: str = "plugins") -> int:
    """启动时扫描 plugins/ 目录，import 所有 .py 文件"""
    for filename in sorted(os.listdir(plugins_path)):
        if filename.startswith("_") or not filename.endswith(".py"):
            continue
        module_name = f"plugins.{filename[:-3]}"
        importlib.import_module(module_name)  # 触发 @ModuleRegistry.register 装饰器
    return count
```

规则：
- 忽略 `_` 开头的文件
- 只导入 `.py` 文件
- 按文件名排序 import
- 导入失败打印警告不阻止启动

### 5.5 实例缓存

```python
# 当前所有注册模块
modules = ModuleRegistry.all()

# 按分类获取
tools = ModuleRegistry.by_category("tools")

# 获取或创建实例（带缓存 + 生命周期检查）
instance = ModuleRegistry.get_or_create("my_tool", main_window)

# 清空缓存（主题切换时重建）
ModuleRegistry.clear_instances()
```

`get_or_create()` 的缓存策略：
1. 检查缓存，存在则用 `isVisible()` 探测 C++ 对象是否存活
2. 存活 → 直接返回缓存实例
3. 已被 Qt 析构 → 重建
4. 首次或重建 → 执行 factory 创建并缓存

---

## 6. Qt 兼容层

### 6.1 设计动机

HopeKit 同时支持 PySide6（Qt 官方，LGPL）和 PyQt6（社区，GPL），通过 `hopekit/qt_compat.py` 实现透明兼容。

### 6.2 兼容策略

```python
try:
    from PySide6 import QtWidgets, QtCore, QtGui
    from PySide6.QtCore import Signal, Slot
    QT_LIB = "PySide6"
except ImportError:
    from PyQt6 import QtWidgets, QtCore, QtGui
    from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
    QT_LIB = "PyQt6"
```

两套绑定都通过统一的别名暴露给上层代码。

### 6.3 导出的别名

所有常用 Qt 类直接在模块级别别名化：

```python
QApplication, QMainWindow, QDialog, QWidget, QLabel, QPushButton,
QLineEdit, QTextEdit, QGroupBox, QVBoxLayout, QHBoxLayout, QGridLayout,
QRadioButton, QStatusBar, QMenuBar, QCalendarWidget, QMessageBox,
QFrame, QStackedWidget, QThread, QPixmap
```

枚举常量统一：
```python
PointingHandCursor, AlignCenter, AlignVCenter, AlignLeft, AlignRight,
ScrollBarAlwaysOff, ScrollBarAsNeeded, SmoothTransformation,
WA_TranslucentBackground, WA_StyledBackground, AA_ShareOpenGLContexts,
NoFrame
```

---

## 7. QSS 样式系统

### 7.1 架构

`Styles/styles.py` 为每种风格提供 **3 组 QSS 函数**：

| 函数 | 作用范围 | 调用位置 |
|------|----------|----------|
| `global_stylesheet(colors)` | QApplication 全局 | `app.setStyleSheet()` |
| `main_stylesheet(colors)` | 主窗口（侧边栏/导航/日历/设置面板） | `MainUi.setStyleSheet()` |
| `dialog_stylesheet(colors)` | SettingsDialog 弹窗 | `SettingsDialog.setStyleSheet()` |

### 7.2 运行时路由

```python
def global_stylesheet(colors):
    s = theme.style
    if s == "md2":       return _md2_global(colors)
    if s == "qt":        return _qt_global(colors)
    if s == "winui3":    return _winui3_global(colors)
    # ... 其他风格
    return _md3_global(colors)  # 默认
```

### 7.3 关键 objectName

QSS 使用 `#objectName` 选择器做精确匹配：

| objectName | 组件 | 说明 |
|------------|------|------|
| `#sidebar` | 侧边栏 QFrame | 各风格背景/边框/圆角差异很大 |
| `#sidebarTitle` | 侧边栏标题 QLabel | |
| `#toggleBtn` | 折叠/展开按钮 | |
| `#navScroll` | 导航滚动区 QScrollArea | |
| `#navContainer` | 导航容器 QWidget | |
| `#navGroupHeader` | 设置分组标题 | |
| `#navBtn` | 导航按钮 | 选中态/悬停态各风格不同 |
| `#navDivider` | 组间分割线 | |
| `#exitBtn` | 退出按钮 | hover 变 error 色 |
| `#pageTitle` | 页面标题 | |
| `#contentArea` | 内容区域 | WinUI3 下 transparent |
| `#subNav` | 设置页左侧二级菜单 | |
| `#subNavTitle` | 二级菜单标题 | |
| `#subNavBtn` | 二级菜单按钮 | |
| `#importFab` | 导入主题按钮 | 各风格外观不同（圆形/矩形/实心/半透明） |

---

## 8. 内置插件清单

| 模块名 | 文件 | 分类 | 类型 | 功能 |
|--------|------|------|------|------|
| `caidan` | `plugins/caidan.py` | tools | window | 开发者致敬诗（彩蛋） |
| `calculator` | `plugins/calculator.py` | tools | window | 简易计算器（eval 实现） |
| `calendar` | `plugins/calendar.py` | calendar | page | 日历控件（QCalendarWidget） |
| `chat_room` | `plugins/chat_room_plugin.py` | tools | window | TCP 聊天室（C/S 架构） |
| `copyright` | `plugins/copyright.py` | tools | window | 希望工作室版权声明 |
| `shit` | `plugins/shit_window.py` | tools | window | 探索系统屎山（关机 + 浏览器） |
| `shutdown` | `plugins/shutdown.py` | tools | window | shutdown -i 关机命令 |
| `website` | `plugins/links.py` | links | window | 打开工作室官网（无窗口） |
| `copyright_link` | `plugins/links.py` | links | window | 版权声明（复用 copyright 插件） |
| `qq_group` | `plugins/links.py` | links | window | 加入 QQ 交流群（无窗口） |
| `sports` | `plugins/links.py` | links | window | 在线看亚运（无窗口） |
| `bilibili` | `plugins/links.py` | links | window | 哔哩哔哩主页（无窗口） |
| `blog` | `plugins/links.py` | links | window | 博客（无窗口） |
| `github` | `plugins/links.py` | links | window | GitHub 主页（无窗口） |
| `ai_bot` | `plugins/chat_room_plugin.py` | tools | window | AI 机器人（`enabled=False`） |
| `ticket` | `plugins/chat_room_plugin.py` | tools | window | 查火车票（`enabled=False`） |
| `tool_ex` | `plugins/chat_room_plugin.py` | tools | window | 外部工具（`enabled=False`） |

分类统计：
- **tools**: 11 个（含 3 个 disabled）
- **links**: 7 个
- **calendar**: 1 个

---

## 9. 版本管理

### 9.1 版本号唯一来源

```python
# hopekit/version.py
VERSION = "2.1.0"
```

被统一的导入链引用：
```
hopekit/version.py        → VERSION = "2.1.0"
    ↓ from hopekit.version import VERSION
hopekit/__init__.py       → __version__ = VERSION
    ↓ from hopekit import __version__ as VERSION
hopekitmain.py            → 窗口标题 "HopeKit {VERSION}"
    ↓ from hopekitmain import VERSION
auto_version_commit.py    → 版本变化检测
```

修改版本号只需改 `hopekit/version.py` 一个文件。

### 9.2 自动提交脚本

`auto_version_commit.py` 的工作机制：

```
1. 从 hopekit/version.py 读取当前版本
2. 从 .last_version 读取上次记录的版本
3. 如果版本变化 → git add . → git commit → git push
4. 更新 .last_version 为当前版本
5. --force 模式：跳过版本检测，直接提交推送
```

日志文件：`auto_commit.log`

---

## 10. 工程文件索引

| 文件 | 行数 | 职责 |
|------|------|------|
| `hopekitmain.py` | 38 | 主入口 |
| `hopekit/version.py` | 10 | 版本号 |
| `hopekit/__init__.py` | 34 | 统一导出 |
| `hopekit/qt_compat.py` | 105 | Qt 兼容层 |
| `hopekit/paths.py` | 25 | 路径处理 |
| `hopekit/theme.py` | 898 | 主题管理器 |
| `hopekit/registry.py` | 180 | 插件注册 |
| `hopekit/main_window.py` | 527 | 主窗口 |
| `hopekit/settings_page.py` | 429 | 设置页面 |
| `hopekit/settings_dialog.py` | 112 | 设置弹窗（旧版） |
| `hopekit/mica.py` | 395 | DWM 材质管理 |
| `Styles/styles.py` | 2462 | QSS 样式生成 |
| `demo_acrylic.py` | 150 | Acrylic 独立 Demo |
| `auto_version_commit.py` | 147 | 自动提交脚本 |

---

*HopeKit 2.1.0 — 不是框架，是好用的脚手架。*
