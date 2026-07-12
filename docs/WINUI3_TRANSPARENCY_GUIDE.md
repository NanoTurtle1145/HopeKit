# WinUI3 透明链路防崩指南

> PySide6 窗口透明 + DWM 材质（Mica/Acrylic）+ 自定义标题栏
> 适用于 HopeKit 及其他基于 PySide6 的 Windows 桌面应用

---

## 🔵 微软官方参考锚点

查阅这些文档，不要凭印象写，AI 幻觉 90% 出在枚举值和时序上。

| 主题 | 链接 |
|------|------|
| DWMWINDOWATTRIBUTE 完整枚举（33/34/35/36/38） | https://learn.microsoft.com/en-ie/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute |
| DWM_SYSTEMBACKDROP_TYPE（22621+） | https://learn.microsoft.com/zh-cn/windows/win32/api/dwmapi/ne-dwmapi-dwm_systembackdrop_type |
| DwmExtendFrameIntoClientArea（Vista+） | https://learn.microsoft.com/id-id/windows/win32/api/dwmapi/nf-dwmapi-dwmextendframeintoclientarea |
| WinUI3 Mica 规范 | https://learn.microsoft.com/zh-cn/windows/apps/design/style/mica |
| WinUI3 Acrylic 规范 | https://learn.microsoft.com/zh-cn/windows/apps/design/style/acrylic |
| Qt WA_TranslucentBackground | doc.qt.io 搜 "WA_TranslucentBackground" |

---

## 🔴 绝对禁令（AI 高频幻觉 9 条）

违者直接驳回重写，别跟自己的眼睛过不去。

### 1. 严禁只写 `background: transparent` QSS 就当"透明做好了"

那只让 Qt 不 fill 纯色，窗口仍是每像素不透明 RGB，DWM 材质挂上去就是黑底。
必须 `setAttribute(Qt.WA_TranslucentBackground)`。

### 2. 严禁 `WA_TranslucentBackground` 不设 `FramelessWindowHint`

有原生标题栏时 DWM 只模糊客户区外圈，标题栏那条实色，Mica 效果断在标题栏下沿。
WinUI3 主窗口风格必须 Frameless + 自定义标题栏。

### 3. 严禁 `WA_TranslucentBackground` 在 `show()` 之后设

必须在 `__init__` 里、`show()` 之前设，否则 Qt 已经按不透明路径走了，再设也不生效。

### 4. 严禁 `centralWidget` 不设 `background: transparent`

central 默认 `autoFillBackground=True`，会用 `palette().window()` 填一遍（灰/黑），挡住 DWM 模糊。
"控件之间空隙透模糊、控件自身带 surface 背景"才是 Win11 终端/记事本的正确视觉——central 必须透明。

### 5. 严禁 `DwmSetWindowAttribute(38, ...)` 在 `show()` 之前调

HWND 未映射，`winId()` 返回 0 或临时 ID，DWM 返回 E_HANDLE 或悄默失败。
必须在 `showEvent` 里、且 `!spontaneous()` 时调。

### 6. 严禁 Mica 用 `DWMSBT_TRANSIENT=3` 或 `DWMSBT_TABBED=4` 当主窗口

- 主窗口 = `DWMSBT_MAINWINDOW = 2`
- 弹窗/Flyout = `DWMSBT_TRANSIENTWINDOW = 3`（Acrylic）
- Tabbed 标题栏 = `DWMSBT_TABBEDWINDOW = 4`（Mica Alt）

### 7. 严禁漏 `DwmExtendFrameIntoClientArea` 做自定义标题栏

Frameless 后标题栏区 DWM 不画，Mica 只糊客户区，标题栏那条是黑/灰。
必须 `DwmExtendFrameIntoClientArea(hwnd, MARGINS{0,0,32,0})` 把顶部 32px 延进 Frame 区。

### 8. 严禁 Frameless 后不处理拖拽/三个按钮/最大化靠边

`WM_NCLBUTTONDOWN + HTCAPTION` 转发给 DWM 处理拖拽，否则自己算边界会疯。

### 9. 严禁 Win10 用 `attr=38`

