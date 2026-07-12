"""
SettingsDialog — 设置对话框

主题风格（md3 / md2 / qt / winui3）与深浅模式（auto / light / dark）切换。
"""

from hopekit.qt_compat import QDialog, QPushButton, QtWidgets
from hopekit.theme import theme
from Styles import styles


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setFixedSize(460, 520)
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

        # ---- 主题风格 ----
        style_box = QtWidgets.QGroupBox("主题风格")
        style_layout = QtWidgets.QVBoxLayout(style_box)
        style_layout.setSpacing(10)

        self._style_md3 = QtWidgets.QRadioButton("Material Design 3（默认，动态强调色 + 大圆角）")
        self._style_md2 = QtWidgets.QRadioButton("Material Design 2（扁平化 + 阴影 + 4px 圆角）")
        self._style_qt = QtWidgets.QRadioButton("Qt 原生风格（使用 Qt 默认控件外观）")

        cur_style = theme.style
        if cur_style == "md2":
            self._style_md2.setChecked(True)
        elif cur_style == "qt":
            self._style_qt.setChecked(True)
        else:
            self._style_md3.setChecked(True)

        style_layout.addWidget(self._style_md3)
        style_layout.addWidget(self._style_md2)
        style_layout.addWidget(self._style_qt)
        layout.addWidget(style_box)

        # ---- 深浅色模式 ----
        mode_box = QtWidgets.QGroupBox("深浅模式")
        mode_layout = QtWidgets.QVBoxLayout(mode_box)
        mode_layout.setSpacing(10)

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

        mode_layout.addWidget(self._auto_btn)
        mode_layout.addWidget(self._light_btn)
        mode_layout.addWidget(self._dark_btn)
        layout.addWidget(mode_box)

        hint = QtWidgets.QLabel("选择主题后将立即应用到整个界面。")
        hint.setStyleSheet(
            f"color:{theme.colors['on_surface_variant']}; font-size:9pt;"
        )
        layout.addWidget(hint)

        layout.addStretch(1)

        btn_row = QtWidgets.QHBoxLayout()
        btn_row.addStretch(1)
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        ok_btn = QPushButton("应用")
        ok_btn.clicked.connect(self._apply)
        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(ok_btn)
        layout.addLayout(btn_row)

    def _apply(self):
        if self._style_md2.isChecked():
            theme.set_style("md2")
        elif self._style_qt.isChecked():
            theme.set_style("qt")
        else:
            theme.set_style("md3")

        if self._auto_btn.isChecked():
            theme.set_mode("auto")
        elif self._dark_btn.isChecked():
            theme.set_mode("dark")
        else:
            theme.set_mode("light")
        self.accept()

    def _apply_dialog_style(self):
        self.setStyleSheet(styles.dialog_stylesheet(theme.colors))
