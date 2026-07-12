"""
HopeKit 2.0.0 — 主程序入口

所有核心模块都在 hopekit/ 包中：
- hopekit.main_window.MainUi: 主窗口
- hopekit.registry.ModuleRegistry: 插件注册
- hopekit.theme: 主题管理
"""

import sys

from hopekit import (
    qt_compat,
    discover_plugins,
    MainUi,
    __version__ as VERSION,
)


def main():
    print("[main] 启动中...", flush=True)
    # WebEngine 需要 OpenGL 上下文共享，必须在创建 QApplication 之前设置
    qt_compat.QtCore.QCoreApplication.setAttribute(
        qt_compat.Qt.ApplicationAttribute.AA_ShareOpenGLContexts
    )

    discover_plugins("plugins")

    app = qt_compat.QApplication(sys.argv)
    window = MainUi(version=VERSION)
    print("[main] 窗口创建完成，show...", flush=True)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
