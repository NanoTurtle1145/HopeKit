"""
HopeKit 最小可运行示例
复制这个文件改改就能起步。
"""

import sys
from hopekit.qt_compat import QtWidgets, QMainWindow, QLabel


class MinimalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HopeKit Minimal")
        self.setFixedSize(400, 300)

        label = QLabel("Hello HopeKit!", self)
        label.setGeometry(130, 120, 200, 40)
        label.setStyleSheet("font-size: 18pt; font-weight: 600;")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MinimalApp()
    window.show()
    sys.exit(app.exec())
