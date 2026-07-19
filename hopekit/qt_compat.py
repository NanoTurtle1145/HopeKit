"""
Qt 兼容层 — PySide6 单绑定 + QWebEngine 集成

锁定 PySide6（Qt 官方、LGPL），同时把 QWebEngineView / QWebChannel
统一在此处导入，避免 plugins 子模块各自 try/except。

用法:
    from hopekit.qt_compat import QtWidgets, QtCore, QtGui, Signal, Slot
    from hopekit.qt_compat import QWebEngineView, QWebChannel, HAS_WEBENGINE

注意: Qt6 枚举必须使用命名空间形式，例如:
    Qt.CursorShape.PointingHandCursor  (非 Qt.PointingHandCursor)
    Qt.AlignmentFlag.AlignCenter       (非 Qt.AlignCenter)
    QFrame.Shape.NoFrame               (非 QFrame.NoFrame)
"""

import sys

try:
    import PySide6
    from PySide6 import QtWidgets, QtCore, QtGui
    from PySide6.QtCore import Signal, Slot, QObject, Property
    from PySide6.QtGui import QDesktopServices, QAction
    from PySide6.QtCore import QUrl

    QT_LIB = "PySide6"
    QT_VERSION = PySide6.__version__

except ImportError as e:
    raise ImportError(
        "PySide6 is not installed. Install with: pip install PySide6"
    ) from e

# QWebEngine 是可选依赖（需要单独安装 PySide6-WebEngine）
HAS_WEBENGINE = False
QWebEngineView = None
QWebEngineSettings = None
QWebEngineProfile = None
QWebChannel = None
QWebEngineUrlScheme = None

try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
    from PySide6.QtWebEngineCore import (
        QWebEngineSettings,
        QWebEngineProfile,
    )
    from PySide6.QtWebChannel import QWebChannel
    HAS_WEBENGINE = True
except ImportError:
    # WebEngine 不可用时，主窗口将回退到 QSS 模式
    pass


# ---- QtWidgets 类别名 ----
QApplication = QtWidgets.QApplication
QMainWindow = QtWidgets.QMainWindow
QDialog = QtWidgets.QDialog
QWidget = QtWidgets.QWidget
QLabel = QtWidgets.QLabel
QPushButton = QtWidgets.QPushButton
QLineEdit = QtWidgets.QLineEdit
QTextEdit = QtWidgets.QTextEdit
QGroupBox = QtWidgets.QGroupBox
QVBoxLayout = QtWidgets.QVBoxLayout
QHBoxLayout = QtWidgets.QHBoxLayout
QGridLayout = QtWidgets.QGridLayout
QRadioButton = QtWidgets.QRadioButton
QStatusBar = QtWidgets.QStatusBar
QMenuBar = QtWidgets.QMenuBar
QCalendarWidget = QtWidgets.QCalendarWidget
QMessageBox = QtWidgets.QMessageBox
QFrame = QtWidgets.QFrame
QStackedWidget = QtWidgets.QStackedWidget
QScrollArea = QtWidgets.QScrollArea
QSizePolicy = QtWidgets.QSizePolicy

# ---- QtCore 类别名 ----
QThread = QtCore.QThread
QPropertyAnimation = QtCore.QPropertyAnimation
QEasingCurve = QtCore.QEasingCurve
QTimer = QtCore.QTimer
QFile = QtCore.QFile
QIODevice = QtCore.QIODevice
QByteArray = QtCore.QByteArray

# ---- QtGui 类别名 ----
QPixmap = QtGui.QPixmap
QColor = QtGui.QColor
QPalette = QtGui.QPalette
QFont = QtGui.QFont
QFontDatabase = QtGui.QFontDatabase
QPainter = QtGui.QPainter
QDragEnterEvent = QtGui.QDragEnterEvent
QDropEvent = QtGui.QDropEvent

# ---- Qt 命名空间 ----
Qt = QtCore.Qt

# 鼠标光标
PointingHandCursor = Qt.CursorShape.PointingHandCursor

# 对齐方式
AlignCenter = Qt.AlignmentFlag.AlignCenter
AlignVCenter = Qt.AlignmentFlag.AlignVCenter
AlignLeft = Qt.AlignmentFlag.AlignLeft
AlignRight = Qt.AlignmentFlag.AlignRight

# 滚动条策略
ScrollBarAlwaysOff = Qt.ScrollBarPolicy.ScrollBarAlwaysOff
ScrollBarAsNeeded = Qt.ScrollBarPolicy.ScrollBarAsNeeded

# 图片变换
SmoothTransformation = Qt.TransformationMode.SmoothTransformation

# 窗口属性
WA_TranslucentBackground = Qt.WidgetAttribute.WA_TranslucentBackground
WA_StyledBackground = Qt.WidgetAttribute.WA_StyledBackground
WA_NoSystemBackground = Qt.WidgetAttribute.WA_NoSystemBackground

# 应用属性
AA_ShareOpenGLContexts = Qt.ApplicationAttribute.AA_ShareOpenGLContexts

# QFrame 形状
NoFrame = QFrame.Shape.NoFrame


def is_pyside6() -> bool:
    """始终返回 True（已锁定 PySide6）。"""
    return True


def is_pyqt6() -> bool:
    """始终返回 False（已锁定 PySide6）。"""
    return False


def require_webengine():
    """供需要 QWebEngine 的入口调用；缺失时抛出清晰的 ImportError。"""
    if not HAS_WEBENGINE:
        raise ImportError(
            "PySide6-WebEngine is not installed. "
            "Install with: pip install PySide6-WebEngine"
        )
