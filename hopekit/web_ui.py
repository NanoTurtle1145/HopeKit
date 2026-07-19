"""
WebUIHost — QWebEngineView 容器

加载 webui/index.html，注册 QWebChannel 桥接对象。

- 开发态：从项目根目录的 webui/index.html 加载（file://）
- 打包态（PyInstaller）：使用 file:// 加载 _MEIPASS/webui/index.html
- 不可用回退：若 HAS_WEBENGINE 为 False，渲染一个 QLabel 占位

透明主题：WebEngineView 背景透明，让 DWM 材质透出
"""

import os
import sys

from hopekit.qt_compat import (
    QtCore, QtGui, QtWidgets,
    QWidget, QVBoxLayout, QLabel,
    QWebEngineView, QWebEngineSettings, QWebEngineProfile, QWebChannel,
    HAS_WEBENGINE,
)
from hopekit.paths import resource_path
from hopekit.web_bridge import PythonBridge


if HAS_WEBENGINE:
    from PySide6.QtWebEngineCore import QWebEnginePage, QWebEnginePage as _WEP

    # level 是 QWebEnginePage.JavaScriptConsoleMessageLevel 枚举
    _LEVEL_TAG = {
        _WEP.JavaScriptConsoleMessageLevel.InfoMessageLevel:    'JS',
        _WEP.JavaScriptConsoleMessageLevel.WarningMessageLevel: 'JS!',
        _WEP.JavaScriptConsoleMessageLevel.ErrorMessageLevel:   'JS?',
    }

    class _BridgeWebPage(QWebEnginePage):
        """把 JS console 消息转发到 Python stdout，便于调试。"""
        def javaScriptConsoleMessage(self, level, message, line_number, source_id):
            tag = _LEVEL_TAG.get(level, 'JS')
            print(f"[{tag}] {message}  ({source_id}:{line_number})", flush=True)
else:
    _BridgeWebPage = None


class WebUIHost(QWidget):
    """
    QWebEngineView 宿主。把 webui/index.html 渲染为主界面。
    main_window 通过 set_bridge() 注入 PythonBridge。
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("webUIHost")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        self._bridge = None
        self._channel = None
        self._view = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        if not HAS_WEBENGINE:
            placeholder = QLabel(self)
            placeholder.setText(
                "<div style='padding:24px;font-family:system-ui;'>"
                "<h2>QtWebEngine 未安装</h2>"
                "<p>请运行：<code>pip install PySide6-WebEngine</code></p>"
                "</div>"
            )
            placeholder.setTextFormat(QtCore.Qt.TextFormat.RichText)
            placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(placeholder)
            self._placeholder = placeholder
            return

        # 使用自定义 page 接管 JS console
        self._view = QWebEngineView(self)
        self._view.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        if _BridgeWebPage is not None:
            old_page = self._view.page()
            new_page = _BridgeWebPage(self._view)
            self._view.setPage(new_page)
            try:
                old_page.deleteLater()
            except Exception:
                pass

        # 让 WebEngine 页面背景透明，使 DWM 材质 / 容器背景透出
        try:
            self._view.page().setBackgroundColor(QtCore.Qt.GlobalColor.transparent)
        except Exception:
            pass

        self._configure_settings()
        self._setup_channel()

        layout.addWidget(self._view)

        # 加载入口 HTML
        self._load_index()

    # ----------------------------------------------------------------
    def _configure_settings(self):
        page = self._view.page()
        settings = page.settings()
        try:
            settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, False)
            settings.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, True)
        except Exception as e:
            print(f"[WebUIHost] settings apply failed: {e}", file=sys.stderr)

    def _setup_channel(self):
        if not HAS_WEBENGINE:
            return
        self._channel = QWebChannel(self)
        # bridge 由 set_bridge() 注入；这里先创建空 channel
        self._view.page().setWebChannel(self._channel)

    def _load_index(self):
        index_path = resource_path(os.path.join("webui", "index.html"))
        if not os.path.isfile(index_path):
            # 开发态兜底：从项目根的 webui/index.html 加载
            here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            index_path = os.path.join(here, "webui", "index.html")
        if not os.path.isfile(index_path):
            self._view.setHtml(
                "<div style='padding:24px;font-family:system-ui;color:#1D1D1F;background:#F5F5F7;"
                "height:100vh;'>"
                "<h2>webui/index.html 未找到</h2>"
                "<p>期望路径：<code>" + index_path + "</code></p>"
                "</div>",
                QtCore.QUrl("about:blank"),
            )
            return

        url = QtCore.QUrl.fromLocalFile(index_path)
        self._view.load(url)

    # ----------------------------------------------------------------
    def set_bridge(self, bridge: PythonBridge):
        """主窗口构造 PythonBridge 后调用此方法注册到 channel。"""
        if not HAS_WEBENGINE or self._channel is None:
            return
        self._bridge = bridge
        self._channel.registerObject("bridge", bridge)

    @property
    def view(self):
        return self._view

    @property
    def bridge(self):
        return self._bridge

    # ----------------------------------------------------------------
    def reload(self):
        if self._view is not None:
            self._view.reload()
