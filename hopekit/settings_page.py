"""
SettingsPage — 设置页面（嵌入主区域，非弹窗）

二级菜单结构:
  - 主题: 主题风格 + 深浅模式 + 导入主题文件
  - 关于: (预留)

布局:
  左侧二级菜单 | 右侧内容区
  ┌─────────┬──────────────────────┐
  │ ● 主题   │  主题风格             │
  │ ○ 关于   │  ○ MD3  ○ MD2  ○ Qt  │
  │          │  深浅模式             │
  │          │  ○ auto ○ 浅 ○ 深    │
  │          │       [导入主题文件]  │
  └─────────┴──────────────────────┘
"""

import json

from hopekit.qt_compat import (
    QtCore, QtWidgets,
    QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
)
from hopekit.theme import theme
from hopekit.paths import config_path


class ThemePage(QtWidgets.QWidget):
    """主题设置子页面"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._main_window = None
        self._build_ui()

    def set_main_window(self, mw):
        self._main_window = mw

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        # ---- 主题风格 ----
        style_box = QtWidgets.QGroupBox("主题风格")
        style_layout = QVBoxLayout(style_box)
        style_layout.setSpacing(10)

        self._style_md3 = QtWidgets.QRadioButton(
            "Material Design 3（默认，动态强调色 + 大圆角）"
        )
        self._style_md2 = QtWidgets.QRadioButton(
            "Material Design 2（Indigo 500 + 扁平化 + 4px 圆角）"
        )
        self._style_qt = QtWidgets.QRadioButton(
            "Qt 原生风格（使用 Qt 默认控件外观）"
        )
        self._style_winui3 = QtWidgets.QRadioButton(
            "WinUI3 / Fluent Design（Win11 Mica + Segoe UI Variable + 分层圆角）"
        )
        self._style_win10fluent = QtWidgets.QRadioButton(
            "Win10 Fluent（Acrylic + Segoe UI + 4dp 圆角 + 左竖条选中）"
        )
        self._style_gnome = QtWidgets.QRadioButton(
            "GNOME / libadwaita（Cantarell 字体 + 6/12px 圆角 + 纯色背景）"
        )
        self._style_kde = QtWidgets.QRadioButton(
            "KDE Plasma / Breeze（半透明面板 + 4/8px 圆角）"
        )
        self._style_cupertino = QtWidgets.QRadioButton(
            "macOS / Cupertino（SF 字体 + 8/12px 圆角 + 实心选中态）"
        )
        self._style_chromeos = QtWidgets.QRadioButton(
            "ChromeOS / Material Desktop（Google Sans + 8/12px 圆角）"
        )

        cur_style = theme.style
        if cur_style == "md2":
            self._style_md2.setChecked(True)
        elif cur_style == "qt":
            self._style_qt.setChecked(True)
        elif cur_style == "winui3":
            self._style_winui3.setChecked(True)
        elif cur_style == "win10fluent":
            self._style_win10fluent.setChecked(True)
        elif cur_style == "gnome":
            self._style_gnome.setChecked(True)
        elif cur_style == "kde":
            self._style_kde.setChecked(True)
        elif cur_style == "cupertino":
            self._style_cupertino.setChecked(True)
        elif cur_style == "chromeos":
            self._style_chromeos.setChecked(True)
        else:
            self._style_md3.setChecked(True)

        # 切换时立即应用
        self._style_md3.toggled.connect(self._on_style_changed)
        self._style_md2.toggled.connect(self._on_style_changed)
        self._style_qt.toggled.connect(self._on_style_changed)
        self._style_winui3.toggled.connect(self._on_style_changed)
        self._style_win10fluent.toggled.connect(self._on_style_changed)
        self._style_gnome.toggled.connect(self._on_style_changed)
        self._style_kde.toggled.connect(self._on_style_changed)
        self._style_cupertino.toggled.connect(self._on_style_changed)
        self._style_chromeos.toggled.connect(self._on_style_changed)

        style_layout.addWidget(self._style_md3)
        style_layout.addWidget(self._style_md2)
        style_layout.addWidget(self._style_qt)
        style_layout.addWidget(self._style_winui3)
        style_layout.addWidget(self._style_win10fluent)
        style_layout.addWidget(self._style_gnome)
        style_layout.addWidget(self._style_kde)
        style_layout.addWidget(self._style_cupertino)
        style_layout.addWidget(self._style_chromeos)
        layout.addWidget(style_box)

        # ---- 深浅模式 ----
        mode_box = QtWidgets.QGroupBox("深浅模式")
        mode_layout = QVBoxLayout(mode_box)
        mode_layout.setSpacing(10)

        self._auto_btn = QtWidgets.QRadioButton("跟随 Windows（自动匹配系统深浅色）")
        self._light_btn = QtWidgets.QRadioButton("浅色模式")
        self._dark_btn = QtWidgets.QRadioButton("深色模式")

        current = theme.mode
        if current == "auto":
            self._auto_btn.setChecked(True)
        elif current == "dark":
            self._dark_btn.setChecked(True)
        else:
            self._light_btn.setChecked(True)

        self._auto_btn.toggled.connect(self._on_mode_changed)
        self._light_btn.toggled.connect(self._on_mode_changed)
        self._dark_btn.toggled.connect(self._on_mode_changed)

        mode_layout.addWidget(self._auto_btn)
        mode_layout.addWidget(self._light_btn)
        mode_layout.addWidget(self._dark_btn)
        layout.addWidget(mode_box)

        # ---- 当前主题信息 ----
        self._info_label = QLabel()
        self._info_label.setStyleSheet("font-size:9pt; opacity:0.7;")
        self._update_info()
        layout.addWidget(self._info_label)

        layout.addStretch(1)

        # ---- 右下角浮动导入按钮（FAB / 系统按钮，依主题风格）----
        self._import_btn = QPushButton()
        self._import_btn.setObjectName("importFab")
        self._import_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self._import_btn.setToolTip("导入主题文件")
        self._import_btn.setFixedSize(56, 56)
        self._import_btn.clicked.connect(self._import_theme)
        self._update_import_btn_appearance()

        fab_row = QHBoxLayout()
        fab_row.addStretch(1)
        fab_row.addWidget(self._import_btn)
        layout.addLayout(fab_row)

    def _on_style_changed(self):
        """单选切换时立即应用主题风格"""
        if self._style_md2.isChecked():
            new_style = "md2"
        elif self._style_qt.isChecked():
            new_style = "qt"
        elif self._style_winui3.isChecked():
            new_style = "winui3"
        elif self._style_win10fluent.isChecked():
            new_style = "win10fluent"
        elif self._style_gnome.isChecked():
            new_style = "gnome"
        elif self._style_kde.isChecked():
            new_style = "kde"
        elif self._style_cupertino.isChecked():
            new_style = "cupertino"
        elif self._style_chromeos.isChecked():
            new_style = "chromeos"
        else:
            new_style = "md3"

        if theme.style != new_style:
            theme.set_style(new_style)
            self._apply_theme()

    def _on_mode_changed(self):
        """单选切换时立即应用深浅模式"""
        if not (self._auto_btn.isChecked() or
                self._light_btn.isChecked() or
                self._dark_btn.isChecked()):
            return

        if self._auto_btn.isChecked():
            new_mode = "auto"
        elif self._dark_btn.isChecked():
            new_mode = "dark"
        else:
            new_mode = "light"

        if theme.mode != new_mode:
            theme.set_mode(new_mode)
            self._apply_theme()

    def _apply_theme(self):
        """应用主题并刷新所有窗口"""
        if self._main_window:
            self._main_window._apply_style()
            self._main_window._refresh_child_window_styles()
        self._update_info()
        self._update_import_btn_appearance()

    def _update_import_btn_appearance(self):
        """根据当前主题风格调整导入按钮外观（文字/尺寸）"""
        style = theme.style
        if style == "qt":
            self._import_btn.setText("导入主题文件")
            self._import_btn.setFixedSize(120, 32)
        elif style in ("winui3", "win10fluent", "gnome", "kde", "cupertino", "chromeos"):
            # WinUI3/GNOME/KDE/Cupertino/ChromeOS: 圆角矩形按钮
            self._import_btn.setText("+")
            self._import_btn.setFixedSize(48, 48)
        else:
            # MD3/MD2: 圆形 FAB
            self._import_btn.setText("+")
            self._import_btn.setFixedSize(56, 56)

    def _update_info(self):
        c = theme.colors
        self._info_label.setText(
            f"当前: {theme.style} / {theme.mode}  |  "
            f"primary={c['primary']}  surface={c['surface']}"
        )

    def _import_theme(self):
        """导入外部主题文件（JSON 格式）"""
        from hopekit.qt_compat import QtWidgets as QW

        file_path, _ = QW.QFileDialog.getOpenFileName(
            self,
            "导入主题文件",
            "",
            "主题文件 (*.json);;所有文件 (*.*)"
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # 期望格式: {"style": "md3/md2/qt", "mode": "auto/light/dark"}
            if "style" in data:
                theme.set_style(data["style"])
            if "mode" in data:
                theme.set_mode(data["mode"])

            # 更新 UI 选中态
            style = theme.style
            if style == "md2":
                self._style_md2.setChecked(True)
            elif style == "qt":
                self._style_qt.setChecked(True)
            elif style == "winui3":
                self._style_winui3.setChecked(True)
            elif style == "win10fluent":
                self._style_win10fluent.setChecked(True)
            elif style == "gnome":
                self._style_gnome.setChecked(True)
            elif style == "kde":
                self._style_kde.setChecked(True)
            elif style == "cupertino":
                self._style_cupertino.setChecked(True)
            elif style == "chromeos":
                self._style_chromeos.setChecked(True)
            else:
                self._style_md3.setChecked(True)

            mode = theme.mode
            if mode == "auto":
                self._auto_btn.setChecked(True)
            elif mode == "dark":
                self._dark_btn.setChecked(True)
            else:
                self._light_btn.setChecked(True)

            self._apply_theme()

            QW.QMessageBox.information(
                self, "导入成功",
                f"主题文件已导入:\n风格={theme.style}\n模式={theme.mode}"
            )
        except (json.JSONDecodeError, KeyError) as e:
            QW.QMessageBox.warning(
                self, "导入失败",
                f"主题文件格式错误:\n{e}"
            )
        except OSError as e:
            QW.QMessageBox.warning(
                self, "导入失败",
                f"无法读取文件:\n{e}"
            )

    def refresh_theme_display(self):
        """外部切换主题后刷新选中态"""
        style = theme.style
        if style == "md2":
            self._style_md2.setChecked(True)
        elif style == "qt":
            self._style_qt.setChecked(True)
        elif style == "winui3":
            self._style_winui3.setChecked(True)
        elif style == "win10fluent":
            self._style_win10fluent.setChecked(True)
        elif style == "gnome":
            self._style_gnome.setChecked(True)
        elif style == "kde":
            self._style_kde.setChecked(True)
        elif style == "cupertino":
            self._style_cupertino.setChecked(True)
        elif style == "chromeos":
            self._style_chromeos.setChecked(True)
        else:
            self._style_md3.setChecked(True)

        mode = theme.mode
        if mode == "auto":
            self._auto_btn.setChecked(True)
        elif mode == "dark":
            self._dark_btn.setChecked(True)
        else:
            self._light_btn.setChecked(True)

        self._update_info()
        self._update_import_btn_appearance()


class AboutPage(QtWidgets.QWidget):
    """关于页面（预留）"""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("关于 HopeKit")
        label.setStyleSheet("font-size: 16pt; font-weight: 600;")
        layout.addWidget(label)

        layout.addStretch(1)


class SettingsPage(QtWidgets.QWidget):
    """设置页面 — 左侧二级菜单 + 右侧内容区"""

    # 二级菜单项: (key, 显示名)
    _SUB_PAGES = [
        ("theme", "主题"),
        ("about", "关于"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._sub_nav_buttons = []
        self._sub_pages = {}
        self._build_ui()

    def _build_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ---- 左侧二级菜单 ----
        self._sub_nav = QtWidgets.QFrame(self)
        self._sub_nav.setObjectName("subNav")
        self._sub_nav.setFixedWidth(160)

        sub_layout = QVBoxLayout(self._sub_nav)
        sub_layout.setContentsMargins(8, 12, 8, 12)
        sub_layout.setSpacing(6)

        sub_title = QLabel("设置")
        sub_title.setObjectName("subNavTitle")
        sub_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        sub_layout.addWidget(sub_title)

        for key, display in self._SUB_PAGES:
            btn = QPushButton(display)
            btn.setObjectName("subNavBtn")
            btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            btn.setCheckable(True)
            btn.clicked.connect(lambda _checked, k=key: self._switch_sub(k))
            sub_layout.addWidget(btn)
            self._sub_nav_buttons.append((key, btn))

        sub_layout.addStretch(1)
        layout.addWidget(self._sub_nav)

        # ---- 右侧内容区 ----
        content = QtWidgets.QWidget(self)
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 16, 20, 16)
        content_layout.setSpacing(12)

        self._sub_stack = QtWidgets.QStackedWidget()

        # 主题页
        self._theme_page = ThemePage()
        self._sub_stack.addWidget(self._theme_page)
        self._sub_pages["theme"] = self._theme_page

        # 关于页
        self._about_page = AboutPage()
        self._sub_stack.addWidget(self._about_page)
        self._sub_pages["about"] = self._about_page

        content_layout.addWidget(self._sub_stack)
        layout.addWidget(content, 1)

        # 默认选中主题
        self._switch_sub("theme")

    def _switch_sub(self, key: str):
        """切换二级菜单"""
        if key in self._sub_pages:
            self._sub_stack.setCurrentWidget(self._sub_pages[key])
        for k, btn in self._sub_nav_buttons:
            btn.setChecked(k == key)

    def set_main_window(self, mw):
        """注入主窗口引用，用于主题切换时刷新全局样式"""
        self._theme_page.set_main_window(mw)

    def refresh_theme_display(self):
        self._theme_page.refresh_theme_display()
