"""
MainUi — Web UI 宿主主窗口

重构后：MainUi 不再直接用 QWidget 拼装侧边栏与内容区，
而是宿主一个 QWebEngineView（WebUIHost），所有 UI 由 webui/index.html
的 Apple 风格 HTML/CSS/JS 渲染。Python 端只负责：

- 桥接（PythonBridge）：插件列表、打开模块、切换主题
- 主题应用（全局 QSS 仍用于插件子窗口）
- 透明材质（DWM Mica/Acrylic）应用到主窗口背景

动画 / 排版 / 材质层级 / 减少动效 等所有 UI 细节都在 Web 端实现
（见 webui/styles/ 与 webui/scripts/motion.js）。
"""

from hopekit.qt_compat import (
    QtCore, QtGui, QtWidgets,
    QMainWindow, QApplication, QWidget,
    QHBoxLayout,
)
from hopekit.theme import theme
from hopekit.registry import ModuleRegistry
from hopekit.transparency import (
    is_transparent_theme,
    enable_transparency_before_show,
    enable_transparency_for_central,
    apply_backdrop_to_window,
    disable_transparency,
    apply_transparency_dynamic,
)
from hopekit.web_ui import WebUIHost
from hopekit.web_bridge import PythonBridge
from Styles import styles


class MainUi(QMainWindow):
    """
    Web UI 宿主窗口。

    Public API（保持与旧版兼容）：
    - _apply_style() — 应用全局样式
    - _refresh_child_window_styles() — 刷新所有插件子窗口
    - _apply_style_to_window(win) — 给新打开的插件窗口套上样式
    """

    def __init__(self, version: str = ""):
        self._version = version
        super().__init__()
        self.setWindowTitle(f"HopeKit {version}")
        self.resize(1200, 700)
        self.setMinimumSize(900, 600)
        self._transparency_applied = False

        # 透明主题：WA_TranslucentBackground 必须在 show() 之前设置
        enable_transparency_before_show(self)

        self._build_ui()
        self._apply_style()

    # ============================================================
    #  UI 构建
    # ============================================================
    def _build_ui(self):
        central = QWidget(self)
        self.setCentralWidget(central)
        # 透明主题：central 不自动填充背景
        enable_transparency_for_central(central)

        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 主界面：WebUIHost
        self._webui = WebUIHost(central)
        layout.addWidget(self._webui, 1)

        # 桥接
        self._bridge = PythonBridge(main_window=self, parent=self)
        self._webui.set_bridge(self._bridge)

        # 状态栏与菜单栏（保留最简形态，主交互在 Web UI 内）
        self.statusBar().showMessage("Ready")
        menubar = QtWidgets.QMenuBar(self)
        self.setMenuBar(menubar)

    # ============================================================
    #  样式应用
    # ============================================================
    @staticmethod
    def _global_stylestring():
        return styles.global_stylesheet(theme.colors)

    def _apply_style(self, notify_web: bool = True):
        """
        应用全局 QSS（主要影响插件子窗口；主窗口由 Web UI 渲染）。

        Args:
            notify_web: 是否推送 themeChanged 给 Web UI。
                        True — 外部主动改主题（如设置对话框），需要 JS 同步
                        False — Web UI 自己发起的 setTheme slot 调用，
                                JS 已经收到 colors 并自己更新了，无需再 emit
        """
        app = QApplication.instance()
        if app is not None:
            app.setStyleSheet(self._global_stylestring())
        # 主窗口本身的 QSS 极简：仅做透明背景容器
        self.setStyleSheet(styles.main_host_stylesheet(theme.colors))
        if self.isVisible():
            if is_transparent_theme():
                if not self._transparency_applied:
                    ok = apply_transparency_dynamic(self)
                    if ok:
                        self._transparency_applied = True
            else:
                if self._transparency_applied:
                    self._clear_transparency()
        if notify_web and self._bridge is not None:
            self._bridge.notify_theme_changed()

    def _apply_style_to_window(self, win):
        """给插件窗口套上当前全局样式。"""
        if win is None:
            return
        try:
            win.setStyleSheet("")
            win.setStyleSheet(self._global_stylestring())
        except Exception:
            pass

    def _refresh_child_window_styles(self):
        """刷新所有已缓存的插件窗口样式（主题切换时调用）。"""
        for name in list(ModuleRegistry._instances.keys()):
            win = ModuleRegistry._instances.get(name)
            if win is not None:
                self._apply_style_to_window(win)

    # ============================================================
    #  透明效果
    # ============================================================
    def _apply_transparency(self):
        if not is_transparent_theme():
            return
        try:
            ok = apply_backdrop_to_window(self, kind=None)
            if ok:
                self._transparency_applied = True
        except Exception as e:
            import traceback
            print(f"[{theme.style}] 透明效果异常: {e}", flush=True)
            traceback.print_exc()

    def _clear_transparency(self):
        try:
            disable_transparency(self)
            self._transparency_applied = False
            self.update()
            self.repaint()
        except Exception as e:
            print(f"[Transparency] 清除透明效果异常: {e}", flush=True)

    # ============================================================
    #  事件
    # ============================================================
    def showEvent(self, event):
        """窗口显示时尝试开启透明效果（hwnd 在 show 后才有效）。"""
        super().showEvent(event)
        if event.spontaneous() or self._transparency_applied:
            return
        self._apply_transparency()

    def reload_web_ui(self):
        """供外部调试调用。"""
        if self._webui is not None:
            self._webui.reload()