Win10 build<22000 根本没有 38 这个 attribute，必返回 E_INVALIDARG。
必须走老路径 `SetWindowCompositionAttribute + ACCENT_ENABLE_ACRYLICBLURBEHIND`。

---

## 📐 规范速查表

### Qt 侧

| 设置 | 时机 | 说明 |
|------|------|------|
| `Qt.FramelessWindowHint` | `__init__`（show 前） | 去原生标题栏，客户区全交 DWM |
| `Qt.WA_TranslucentBackground` | `__init__`（show 前） | 走 WS_EX_LAYERED，每像素 alpha 交给 DWM |
| `centralWidget.setAutoFillBackground(False)` | `__init__`（show 前） | 不让 palette 填背景，控件缝隙透模糊 |
| 子控件自带 surface 背景 | QSS | 内容区不透明，保证可读 |

### DWM 侧（Win11 22621+）

| attr | 值 | 说明 |
|------|-----|------|
| 38 | 2 (`DWMSBT_MAINWINDOW`) | Mica 主窗口 |
| 38 | 3 (`DWMSBT_TRANSIENTWINDOW`) | Acrylic 弹窗/Flyout |
| 38 | 4 (`DWMSBT_TABBEDWINDOW`) | Mica Alt（Tabbed 标题栏） |
| 33 | 2 (`DWMWCP_ROUND`) | DWM 圆角（ROUND） |
| 33 | 3 (`DWMWCP_ROUNDSMALL`) | 小圆角 |
| 35 | 0xFFFFFFFF | 标题栏色透回 Mica（部分 build 认） |
| 36 | - | 标题栏文字颜色 |

### DWM 侧（自定义标题栏）

| 函数 | 参数 | 说明 |
|------|------|------|
| `DwmExtendFrameIntoClientArea` | MARGINS{0,0,32,0} | 顶部 32px 延进 Frame，Mica 糊到标题栏区 |
| `DwmExtendFrameIntoClientArea` | MARGINS{-1,-1,-1,-1} | "sheet of glass" 全窗玻璃片 |

### 降级链

| 系统版本 | 材质方案 |
|----------|----------|
| Win11 22621+ | `DWMWA_SYSTEMBACKDROP_TYPE=38` Mica/Acrylic |
| Win11 22000-22598 | 降级 `DWMWA_MICA=1029` 老 Mica |
| Win10 1803+ | `SetWindowCompositionAttribute` Acrylic 老路径 |
| Win10 更老 / 高对比 / 省电 | 纯色降级（SolidBackgroundFillColorBase） |

---

## 🩺 翻车现象对照表

| 现象 | 根因 | 修法 |
|------|------|------|
| 窗口黑底，Mica 调成功了但看不见 | 没 `WA_TranslucentBackground`，DWM 没拿到 alpha 缓冲 | 加 `setAttribute(Qt.WA_TranslucentBackground)` 在 show 前 |
| 窗口白底/灰底，像蒙了层灰 | `autoFillBackground=True` 还在填 palette.window() | `centralWidget().setAutoFillBackground(False)` |
| 拖窗口有残影/撕裂 | `WA_NoSystemBackground` 误开，或 paintEvent 没处理好 | 关掉 `WA_NoSystemBackground`，用 `WA_TranslucentBackground` |
| 鼠标点透明区穿透到后面窗口 | `WA_TransparentForMouseEvents` 误开，或 WS_EX_TRANSPARENT | 检查 windowFlags |
| Frameless 后窗口阴影没了 | 去标题栏的同时把 DWM 阴影也干掉了 | `DWMWA_NCRENDERING_POLICY` 设 `DWMNCRP_ENABLED` |
| Mica 在 Win10 上黑底 | Win10 根本没 Mica，38 不存在 | 降级 Acrylic 老路径或纯色 |
| 材质效果溢出窗口边界 | 没设 `WA_TranslucentBackground` 时用了老路径 | 确保 `WA_TranslucentBackground` 在 show 前设置 |

---

## 🎯 HopeKit 实现要点

### 当前实现位置

