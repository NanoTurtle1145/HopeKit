"""
HopeKit 2.0.0 — 主程序入口
瘦身版：主题管理在 hopekit/theme.py，插件注册在 hopekit/registry.py，
工具模块在 plugins/，示例在 examples/。
"""

import sys

from hopekit.qt_compat import (
    QtCore, QtGui, QtWidgets,
    QMainWindow, QDialog, QApplication,
    QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGridLayout, QGroupBox,
    Qt,
)
from hopekit.theme import theme
from hopekit.paths import resource_path
from hopekit.registry import ModuleRegistry, discover_plugins
from Styles import styles


VERSION = "2.0.0"


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setFixedSize(420, 360)
        self._build_ui()
        self._apply_dialog_style()

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QtWidgets.QLabel("设置")
        title.setObjectName("pageTitle")
        title.setStyleSheet(
            f"font-size:20pt; font-weight:500; color:{theme.colors['on_surface']};"
        )
        layout.addWidget(title)

        theme_box = QtWidgets.QGroupBox("外观主题")
        theme_layout = QtWidgets.QVBoxLayout(theme_box)
        theme_layout.setSpacing(10)

        self._auto_btn = QtWidgets.QRadioButton("跟随 Windows（自动匹配系统强调色与深浅色）")
        self._light_btn = QtWidgets.QRadioButton("浅色模式")
        self._dark_btn = QtWidgets.QRadioButton("深色模式")

        current = theme.mode
        if current == "auto":
            self._auto_btn.setChecked(True)
        elif current == "dark":
            self._dark_btn.setChecked(True)
        else:
            self._light_btn.setChecked(True)

        theme_layout.addWidget(self._auto_btn)
        theme_layout.addWidget(self._light_btn)
        theme_layout.addWidget(self._dark_btn)
        layout.addWidget(theme_box)

        hint = QtWidgets.QLabel("选择主题后将立即应用到整个界面。")
        hint.setStyleSheet(
            f"color:{theme.colors['on_surface_variant']}; font-size:9pt;"
        )
        layout.addWidget(hint)

        layout.addStretch(1)

        btn_row = QtWidgets.QHBoxLayout()
        btn_row.addStretch(1)
        cancel_btn = QtWidgets.QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        ok_btn = QtWidgets.QPushButton("应用")
        ok_btn.clicked.connect(self._apply)
        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(ok_btn)
        layout.addLayout(btn_row)

    def _apply(self):
        if self._auto_btn.isChecked():
            theme.set_mode("auto")
        elif self._dark_btn.isChecked():
            theme.set_mode("dark")
        else:
            theme.set_mode("light")
        self.accept()

    def _apply_dialog_style(self):
        self.setStyleSheet(styles.dialog_stylesheet(theme.colors))


