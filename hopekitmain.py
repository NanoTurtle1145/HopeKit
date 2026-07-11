"""
HopeKit 2.0.0-revived — 主程序入口
清理后的版本：移除了死代码、注释掉的代码块、泄漏的 API Key、
未使用的类（ticket/ChatGPT/tool_ex），以及重复/冗余导入。
聊天室模块已拆分至 chat_room.py
"""

import json
import os
import subprocess
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import (
    QMainWindow, QDialog,
    QApplication, QLabel, QLineEdit,
    QPushButton, QGridLayout, QTextEdit,
)

from chat_room import MainWin, OtherWindow, WebWindow

from Styles import styles


# ============================================================
#  路径处理 — 兼容 PyInstaller 打包
# ============================================================
def resource_path(relative: str) -> str:
    """只读资源路径（logo 等），打包后从 _MEIPASS 解压目录加载。"""
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS  # type: ignore[attr-defined]
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative)


def config_path(filename: str) -> str:
    """可读写配置文件路径（theme.json），放在 exe 同目录便于持久化。"""
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, filename)


# ============================================================
#  ThemeManager — Material Design 3 主题管理（跟随 Windows + 深/浅色 + 持久化）
# ============================================================
class ThemeManager:
    """
    Material Design 3 风格主题管理器。
    支持 auto / light / dark 三种模式：
      - auto:  跟随 Windows 系统强调色 + 深浅色主题
      - light: 固定浅色（使用 Windows 强调色生成调色板）
      - dark:  固定深色（使用 Windows 强调色生成调色板）
    配色持久化到本地 JSON。
    """
    _CONFIG_PATH = config_path("theme.json")

    # 圆角常量
    _RADII = {
        "card_radius": "16px",
        "btn_radius":  "20px",
        "nav_radius":  "28px",
    }

    def __init__(self):
        self._mode = "auto"
        self.load()

    # ---- 模式属性 ----
    @property
    def mode(self) -> str:
        return self._mode

    @property
    def is_dark(self) -> bool:
        if self._mode == "dark":
            return True
        if self._mode == "light":
            return False
        # auto: 读取 Windows 深浅色设置
        return self._read_windows_dark_mode()

    @property
    def colors(self) -> dict:
        accent = self._read_windows_accent()
        return self._build_palette(accent, self.is_dark)

    # ---- 模式切换 ----
    def set_mode(self, mode: str):
        if mode in ("auto", "light", "dark"):
            self._mode = mode
            self.save()

    def load(self):
        try:
            with open(self._CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data.get("mode") in ("auto", "light", "dark"):
                self._mode = data["mode"]
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            pass

    def save(self):
        try:
            with open(self._CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump({"mode": self._mode}, f, ensure_ascii=False, indent=2)
        except OSError:
            pass

    # ============================================================
    #  读取 Windows 系统配色
    # ============================================================
    @staticmethod
    def _read_windows_accent() -> tuple:
        """
        从注册表读取 Windows 强调色。
        返回 (r, g, b) 元组，失败时返回默认紫色 (103, 80, 164)。
        """
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\DWM"
            )
            value, _ = winreg.QueryValueEx(key, "AccentColor")
            winreg.CloseKey(key)
            # AccentColor 是 ABGR 格式（0xAABBGGRR）
            r = value & 0xFF
            g = (value >> 8) & 0xFF
            b = (value >> 16) & 0xFF
            return (r, g, b)
        except Exception:
            return (103, 80, 164)

    @staticmethod
    def _read_windows_dark_mode() -> bool:
        """
        读取 Windows 应用深浅色主题设置。
        返回 True 表示深色模式，失败时返回 False。
        """
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            )
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            return value == 0
        except Exception:
            return False

    # ============================================================
    #  根据 accent 色生成 MD3 调色板
    # ============================================================
    @staticmethod
    def _mix(c1: tuple, c2: tuple, t: float) -> tuple:
        """线性混合两个 RGB 颜色，t=0 得 c1，t=1 得 c2"""
        return (
            round(c1[0] + (c2[0] - c1[0]) * t),
            round(c1[1] + (c2[1] - c1[1]) * t),
            round(c1[2] + (c2[2] - c1[2]) * t),
        )

    @staticmethod
    def _luminance(rgb: tuple) -> float:
        """计算相对亮度（0~1）"""
        def chan(v):
            v = v / 255.0
            return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
        return 0.2126 * chan(rgb[0]) + 0.7152 * chan(rgb[1]) + 0.0722 * chan(rgb[2])

    @classmethod
    def _on_color(cls, bg: tuple) -> str:
        """根据背景亮度返回黑或白作为 on_color"""
        return "#FFFFFF" if cls._luminance(bg) < 0.5 else "#000000"

    @classmethod
    def _build_palette(cls, accent: tuple, dark: bool) -> dict:
        """
        根据 accent 色 + 深浅标志，生成完整的 MD3 调色板。
        通过 accent 色的明暗混合派生出 primary / container / secondary 等。
        """
        r, g, b = accent

        if dark:
            # 深色模式：primary 提亮，container 压暗
            primary = cls._mix(accent, (255, 255, 255), 0.4)
            primary_container = cls._mix(accent, (0, 0, 0), 0.3)
            on_primary_container = cls._mix(accent, (255, 255, 255), 0.85)

            secondary = cls._mix(accent, (160, 160, 170), 0.5)
            secondary_container = cls._mix(accent, (50, 50, 60), 0.7)
            on_secondary_container = cls._mix(accent, (255, 255, 255), 0.85)

            surface = (28, 27, 31)
            on_surface = (230, 225, 229)
            surface_variant = (73, 69, 79)
            on_surface_variant = (202, 196, 208)
            background = (20, 18, 24)
            on_background = (230, 225, 229)
            outline = (147, 143, 153)
            sidebar_bg = cls._mix(accent, (30, 30, 40), 0.85)
            sidebar_text = (230, 225, 229)
            sidebar_hover = cls._mix(accent, (60, 60, 75), 0.6)
            sidebar_active = cls._mix(accent, (40, 40, 50), 0.7)
            error = (242, 184, 181)
            on_error = (96, 20, 16)
        else:
            # 浅色模式：primary 用原色，container 提亮
            primary = accent
            primary_container = cls._mix(accent, (255, 255, 255), 0.78)
            on_primary_container = cls._mix(accent, (0, 0, 0), 0.7)

            secondary = cls._mix(accent, (98, 91, 113), 0.5)
            secondary_container = cls._mix(accent, (240, 235, 245), 0.8)
            on_secondary_container = (29, 25, 43)

            surface = (255, 251, 254)
            on_surface = (28, 27, 31)
            surface_variant = (231, 224, 236)
            on_surface_variant = (73, 69, 79)
            background = (255, 251, 254)
            on_background = (28, 27, 31)
            outline = (121, 116, 126)
            sidebar_bg = cls._mix(accent, (245, 243, 248), 0.88)
            sidebar_text = (29, 25, 43)
            sidebar_hover = cls._mix(accent, (255, 255, 255), 0.75)
            sidebar_active = cls._mix(accent, (255, 255, 255), 0.82)
            error = (179, 38, 30)
            on_error = (255, 255, 255)

        on_primary = cls._on_color(primary)
        on_secondary = cls._on_color(secondary)

        def hexstr(rgb):
            return "#{:02X}{:02X}{:02X}".format(*rgb)

        palette = {
            "primary":             hexstr(primary),
            "on_primary":          on_primary,
            "primary_container":   hexstr(primary_container),
            "on_primary_container":hexstr(on_primary_container),
            "secondary":           hexstr(secondary),
            "on_secondary":        on_secondary,
            "secondary_container": hexstr(secondary_container),
            "on_secondary_container": hexstr(on_secondary_container),
            "surface":             hexstr(surface),
            "on_surface":          hexstr(on_surface),
            "surface_variant":     hexstr(surface_variant),
            "on_surface_variant":  hexstr(on_surface_variant),
            "background":          hexstr(background),
            "on_background":       hexstr(on_background),
            "outline":             hexstr(outline),
            "error":               hexstr(error),
            "on_error":            on_error,
            "shadow":              "#000000",
            "sidebar_bg":          hexstr(sidebar_bg),
            "sidebar_text":        hexstr(sidebar_text),
            "sidebar_hover":       hexstr(sidebar_hover),
            "sidebar_active":      hexstr(sidebar_active),
            "sidebar_active_border": hexstr(primary),
            "exit_btn_bg":         hexstr(error),
            "exit_btn_hover":      hexstr(cls._mix(error, (255, 255, 255), 0.2)),
        }
        palette.update(cls._RADII)
        return palette


