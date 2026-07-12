"""
内嵌浏览器 demo
基于 QtWebEngine 的简易浏览器，含加载进度与失败回退
"""

from hopekit.qt_compat import QUrl, QMainWindow, QStatusBar

try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
    HAS_WEBENGINE = True
except ImportError:
    try:
        from PyQt6.QtWebEngineWidgets import QWebEngineView
        HAS_WEBENGINE = True
    except ImportError:
        HAS_WEBENGINE = False


class WebWindow(QMainWindow):
    def __init__(self, url: str = "https://hopestudio.top/"):
        super().__init__()
        self.setWindowTitle("官网")
        self.setGeometry(100, 100, 800, 600)

        if not HAS_WEBENGINE:
            from hopekit.qt_compat import QLabel
            self.setCentralWidget(QLabel("QtWebEngine 未安装，无法使用内嵌浏览器"))
            return

        self.web_view = QWebEngineView()
        self.web_view.load(QUrl(url))
        self.setCentralWidget(self.web_view)

        self._status = QStatusBar()
        self.setStatusBar(self._status)
        self._status.showMessage("正在加载...")

        self.web_view.loadProgress.connect(
            lambda p: self._status.showMessage(f"加载中... {p}%")
        )
        self.web_view.loadFinished.connect(self._on_load_finished)

    def _on_load_finished(self, ok: bool):
        if ok:
            self._status.showMessage("加载完成", 3000)
        else:
            self._status.showMessage("加载失败：网站无法访问（可能是 502/网络问题）", 5000)
            self.web_view.setHtml(
                "<div style='font-family:微软雅黑; padding:30px; text-align:center;'>"
                "<h2 style='color:#c0392b;'>无法打开网页</h2>"
                "<p>网站当前无法访问。</p>"
                "<p>可能原因：服务器故障或网络连接问题。</p>"
                "<p style='color:#888;'>这不是浏览器的问题，请稍后重试。</p>"
                "</div>"
            )


def open_web_with_fallback(parent, url: str = "https://hopestudio.top/"):
    """优先尝试内嵌浏览器，失败则回退到系统默认浏览器。"""
    from hopekit.qt_compat import QMessageBox, QDesktopServices, QUrl
    try:
        win = WebWindow(url)
        win.show()
        return win
    except Exception as reason:
        QMessageBox.warning(
            parent, "内置浏览器不可用",
            f"QtWebEngine 调用失败，已改用系统浏览器打开。\n\n错误信息：{reason}"
        )
        QDesktopServices.openUrl(QUrl(url))
        return None
