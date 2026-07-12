"""
Qt 兼容层 — 同时支持 PySide6 和 PyQt6

优先使用 PySide6（Qt 官方、LGPL），回退到 PyQt6。
用法:
    from hopekit.qt_compat import QtWidgets, QtCore, QtGui, Signal, Slot, QT_LIB

注意: Qt6 枚举必须使用命名空间形式，例如:
    Qt.CursorShape.PointingHandCursor  (非 Qt.PointingHandCursor)
    Qt.AlignmentFlag.AlignCenter       (非 Qt.AlignCenter)
    QFrame.Shape.NoFrame               (非 QFrame.NoFrame)
"""

import sys

QT_LIB = ""

try:
    import PySide6
    from PySide6 import QtWidgets, QtCore, QtGui
    from PySide6.QtCore import Signal, Slot
    from PySide6.QtGui import QDesktopServices
    from PySide6.QtCore import QUrl
    QT_LIB = "PySide6"

    _qt_version = PySide6.__version__

except ImportError:
    try:
        from PyQt6 import QtWidgets, QtCore, QtGui
        from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
        from PyQt6.QtGui import QDesktopServices
        from PyQt6.QtCore import QUrl
        QT_LIB = "PyQt6"

        _qt_version = QtCore.QT_VERSION_STR if hasattr(QtCore, 'QT_VERSION_STR') else PyQt6.__version__

    except ImportError:
        raise ImportError(
            "Neither PySide6 nor PyQt6 is installed. "
            "Install one with: pip install PySide6  # or PyQt6"
        )


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

QThread = QtCore.QThread

QPixmap = QtGui.QPixmap

# Qt6 命名空间枚举别名（两套绑定统一用这些常量）
Qt = QtCore.Qt

# 指向手的鼠标样式
PointingHandCursor = Qt.CursorShape.PointingHandCursor

# 对齐方式
AlignCenter = Qt.AlignmentFlag.AlignCenter
AlignVCenter = Qt.AlignmentFlag.AlignVCenter
AlignLeft = Qt.AlignmentFlag.AlignLeft
AlignRight = Qt.AlignmentFlag.AlignRight

# 滚动条策略
ScrollBarAlwaysOff = Qt.ScrollBarPolicy.ScrollBarAlwaysOff
ScrollBarAsNeeded = Qt.ScrollBarPolicy.ScrollBarAsNeeded

# 图片变换模式
SmoothTransformation = Qt.TransformationMode.SmoothTransformation

# 窗口属性
WA_TranslucentBackground = Qt.WidgetAttribute.WA_TranslucentBackground
WA_StyledBackground = Qt.WidgetAttribute.WA_StyledBackground

# 应用属性
AA_ShareOpenGLContexts = Qt.ApplicationAttribute.AA_ShareOpenGLContexts

# QFrame 形状
NoFrame = QFrame.Shape.NoFrame


def is_pyside6() -> bool:
    return QT_LIB == "PySide6"


def is_pyqt6() -> bool:
    return QT_LIB == "PyQt6"