# 全局主题实例
theme = ThemeManager()


# ============================================================
#  CaidanWindow — 彩蛋窗口
# ============================================================
class CaidanWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('彩蛋')
        text_edit = QTextEdit(self)
        text_edit.setPlainText(
            '只要功夫深，bug如井喷。\n'
            '一测三千年，测完成荒坟。\n'
            '熟识与非门，交谈非真人。\n'
            '谁解其中味，颈雄已沉沉!\n'
            '    ——致敬程序开发者\n'
            '    ——GXBF(NanoTurtle1145)\n'
            '    ——shengrui11(BusySheng)'
        )
        text_edit.setReadOnly(True)
        self.setCentralWidget(text_edit)

        button = QPushButton('关闭', self)
        button.move(100, 220)
        button.clicked.connect(self.close)
        self.setFixedSize(200, 250)


# ============================================================
#  ShutWindow — 关机命令集
# ============================================================
class ShutWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('关机命令集')
        btn = QPushButton('有注释的关机', self)
        btn.setGeometry(0, 0, 200, 41)
        btn.clicked.connect(lambda: subprocess.call(["shutdown", "-i"]))


# ============================================================
#  ShitWindow — 系统工具探索
# ============================================================
class ShitWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('探索系统屎山')
        self._shut_win = None
        self._web_win = None

        self.shutbutton = QPushButton('关机命令集', self)
        self.webbutton = QPushButton('简易官网', self)
        self.shutbutton.setGeometry(0, 0, 200, 41)
        self.webbutton.setGeometry(0, 50, 200, 41)

        self.shutbutton.clicked.connect(self._open_shut)
        self.webbutton.clicked.connect(self._open_web)

    def _open_shut(self):
        if self._shut_win is None:
            self._shut_win = ShutWindow()
        self._shut_win.show()

    def _open_web(self):
        from PyQt5.QtWidgets import QMessageBox
        from PyQt5.QtGui import QDesktopServices
        from PyQt5.QtCore import QUrl
        try:
            if self._web_win is None:
                self._web_win = WebWindow()
            self._web_win.show()
        except Exception as reason:
            QMessageBox.warning(
                self, "内置浏览器不可用",
                f"PyQtWebEngine 调用失败，已改用系统浏览器打开。\n\n错误信息：{reason}"
            )
            QDesktopServices.openUrl(QUrl("https://hopestudio.top/"))


