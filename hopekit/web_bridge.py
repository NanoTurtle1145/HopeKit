"""
PythonBridge — QWebChannel 桥接对象

把 PySide6 端的能力暴露给 Web UI（HTML/JS）：
- 查询模块/分类/主题
- 打开模块、切换启用
- 切换主题、导入主题
- 退出

所有 Slot 用 @Slot 装饰，QWebChannel 会把它的返回值（或异步 callback）
传给 JS 端。返回的复杂数据用 JSON 字符串传递，JS 端再 JSON.parse。

用法（main_window 中）:
    from hopekit.web_bridge import PythonBridge
    self._bridge = PythonBridge(self)
    self._channel = QWebChannel()
    self._channel.registerObject("bridge", self._bridge)
    self._webview.page().setWebChannel(self._channel)
"""

import json
import os
import sys

from hopekit.qt_compat import (
    QObject, Slot, Signal,
    QUrl, QDesktopServices,
)
from hopekit.registry import ModuleRegistry
from hopekit.theme import theme
from hopekit.paths import resource_path
from hopekit.version import VERSION
from hopekit.settings_page import AboutPage


AVAILABLE_STYLES = [
    "md3", "md2", "qt",
    "winui3", "win10fluent",
    "gnome", "kde", "cupertino", "chromeos",
]


class PythonBridge(QObject):
    """
    注册到 QWebChannel 名为 "bridge" 的对象。

    注意：JS 调用 .foo(args, callback) 时，PySide6 会自动把 return 值
    传给 callback；不需要显式 @Slot(result=str)。但显式声明 result=str
    有时能让 QWebChannel 更早绑定方法签名，建议保留。
    """

    # Python → JS 信号（push 模型；JS 通过 bridge.signalName.connect 订阅）
    themeChanged = Signal(str)
    pluginsChanged = Signal(str)

    def __init__(self, main_window=None, parent=None):
        super().__init__(parent)
        self._main = main_window

    # ============================================================
    #  INITIAL STATE
    # ============================================================
    @Slot(result=str)
    def getInitialState(self):
        """一次性返回 JS 启动所需的全部状态。"""
        data = {
            "version": VERSION,
            "categories": ModuleRegistry.categories(),
            "plugins": self._serialize_plugins(),
            "theme": self._serialize_theme(),
            "logoUrl": self._logo_url(),
        }
        return json.dumps(data, ensure_ascii=False)

    @Slot(result=str)
    def getPlugins(self):
        return json.dumps(self._serialize_plugins(), ensure_ascii=False)

    @Slot(result=str)
    def getTheme(self):
        return json.dumps(self._serialize_theme(), ensure_ascii=False)

    # ============================================================
    #  MODULE ACTIONS
    # ============================================================
    @Slot(str, result=bool)
    def openModule(self, name: str) -> bool:
        info = ModuleRegistry.get(name)
        if not info or not info["enabled"]:
            return False
        if self._main is None:
            return False
        try:
            win = ModuleRegistry.get_or_create(name, self._main)
            if win is None:
                # links 类型：factory 已自行打开外部浏览器，返回 True
                return True
            # 应用全局样式（与原生 plugin window 一致）
            self._main._apply_style_to_window(win)
            win.show()
            win.raise_()
            win.activateWindow()
            return True
        except Exception as e:
            print(f"[bridge] openModule '{name}' failed: {e}", file=sys.stderr)
            return False

    @Slot(str, bool, result=bool)
    def toggleModule(self, name: str, enabled: bool) -> bool:
        info = ModuleRegistry.get(name)
        if not info:
            return False
        ModuleRegistry.set_enabled(name, enabled)
        return True

    # ============================================================
    #  THEME ACTIONS
    # ============================================================
    @Slot(str, str, result=str)
    def setTheme(self, style: str, mode: str) -> str:
        """
        应用主题并返回新的 colors JSON。
        JS 端拿到 colors 后更新 CSS 变量。

        注意：这里不再主动 emit themeChanged，因为 JS 已经通过 return 拿到
        了最新 colors 并自己更新了。重复 emit 会导致 JS 双重渲染。
        外部主动改主题时，调用方应直接调 main_window._apply_style(notify_web=True)。
        """
        if style not in AVAILABLE_STYLES:
            style = "cupertino"
        if mode not in ("auto", "light", "dark"):
            mode = "auto"
        theme.set_style(style)
        theme.set_mode(mode)
        # 触发主窗口刷新（透明效果 / 全局样式 / 子窗口样式）
        # notify_web=False：JS 已通过 return 拿到 colors，无需重复 emit
        if self._main is not None:
            try:
                self._main._apply_style(notify_web=False)
                self._main._refresh_child_window_styles()
            except Exception as e:
                print(f"[bridge] _apply_style failed: {e}", file=sys.stderr)
        return json.dumps(theme.colors, ensure_ascii=False)

    @Slot(result=bool)
    def importTheme(self) -> bool:
        """通过系统文件对话框选择 JSON 主题文件并应用。"""
        if self._main is None:
            return False
        from hopekit.qt_compat import QtWidgets, QFileDialog
        path, _ = QFileDialog.getOpenFileName(
            self._main, "导入主题", "", "Theme JSON (*.json)"
        )
        if not path:
            return False
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            style = data.get("style")
            mode = data.get("mode", "auto")
            if style in AVAILABLE_STYLES:
                self.setTheme(style, mode)
                return True
            return False
        except Exception as e:
            print(f"[bridge] importTheme failed: {e}", file=sys.stderr)
            return False

    @Slot()
    def exitApp(self):
        if self._main is not None:
            self._main.close()

    @Slot(result=str)
    def getLogoUrl(self):
        return self._logo_url()

    @Slot(result=str)
    def getAboutInfo(self):
        """返回关于信息，供 Web UI 渲染关于页面"""
        return json.dumps(AboutPage.get_about_info(), ensure_ascii=False)

    # ============================================================
    #  Helpers
    # ============================================================
    def _serialize_plugins(self):
        out = []
        for name, info in ModuleRegistry.all().items():
            out.append({
                "name": name,
                "icon": info.get("icon", "📦"),
                "title": info.get("title", name),
                "description": info.get("description", ""),
                "category": info.get("category", "tools"),
                "kind": info.get("kind", "window"),
                "enabled": info.get("enabled", True),
            })
        return out

    def _serialize_theme(self):
        return {
            "style": theme.style,
            "mode": theme.mode,
            "availableStyles": AVAILABLE_STYLES,
            "isDark": theme.is_dark,
            "colors": theme.colors,
        }

    def _logo_url(self):
        """返回 logo.jpg 的 file:// URL（QWebEngine 可加载本地资源）。"""
        try:
            path = resource_path("logo.jpg")
            if path and os.path.isfile(path):
                return QUrl.fromLocalFile(path).toString()
        except Exception as e:
            print(f"[bridge] logo url failed: {e}", file=sys.stderr)
        return ""

    # ============================================================
    #  外部主动推送（供 main_window 调用）
    # ============================================================
    def notify_theme_changed(self):
        """主窗口外部触发主题刷新时调用，把最新主题推给 JS。"""
        self.themeChanged.emit(json.dumps(self._serialize_theme(), ensure_ascii=False))

    def notify_plugins_changed(self):
        self.pluginsChanged.emit(json.dumps(self._serialize_plugins(), ensure_ascii=False))
