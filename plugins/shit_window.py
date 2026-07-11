from hopekit.registry import ModuleRegistry
from hopekit.qt_compat import (
    QDialog, QPushButton, QVBoxLayout, QMessageBox,
    QDesktopServices, QUrl,
)


@ModuleRegistry.register("shit", icon="💩", title="探索系统屎山", category="tools")
def shit_factory(main_window):
    from plugins.shutdown import shutdown_factory

    dlg = QDialog()
    dlg.setWindowTitle('探索系统屎山')
    dlg._shut_win = None
    dlg._web_win = None

    shutbutton = QPushButton('关机命令集')
    webbutton = QPushButton('简易官网')

    def open_shut():
        if dlg._shut_win is None:
            dlg._shut_win = shutdown_factory(dlg)
        dlg._shut_win.show()

    def open_web():
        try:
            from examples.browser.web_window import WebWindow
            if dlg._web_win is None:
                dlg._web_win = WebWindow()
            dlg._web_win.show()
        except Exception as reason:
            QMessageBox.warning(
                dlg, "内置浏览器不可用",
                f"PyQtWebEngine 调用失败，已改用系统浏览器打开。\n\n错误信息：{reason}"
            )
            QDesktopServices.openUrl(QUrl("https://hopestudio.top/"))

    shutbutton.clicked.connect(open_shut)
    webbutton.clicked.connect(open_web)

    layout = QVBoxLayout(dlg)
    layout.addWidget(shutbutton)
    layout.addWidget(webbutton)
    dlg.setFixedWidth(200)
    return dlg
