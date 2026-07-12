# HopeKit Code Wiki

> **项目名称**: HopeKit
> **版本**: 2.0.0
> **主入口**: [hopekitmain.py](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/hopekitmain.py)
> **打包配置**: [HopeKit.spec](file:///c:/Documents/Hope%20Teams-revived/Hope-Teams-1.6.8/HopeKit.spec)

---

## 1. MD3 主题系统

### 1.1 核心机制

`ThemeManager` 类实现了 Material Design 3 风格的动态主题系统，支持三种模式：

| 模式 | 说明 |
|------|------|
| `auto` | 跟随 Windows 系统强调色 + 深浅色主题 |
| `light` | 固定浅色模式（使用 Windows 强调色生成调色板） |
| `dark` | 固定深色模式（使用 Windows 强调色生成调色板） |

### 1.2 工作流程

```
1. 程序启动 → ThemeManager.__init__()
   ├── load()  从 theme.json 读取上次模式
   └── 默认 "auto"

2. 用户点击"设置" → 选择模式 → 应用
   ├── theme.set_mode(mode) → save() 写入 theme.json
   └── MainUi._apply_style() 刷新全局样式
```

### 1.3 Windows 强调色读取

从注册表读取系统配色，这是 HopeKit 最有辨识度的特性：

- **强调色**: `HKEY_CURRENT_USER\Software\Microsoft\Windows\DWM` → `AccentColor`（ABGR 格式）
- **深浅色**: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize` → `AppsUseLightTheme`

非 Windows 系统会回退到默认紫色 `(103, 80, 164)`。

### 1.4 调色板生成

通过颜色混合算法，从单一 accent 色派生出 25+ 个颜色 token：

- `primary` / `on_primary` / `primary_container` / `on_primary_container`
- `secondary` / `secondary_container` 等同理
- `surface` / `background` / `outline` / `error` 等基础色
- `sidebar_bg` / `sidebar_hover` / `sidebar_active` 等侧边栏专用色

关键算法：`_mix()` 线性插值、`_luminance()` 相对亮度、`_on_color()` 自动选择黑/白前景。

### 1.5 样式层

样式表由 `Styles/styles.py` 中的三个纯函数生成：

| 函数 | 应用范围 |
|------|----------|
| `global_stylesheet(colors)` | QApplication 全局（按钮、输入框、标签等） |
| `main_stylesheet(colors)` | 主窗口专属（侧边栏、导航按钮、滚动条等） |
| `dialog_stylesheet(colors)` | 设置对话框 |

---

## 2. 双模式路径处理

### 2.1 为什么需要双模式

PyInstaller 打包后，资源路径会发生变化：
- 开发模式：资源在源码同级目录
- 打包模式：资源被嵌入 exe，运行时解压到临时 `_MEIPASS` 目录

HopeKit 提供两个路径函数，分别处理只读资源和可读写配置。

### 2.2 resource_path() — 只读资源

```python
def resource_path(relative: str) -> str:
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS      # 打包后：临时解压目录
    else:
        base = os.path.dirname(os.path.abspath(__file__))  # 开发时：源码目录
    return os.path.join(base, relative)
```

**用途**: logo.jpg 等只读资源。

### 2.3 config_path() — 可读写配置

```python
def config_path(filename: str) -> str:
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)  # 打包后：exe 同目录
    else:
        base = os.path.dirname(os.path.abspath(__file__))  # 开发时：源码目录
    return os.path.join(base, filename)
```

**用途**: theme.json 等需要持久化的配置文件。

---

## 3. 模块注册协议

### 3.1 设计原则

加一个新模块 = 写一个插件文件，主文件零修改。

### 3.2 ModuleRegistry

`hopekit/registry.py` 提供装饰器式注册：

```python
from hopekit.registry import ModuleRegistry

@ModuleRegistry.register("my_tool", icon="🔧", title="我的工具", category="tools")
def my_tool_factory(main_window):
    from my_module import MyWindow
    return MyWindow()
```

### 3.3 注册字段

| 字段 | 说明 |
|------|------|
| `name` | 唯一标识，用于惰性创建的 key |
| `icon` | 按钮图标（emoji 或文字） |
| `title` | 按钮显示文本 |
| `category` | 所属分类：`tools` / `links` / `calendar` |

工厂函数签名：`(main_window) -> QWidget`，接收主窗口引用，返回窗口实例。

### 3.4 自动发现

启动时自动扫描 `plugins/` 目录，通过 `importlib.import_module` 加载所有插件模块，触发装饰器执行注册。侧边栏与工具页按钮由注册表动态生成。

---

*HopeKit — 不是框架，是好用的脚手架。* （这不是奶糖，这是压缩毛巾，遇水变大变高）
