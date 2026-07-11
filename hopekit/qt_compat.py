"""
Qt 兼容层 — 同时支持 PyQt5 和 PySide6

优先使用 PySide6（Qt 官方、LGPL），回退到 PyQt5。
用法:
    from hopekit.qt_compat import QtWidgets, QtCore, QtGui, Signal, Slot, QT_LIB
"""

import sys

QT_LIB = ""

try:
    from PySide6 import QtWidgets, QtCore, QtGui
    from PySide6.QtCore import Signal, Slot
    from PySide6.QtGui import QDesktopServices
    from PySide6.QtCore import QUrl
    QT_LIB = "PySide6"

    _qt_version = QtCore.QT_VERSION_STR

    def _enum_val(enum_val):
        return enum_val

except ImportError:
    try:
        from PyQt5 import QtWidgets, QtCore, QtGui
        from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
        from PyQt5.QtGui import QDesktopServices
        from PyQt5.QtCore import QUrl
        QT_LIB = "PyQt5"

        def _enum_val(enum_val):
            return enum_val

    except ImportError:
        raise ImportError(
            "Neither PySide6 nor PyQt5 is installed. "
            "Install one with: pip install PySide6  # or PyQt5"
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

QPixmap = QtGui.QPixmap
QCursor = QtCore.Qt.PointingHandCursor if hasattr(QtCore.Qt, 'PointingHandCursor') else None

Qt = QtCore.Qt


def is_pyside6() -> bool:
    return QT_LIB == "PySide6"


def is_pyqt5() -> bool:
    return QT_LIB == "PyQt5"
