import sys
from PyQt5 import QtCore, QtWidgets

# 导入 HopeKit 框架
from hopekitmain import MainUi, theme
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton

# ── 自定义工具窗口 ──────────────────────────────────────────
class MyToolWindow(QDialog):
    """你自己的工具，完全独立"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("我的自定义工具")
        self.setFixedSize(400, 300)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("这是我自己写的工具！"))
        btn = QPushButton("点我")
        btn.clicked.connect(lambda: print("Hello from my tool!"))
        layout.addWidget(btn)

# ── 继承主界面，追加自定义工具 ─────────────────────────────
class MyMainUi(MainUi):
    def __init__(self):
        super().__init__()

        # 新增一个页面到堆叠区
        self._stack.addWidget(self._build_my_page())

        # 在侧边栏导航按钮列表末尾追加
        btn = QtWidgets.QPushButton("我的分类")
        btn.setObjectName("navBtn")
        btn.setCursor(QtCore.Qt.PointingHandCursor)
        btn.setCheckable(True)
        btn.clicked.connect(lambda: self._switch_page(3))  # 第 4 页
        self._nav_buttons.append(btn)

        # 把按钮插入到 nav_container 的 layout 中（在 stretch 之前）
        nav_layout = self._nav_container.layout()
        nav_layout.insertWidget(nav_layout.count() - 1, btn)

    def _build_my_page(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.addWidget(QtWidgets.QLabel("这是我新加的分类页"))
        return page
    
    def _inject_my_tools(self):
        """在工具页的网格中追加自定义按钮"""
        # 找到工具页里的 grid（_build_tools_page 中创建的 grid_box）
        tools_page = self._stack.widget(0)
        # 遍历找到 QGroupBox("可用工具")
        for child in tools_page.findChildren(QtWidgets.QGroupBox):
            if child.title() == "可用工具":
                grid = child.layout()
                # 在第 4 行第 0 列追加你的工具按钮
                btn = QtWidgets.QPushButton("我的自定义工具")
                btn.setMinimumHeight(50)
                btn.setCursor(QtCore.Qt.PointingHandCursor)
                btn.clicked.connect(self._open_mytool)
                grid.addWidget(btn, 4, 0)
                break
    
    # def _open_mytool(self):
    #     if self._mytool_win is None:
    #         self._mytool_win = MyToolWindow()
    #         self._mytool_win.setStyleSheet(MainUi._global_stylestring())
    #     self._mytool_win.show()

# ── 入口 ───────────────────────────────────────────────────
if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication([])
    window = MyMainUi()
    window.show()
    sys.exit(app.exec_())