# ============================================================
#  Calculator — 简易计算器
# ============================================================
class Calculator(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("计算器")

        self.input_line = QLineEdit()
        self.result_line = QLineEdit()
        self.result_line.setReadOnly(True)

        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+'],
            ['C'],
        ]

        layout = QGridLayout(self)
        layout.addWidget(self.input_line, 0, 0, 1, 4)
        layout.addWidget(self.result_line, 1, 0, 1, 4)

        for row_idx, button_row in enumerate(buttons, start=2):
            for col_idx, label in enumerate(button_row):
                btn = QPushButton(label)
                btn.clicked.connect(self._on_click)
                layout.addWidget(btn, row_idx, col_idx)

    def _on_click(self):
        label = self.sender().text()
        if label == "=":
            try:
                result = eval(self.input_line.text())
                self.result_line.setText(str(result))
            except Exception:
                self.result_line.setText("Error")
        elif label == "C":
            self.input_line.clear()
            self.result_line.clear()
        else:
            self.input_line.insert(label)


# ============================================================
#  CopyrightWindow — 版权声明
# ============================================================
class CopyrightWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('版权声明')
        text_edit = QTextEdit(self)
        text_edit.setPlainText(
            "版权声明\n"
            "感谢您对希望工作室的关注和支持。在使用我们的产品、服务和内容之前，"
            "请务必仔细阅读并理解本版权声明。\n\n"
            "1. 版权所有：除非另有明确说明，希望工作室拥有所有产品、服务和内容"
            "（包括但不限于文字、图像、音频、视频、软件、标志、商标等）的版权。\n\n"
            "2. 保护知识产权：未经希望工作室明确授权，禁止任何人使用、复制、修改、"
            "发布、传播、展示或运用希望工作室的知识产权内容。\n\n"
            "3. 授权使用：若您希望使用希望工作室的产品、服务或内容，"
            "请您与我们联系，获取书面授权。\n\n"
            "4. 用户提交内容：对于您在产品、服务或平台上提交的内容，"
            "您同意授予希望工作室非独占的、永久的、全球范围内的、免费的使用权许可。\n\n"
            "5. 第三方内容和链接：对于这些内容和链接，希望工作室不能保证"
            "其准确性、合法性、安全性或完整性。\n\n"
            "6. 免责声明：在法律允许的范围内，希望工作室不对因使用其产品、服务和内容"
            "而导致的任何直接或间接损失承担责任。\n\n"
            "7. 法律适用和争议解决：本版权声明受中华人民共和国法律的约束。\n\n"
            "本版权声明的解释权归希望工作室所有。\n\n"
            "希望工作室 版权所有"
        )
        text_edit.setReadOnly(True)
        self.setCentralWidget(text_edit)

        button = QPushButton('关闭', self)
        button.move(375, 465)
        button.clicked.connect(self.close)
        self.setFixedSize(500, 500)