| 文件 | 职责 |
|------|------|
| `hopekit/main_window.py` | MainUi 窗口，`__init__` 设属性，`showEvent` 挂材质 |
| `hopekit/mica.py` | DWM API 封装，Mica/Acrylic/降级 全链路 |
| `hopekit/theme.py` | ThemeManager，管理 style/mode/colors |
| `Styles/styles.py` | QSS 生成，WinUI3 主题对应 `_winui3_*` 系列函数 |

### 正确时序（必背）

```
__init__
  ├─ setWindowFlags(FramelessWindowHint)     ← 可选，当前 HopeKit 没开
  ├─ setAttribute(WA_TranslucentBackground)  ← show 前！
  ├─ setCentralWidget(central)
  ├─ central.setAutoFillBackground(False)    ← show 前！
  └─ ... UI 构建 ...

show()
  ↓
showEvent(e)
  ├─ if e.spontaneous(): return              ← 过滤系统触发
  ├─ if _mica_applied: return                ← 防重复
  ├─ hwnd = int(self.winId())                ← 拿真 HWND
  ├─ BackdropManager.apply(hwnd, "mica")     ← 挂材质
  ├─ DwmExtendFrameIntoClientArea(...)       ← 自定义标题栏用
  ├─ DWMWA_WINDOW_CORNER_PREFERENCE = 2      ← DWM 圆角
  └─ _mica_applied = True
```

### QSS 分层原则

从底到顶：

```
QMainWindow             → transparent    （DWM 材质直接透）
└─ centralWidget        → transparent    （同上）
   ├─ #sidebar          → rgba(半透明)   （透材质 + tint 保可读）
   └─ #contentArea      → surface 不透明  （内容区保证可读）
      └─ QStackedWidget → surface 不透明
         └─ 各页面卡片   → surface_container
```

---

## 📋 判别测试（答不出说明没真查文档）

### 题 1
**DWMSBT_MAINWINDOW=2 / TRANSIENT=3 / TABBED=4 分别对应什么材质？哪个是主窗口该用的？**

> 2 = Mica（主窗）/ 3 = Acrylic（弹窗，TRANSIENT = 桌面亚克力）/ 4 = Mica Alt（Tabbed 标题栏）。主窗用 2。

### 题 2
**WA_TranslucentBackground 为什么必须配 FramelessWindowHint？不配会怎样？**

> 不 Frameless 时 DWM 只把模糊挂客户区外圈，标题栏那条是 DWM 自己画的实色（系统色），Mica 效果断在标题栏下沿。Frameless 后客户区全交 DWM，Mica 才糊全窗。

### 题 3
**DwmExtendFrameIntoClientArea 的 MARGINS 传 {-1} 是什么意思？{0,0,32,0} 和 {32,0,0,0} 分别延了哪边？**

> {-1, -1, -1, -1} = 全边 -1 → "sheet of glass" 整窗无边框实心玻璃片效果；
> {0, 0, 32, 0} = 仅顶部延 32px 进客户区（自定义标题栏标准写法）；
> 顺序：cxLeftWidth, cxRightWidth, cyTopHeight, cyBottomHeight。

### 题 4
**DWM attr=33/34/35/36 分别对应什么？其中哪个能让标题栏"透回 Mica"？**

> 33 = WINDOW_CORNER_PREFERENCE / 34 = BORDER_COLOR / 35 = CAPTION_COLOR / 36 = TEXT_COLOR。
> 35 传 0xFFFFFFFF 让标题栏色透回 Mica（22621+ 部分 build 认）。

### 题 5
**PySide6 里 HWND 为什么必须在 showEvent 里拿，__init__ 里拿会怎样？**

> `__init__` 里 `winId()` 返回 0 或 Qt 内部临时 HWND（窗口还没 native 映射），DwmSetWindowAttribute 返回 E_HANDLE 或悄默失败。必须 `show()` 之后 `windowHandle()->winId()` 才拿到真 HWND。

---

## 💡 一句收

PySide6 透明"难"是因为它横跨两条链：

**Qt 侧**：flag + attribute + central 透明 + show 时序
**DWM 侧**：38+Mica / 38+Acrylic / 老路径 Acrylic / ExtendFrame / 33 圆角 / 35 标题色

缺一环就黑底/灰底/残影。两条链全对上，Mica/Acrylic 立马就"活"了。
