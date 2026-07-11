import subprocess

from hopekit.registry import ModuleRegistry
from hopekit.qt_compat import QDialog, QPushButton


@ModuleRegistry.register("shutdown", icon="⏻", title="关机命令集", category="tools")
def shutdown_factory(main_window):
    dlg = QDialog()
    dlg.setWindowTitle('关机命令集')
    btn = QPushButton('有注释的关机', dlg)
    btn.setGeometry(0, 0, 200, 41)
    btn.clicked.connect(lambda: subprocess.call(["shutdown", "-i"]))
    dlg.setFixedSize(200, 41)
    return dlg