# ============================================================
#  SettingsDialog — 设置对话框（主题深/浅色切换）
# ============================================================
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

        # 主题选择区
        theme_box = QtWidgets.QGroupBox("外观主题")
        theme_layout = QtWidgets.QVBoxLayout(theme_box)
        theme_layout.setSpacing(10)

        self._auto_btn = QtWidgets.QRadioButton("跟随 Windows（自动匹配系统强调色与深浅色）")
        self._light_btn = QtWidgets.QRadioButton("浅色模式")
        self._dark_btn = QtWidgets.QRadioButton("深色模式")

        # 根据当前模式选中
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

        # 说明文字
        hint = QtWidgets.QLabel("选择主题后将立即应用到整个界面。")
        hint.setStyleSheet(
            f"color:{theme.colors['on_surface_variant']}; font-size:9pt;"
        )
        layout.addWidget(hint)

        layout.addStretch(1)

        # 按钮行
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


# ============================================================
#  MainUi — 主界面
# ============================================================
class MainUi(QMainWindow):
    # 侧边栏宽度
    _SIDEBAR_EXPANDED = 210
    _SIDEBAR_COLLAPSED = 48

    def __init__(self):
        super().__init__()
        self.setWindowTitle("HopeKit 2.0.0-revived")
        self.setFixedSize(1200, 665)
        self._chat_win = None
        self._caidan_win = None
        self._calc_win = None
        self._shit_win = None
        self._copyright_win = None
        self._sidebar_collapsed = False
        self._build_ui()
        self._apply_style()

    def _build_ui(self):
        central = QtWidgets.QWidget(self)
        self.setCentralWidget(central)

        main_layout = QtWidgets.QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ============ 左侧可折叠菜单（分类导航）============
        self._sidebar = QtWidgets.QFrame(central)
        self._sidebar.setObjectName("sidebar")
        self._sidebar.setFixedWidth(self._SIDEBAR_EXPANDED)

        sidebar_layout = QtWidgets.QVBoxLayout(self._sidebar)
        sidebar_layout.setContentsMargins(8, 12, 8, 12)
        sidebar_layout.setSpacing(6)

        # 菜单标题
        self._sidebar_title = QtWidgets.QLabel("导航菜单")
        self._sidebar_title.setObjectName("sidebarTitle")
        self._sidebar_title.setAlignment(QtCore.Qt.AlignCenter)
        sidebar_layout.addWidget(self._sidebar_title)

        # 折叠按钮
        self._toggle_btn = QtWidgets.QPushButton("◀  折叠")
        self._toggle_btn.setObjectName("toggleBtn")
        self._toggle_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self._toggle_btn.clicked.connect(self._toggle_sidebar)
        sidebar_layout.addWidget(self._toggle_btn)

        # 分类导航容器（折叠时整体隐藏）
        self._nav_container = QtWidgets.QWidget(self._sidebar)
        nav_layout = QtWidgets.QVBoxLayout(self._nav_container)
        nav_layout.setContentsMargins(0, 6, 0, 0)
        nav_layout.setSpacing(6)

        # 分类项：(显示文本, 堆叠页索引)
        self._nav_buttons = []
        categories = [
            ("工具", 0),
            ("链接", 1),
            ("日历", 2),
        ]
        for text, page_idx in categories:
            btn = QtWidgets.QPushButton(text)
            btn.setObjectName("navBtn")
            btn.setCursor(QtCore.Qt.PointingHandCursor)
            btn.setCheckable(True)
            btn.clicked.connect(
                lambda _checked, idx=page_idx: self._switch_page(idx)
            )
            nav_layout.addWidget(btn)
            self._nav_buttons.append(btn)

        nav_layout.addStretch(1)
        sidebar_layout.addWidget(self._nav_container, 1)

        # 退出按钮
        self._exit_btn = QtWidgets.QPushButton("退出...")
        self._exit_btn.setObjectName("exitBtn")
        self._exit_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self._exit_btn.clicked.connect(self.close)
        sidebar_layout.addWidget(self._exit_btn)

        # 设置按钮（打开主题设置对话框）
        self._settings_btn = QtWidgets.QPushButton("设置")
        self._settings_btn.setObjectName("settingsBtn")
        self._settings_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self._settings_btn.clicked.connect(self._open_settings)
        sidebar_layout.addWidget(self._settings_btn)

        main_layout.addWidget(self._sidebar)

        # ============ 右侧主内容区 ============
        content = QtWidgets.QWidget(central)
        content_layout = QtWidgets.QVBoxLayout(content)
        content_layout.setContentsMargins(16, 16, 16, 16)
        content_layout.setSpacing(12)

        # 顶部：单个 logo + 标题 + 提示语（去掉重复 logo）
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
        title_lbl = QtWidgets.QLabel("HopeKit 2.0.0-revived")
        title_lbl.setStyleSheet("font-size:16pt; font-weight:600; color:#333;")
        tip = QtWidgets.QLabel(
            '<span style="font-size:18pt; color:#0000ff;">你今天看起来很聪明！</span>'
        )
        title_box.addWidget(title_lbl)
        title_box.addWidget(tip)
        header_layout.addLayout(title_box)
        header_layout.addStretch(1)
        content_layout.addLayout(header_layout)

        # 分类堆叠内容区：点击左侧分类切换右侧页面
        self._stack = QtWidgets.QStackedWidget()
        self._stack.addWidget(self._build_tools_page())
        self._stack.addWidget(self._build_links_page())
        self._stack.addWidget(self._build_calendar_page())
        content_layout.addWidget(self._stack, 1)

        main_layout.addWidget(content, 1)

        # 默认选中第一个分类
        self._switch_page(0)

        # ---- 状态栏 & 菜单栏 ----
        self.statusBar()
        menu_bar = QtWidgets.QMenuBar(self)
        self.setMenuBar(menu_bar)

    # ------------------------------------------------------------
    #  分类页面构建
    # ------------------------------------------------------------
    def _build_tools_page(self):
        """工具分类页：以网格按钮形式展示，点击打开对应 dialog"""
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setSpacing(12)

        title = QtWidgets.QLabel("工具")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        grid_box = QtWidgets.QGroupBox("可用工具")
        grid = QtWidgets.QGridLayout(grid_box)
        grid.setSpacing(10)

        # (文本, 行, 列, 处理函数)
        tools = [
            ("聊天室",            0, 0, self._open_chat),
            ("彩蛋",              0, 1, self._open_caidan),
            ("简易计算器",        1, 0, self._open_calc),
            ("探索系统屎山",      1, 1, self._open_shit),
            ("AI机器人（余额用尽）",   2, 0, None),
            ("查火车票（暂未开放）",   2, 1, None),
            ("牛逼の外部工具",    3, 0, None),
        ]
        for text, row, col, handler in tools:
            btn = QtWidgets.QPushButton(text)
            btn.setMinimumHeight(50)
            btn.setCursor(QtCore.Qt.PointingHandCursor)
            if handler:
                btn.clicked.connect(handler)
            else:
                btn.setEnabled(False)
            grid.addWidget(btn, row, col)

        layout.addWidget(grid_box)
        layout.addStretch(1)
        return page

    def _build_links_page(self):
        """链接分类页：开发者新闻列表，点击查看按钮打开对应内容"""
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setSpacing(12)

        title = QtWidgets.QLabel("链接")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        links_box = QtWidgets.QGroupBox("开发者新闻")
        links_layout = QtWidgets.QVBoxLayout(links_box)
        links_layout.setSpacing(10)

        links = [
            ("我们的网站",    self._open_website),
            ("版权声明",      self._open_copyright),
            ("加入QQ交流群",  self._open_qq_group),
            ("在线看亚运",    self._open_sports),
        ]
        for text, handler in links:
            row = QtWidgets.QHBoxLayout()
            lbl = QtWidgets.QLabel(
                f'<span style="font-size:14pt; font-weight:600;">{text}</span>'
            )
            btn = QtWidgets.QPushButton("查看")
            btn.setCursor(QtCore.Qt.PointingHandCursor)
            btn.clicked.connect(handler)
            row.addWidget(lbl)
            row.addStretch(1)
            row.addWidget(btn)
            links_layout.addLayout(row)
        layout.addWidget(links_box)

        contact_box = QtWidgets.QGroupBox("联系作者")
        contact_layout = QtWidgets.QVBoxLayout(contact_box)
        contact_layout.setSpacing(10)

        contacts = [
            ("哔哩哔哩",   self._open_bilibili),
            ("博客",       self._open_blog),
            ("GitHub",     self._open_github),
        ]
        for text, handler in contacts:
            row = QtWidgets.QHBoxLayout()
            lbl = QtWidgets.QLabel(
                f'<span style="font-size:14pt; font-weight:600;">{text}</span>'
            )
            btn = QtWidgets.QPushButton("查看")
            btn.setCursor(QtCore.Qt.PointingHandCursor)
            btn.clicked.connect(handler)
            row.addWidget(lbl)
            row.addStretch(1)
            row.addWidget(btn)
            contact_layout.addLayout(row)
        layout.addWidget(contact_box)

        layout.addStretch(1)
        return page

    def _build_calendar_page(self):
        """日历分类页"""
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setSpacing(12)

        title = QtWidgets.QLabel("日历")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        cal_box = QtWidgets.QGroupBox("日历")
        cal_layout = QtWidgets.QVBoxLayout(cal_box)
        cal_layout.addWidget(QtWidgets.QCalendarWidget())
        layout.addWidget(cal_box)
        layout.addStretch(1)
        return page

    def _switch_page(self, idx):
        """切换右侧堆叠页，并高亮当前选中的分类按钮"""
        self._stack.setCurrentIndex(idx)
        for i, btn in enumerate(self._nav_buttons):
            btn.setChecked(i == idx)

    def _toggle_sidebar(self):
        """折叠 / 展开左侧菜单"""
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

    def _open_settings(self):
        """打开设置对话框，切换主题后实时刷新界面"""
        dlg = SettingsDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            self._apply_style()
            # 同步刷新已打开的子窗口
            for win in (self._chat_win, self._caidan_win, self._calc_win,
                        self._shit_win, self._copyright_win):
                if win is not None:
                    try:
                        win.setStyleSheet("")
                        win.setStyleSheet(MainUi._global_stylestring())
                    except Exception:
                        pass

    @staticmethod
    def _global_stylestring():
        """供子窗口复用的全局样式表"""
        return styles.global_stylesheet(theme.colors)

    def _apply_style(self):
        # 全局样式表设置到 QApplication，让所有窗口（含子窗口）的按钮都圆角
        app = QtWidgets.QApplication.instance()
        if app is not None:
            app.setStyleSheet(self._global_stylestring())
        # 主窗口专属样式（侧边栏等）
        self.setStyleSheet(styles.main_stylesheet(theme.colors))

    def _open_chat(self):
        if self._chat_win is None:
            self._chat_win = MainWin()
            self._chat_win.setStyleSheet(MainUi._global_stylestring())
        self._chat_win.show()

    def _open_caidan(self):
        if self._caidan_win is None:
            self._caidan_win = CaidanWindow()
            self._caidan_win.setStyleSheet(MainUi._global_stylestring())
        self._caidan_win.show()

    def _open_calc(self):
        if self._calc_win is None:
            self._calc_win = Calculator()
            self._calc_win.setStyleSheet(MainUi._global_stylestring())
        self._calc_win.show()

    def _open_shit(self):
        if self._shit_win is None:
            self._shit_win = ShitWindow()
            self._shit_win.setStyleSheet(MainUi._global_stylestring())
        self._shit_win.show()

    def _open_copyright(self):
        if self._copyright_win is None:
            self._copyright_win = CopyrightWindow()
            self._copyright_win.setStyleSheet(MainUi._global_stylestring())
        self._copyright_win.show()

    @staticmethod
    def _open_website():
        QDesktopServices.openUrl(QUrl("https://hopestudio.top/"))

    @staticmethod
    def _open_qq_group():
        QDesktopServices.openUrl(QUrl(
            "http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=ZWK9Hjr85usU530C3rt0X_3a3ELG0o9e"
            "&authKey=g5Q5ELTce3ChemOo76dqWRxgCbJOHRJ6cRWiEJGFL95vR+JE4tyB2yqgTj5V22xf"
            "&noverify=0&group_code=876244203"
        ))

    @staticmethod
    def _open_sports():
        QDesktopServices.openUrl(QUrl("https://sports.cctv.com/"))

    @staticmethod
    def _open_bilibili():
        QDesktopServices.openUrl(QUrl("https://space.bilibili.com/1711131229"))

    @staticmethod
    def _open_blog():
        QDesktopServices.openUrl(QUrl("https://blog.nanoturtle.cn"))

    @staticmethod
    def _open_github():
        QDesktopServices.openUrl(QUrl("https://github.com/NanoTurtle1145"))


# ============================================================
#  入口
# ============================================================
if __name__ == "__main__":
    # 必须在 QApplication 创建前设置，否则 QtWebEngineWidgets 无法初始化
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication([])
    window = MainUi()
    window.show()
    sys.exit(app.exec_())