class MainUi(QMainWindow):
    _SIDEBAR_EXPANDED = 210
    _SIDEBAR_COLLAPSED = 48

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"HopeKit {VERSION}")
        self.setFixedSize(1200, 665)
        self._sidebar_collapsed = False
        self._nav_buttons = []
        self._page_widgets = {}
        self._build_ui()
        self._apply_style()

    def _build_ui(self):
        central = QtWidgets.QWidget(self)
        self.setCentralWidget(central)

        main_layout = QtWidgets.QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self._sidebar = QtWidgets.QFrame(central)
        self._sidebar.setObjectName("sidebar")
        self._sidebar.setFixedWidth(self._SIDEBAR_EXPANDED)

        sidebar_layout = QtWidgets.QVBoxLayout(self._sidebar)
        sidebar_layout.setContentsMargins(8, 12, 8, 12)
        sidebar_layout.setSpacing(6)

        self._sidebar_title = QtWidgets.QLabel("导航菜单")
        self._sidebar_title.setObjectName("sidebarTitle")
        self._sidebar_title.setAlignment(QtCore.Qt.AlignCenter)
        sidebar_layout.addWidget(self._sidebar_title)

        self._toggle_btn = QtWidgets.QPushButton("◀  折叠")
        self._toggle_btn.setObjectName("toggleBtn")
        self._toggle_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self._toggle_btn.clicked.connect(self._toggle_sidebar)
        sidebar_layout.addWidget(self._toggle_btn)

        self._nav_container = QtWidgets.QWidget(self._sidebar)
        nav_layout = QtWidgets.QVBoxLayout(self._nav_container)
        nav_layout.setContentsMargins(0, 6, 0, 0)
        nav_layout.setSpacing(6)

        categories = ModuleRegistry.categories()
        for idx, cat in enumerate(categories):
            btn = QtWidgets.QPushButton(cat)
            btn.setObjectName("navBtn")
            btn.setCursor(QtCore.Qt.PointingHandCursor)
            btn.setCheckable(True)
            btn.clicked.connect(
                lambda _checked, c=cat: self._switch_category(c)
            )
            nav_layout.addWidget(btn)
            self._nav_buttons.append((cat, btn))

        nav_layout.addStretch(1)
        sidebar_layout.addWidget(self._nav_container, 1)

        self._settings_btn = QtWidgets.QPushButton("设置")
        self._settings_btn.setObjectName("settingsBtn")
        self._settings_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self._settings_btn.clicked.connect(self._open_settings)
        sidebar_layout.addWidget(self._settings_btn)

        self._exit_btn = QtWidgets.QPushButton("退出...")
        self._exit_btn.setObjectName("exitBtn")
        self._exit_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self._exit_btn.clicked.connect(self.close)
        sidebar_layout.addWidget(self._exit_btn)

        main_layout.addWidget(self._sidebar)

        content = QtWidgets.QWidget(central)
        content_layout = QtWidgets.QVBoxLayout(content)
        content_layout.setContentsMargins(16, 16, 16, 16)
        content_layout.setSpacing(12)

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setSpacing(12)

        logo = QtWidgets.QLabel()
        pix = QtGui.QPixmap(resource_path("logo.jpg"))
        if not pix.isNull():
            logo.setPixmap(pix.scaledToHeight(72, QtCore.Qt.SmoothTransformation))
        logo.setFixedSize(72, 72)
        header_layout.addWidget(logo, 0, QtCore.Qt.AlignVCenter)

        title_box = QtWidgets.QVBoxLayout()
        title_box.setSpacing(2)
        title_lbl = QtWidgets.QLabel(f"HopeKit {VERSION}")
        title_lbl.setStyleSheet("font-size:16pt; font-weight:600; color:#333;")
        tip = QtWidgets.QLabel(
            '<span style="font-size:18pt; color:#0000ff;">你今天看起来很聪明！</span>'
        )
        title_box.addWidget(title_lbl)
        title_box.addWidget(tip)
        header_layout.addLayout(title_box)
        header_layout.addStretch(1)
        content_layout.addLayout(header_layout)

        self._stack = QtWidgets.QStackedWidget()
        for cat in categories:
            page = self._build_category_page(cat)
            self._stack.addWidget(page)
            self._page_widgets[cat] = page
        content_layout.addWidget(self._stack, 1)

        main_layout.addWidget(content, 1)

        if categories:
            self._switch_category(categories[0])

        self.statusBar()
        menu_bar = QtWidgets.QMenuBar(self)
        self.setMenuBar(menu_bar)

    def _build_category_page(self, category: str):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setSpacing(12)

        title = QtWidgets.QLabel(category)
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        modules = ModuleRegistry.by_category(category)

        page_modules = {n: i for n, i in modules.items() if i.get("kind") == "page"}
        window_modules = {n: i for n, i in modules.items() if i.get("kind") != "page"}

        if page_modules:
            for name, info in page_modules.items():
                if not info["enabled"]:
                    continue
                widget = ModuleRegistry.get_or_create(name, self)
                if widget is not None:
                    layout.addWidget(widget, 1)

        if window_modules:
            if category == "links":
                self._build_links_list(layout, window_modules)
            else:
                self._build_tools_grid(layout, window_modules)

        layout.addStretch(1)
        return page

    def _build_tools_grid(self, parent_layout, modules: dict):
        grid_box = QGroupBox("可用工具")
        grid = QGridLayout(grid_box)
        grid.setSpacing(10)

        col_count = 2
        for idx, (name, info) in enumerate(modules.items()):
            row = idx // col_count
            col = idx % col_count
            text = f"{info['icon']}  {info['title']}" if info['icon'] else info['title']
            btn = QPushButton(text)
            btn.setMinimumHeight(50)
            btn.setCursor(QtCore.Qt.PointingHandCursor)
            if info["enabled"]:
                btn.clicked.connect(lambda _=False, n=name: self._open_module(n))
            else:
                btn.setEnabled(False)
            grid.addWidget(btn, row, col)

        parent_layout.addWidget(grid_box)

    def _build_links_list(self, parent_layout, modules: dict):
        dev_links = {}
        contact_links = {}
        for name, info in modules.items():
            if name in ("website", "copyright_link", "qq_group", "sports"):
                dev_links[name] = info
            else:
                contact_links[name] = info

        if dev_links:
            links_box = QGroupBox("开发者新闻")
            links_layout = QVBoxLayout(links_box)
            links_layout.setSpacing(10)
            for name, info in dev_links.items():
                text = f"{info['icon']}  {info['title']}" if info['icon'] else info['title']
                row = QHBoxLayout()
                lbl = QLabel(f'<span style="font-size:14pt; font-weight:600;">{text}</span>')
                btn = QPushButton("查看")
                btn.setCursor(QtCore.Qt.PointingHandCursor)
                if info["enabled"]:
                    btn.clicked.connect(lambda _=False, n=name: self._open_module(n))
                else:
                    btn.setEnabled(False)
                row.addWidget(lbl)
                row.addStretch(1)
                row.addWidget(btn)
                links_layout.addLayout(row)
            parent_layout.addWidget(links_box)

        if contact_links:
            contact_box = QGroupBox("联系作者")
            contact_layout = QVBoxLayout(contact_box)
            contact_layout.setSpacing(10)
            for name, info in contact_links.items():
                text = f"{info['icon']}  {info['title']}" if info['icon'] else info['title']
                row = QHBoxLayout()
                lbl = QLabel(f'<span style="font-size:14pt; font-weight:600;">{text}</span>')
                btn = QPushButton("查看")
                btn.setCursor(QtCore.Qt.PointingHandCursor)
                if info["enabled"]:
                    btn.clicked.connect(lambda _=False, n=name: self._open_module(n))
                else:
                    btn.setEnabled(False)
                row.addWidget(lbl)
                row.addStretch(1)
                row.addWidget(btn)
                contact_layout.addLayout(row)
            parent_layout.addWidget(contact_box)

    def _switch_category(self, category: str):
        if category in self._page_widgets:
            self._stack.setCurrentWidget(self._page_widgets[category])
        for cat, btn in self._nav_buttons:
            btn.setChecked(cat == category)

    def _toggle_sidebar(self):
        self._sidebar_collapsed = not self._sidebar_collapsed
        if self._sidebar_collapsed:
            self._sidebar.setFixedWidth(self._SIDEBAR_COLLAPSED)
            self._toggle_btn.setText("▶")
            self._sidebar_title.setVisible(False)
            self._nav_container.setVisible(False)
            self._exit_btn.setText("×")
            self._settings_btn.setText("⚙")
        else:
            self._sidebar.setFixedWidth(self._SIDEBAR_EXPANDED)
            self._toggle_btn.setText("◀  折叠")
            self._sidebar_title.setVisible(True)
            self._nav_container.setVisible(True)
            self._exit_btn.setText("退出...")
            self._settings_btn.setText("设置")

    def _open_module(self, name: str):
        info = ModuleRegistry.get(name)
        if not info or not info["enabled"]:
            return

        win = ModuleRegistry.get_or_create(name, self)
        if win is None:
            return

        try:
            win.setStyleSheet("")
            win.setStyleSheet(self._global_stylestring())
        except Exception:
            pass

        win.show()
        win.raise_()
        win.activateWindow()

    def _open_settings(self):
        dlg = SettingsDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            self._apply_style()
            self._refresh_child_window_styles()

    def _refresh_child_window_styles(self):
        for name in list(ModuleRegistry._instances.keys()):
            win = ModuleRegistry._instances.get(name)
            if win is not None:
                try:
                    win.setStyleSheet("")
                    win.setStyleSheet(self._global_stylestring())
                except Exception:
                    pass

    @staticmethod
    def _global_stylestring():
        return styles.global_stylesheet(theme.colors)

    def _apply_style(self):
        app = QApplication.instance()
        if app is not None:
            app.setStyleSheet(self._global_stylestring())
        self.setStyleSheet(styles.main_stylesheet(theme.colors))


if __name__ == "__main__":
    discover_plugins("plugins")

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    window = MainUi()
    window.show()
    sys.exit(app.exec_())
