"""
样式表模块 — 按主题风格返回对应 QSS

风格: md3 / md2 / windows
每个风格有三组样式:
  - global_stylesheet: 应用到 QApplication 级别的全局样式
  - main_stylesheet:  主窗口专属样式（侧边栏、导航、日历等）
  - dialog_stylesheet: 设置对话框样式
"""

from hopekit.theme import theme


# ============================================================
#  对外统一接口
# ============================================================
def global_stylesheet(colors):
    if theme.style == "md2":
        return _md2_global(colors)
    if theme.style == "windows":
        return _windows_global(colors)
    return _md3_global(colors)


def main_stylesheet(colors):
    if theme.style == "md2":
        return _md2_main(colors)
    if theme.style == "windows":
        return _windows_main(colors)
    return _md3_main(colors)


def dialog_stylesheet(colors):
    if theme.style == "md2":
        return _md2_dialog(colors)
    if theme.style == "windows":
        return _windows_dialog(colors)
    return _md3_dialog(colors)


# ============================================================
#  MD3 样式（原样式保留）
# ============================================================
def _md3_global(c):
    return f"""
        QWidget {{
            background: {c['background']};
            color: {c['on_background']};
        }}
        QGroupBox {{
            font-weight: 500;
            border: 1px solid {c['surface_variant']};
            border-radius: {c['card_radius']};
            margin-top: 14px;
            padding: 16px 14px 14px 14px;
            background: {c['surface']};
            color: {c['on_surface_variant']};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 16px; padding: 0 6px;
            color: {c['primary']}; font-weight: 600;
        }}
        QPushButton {{
            background: {c['primary']};
            color: {c['on_primary']};
            border: none;
            padding: 8px 18px;
            border-radius: {c['btn_radius']};
            font-weight: 500; min-height: 22px;
        }}
        QPushButton:hover {{
            background: {c['primary_container']};
            color: {c['on_primary_container']};
        }}
        QPushButton:disabled {{
            background: {c['surface_variant']};
            color: {c['outline']};
        }}
        QLineEdit, QTextEdit {{
            background: {c['surface']};
            color: {c['on_surface']};
            border: 1px solid {c['outline']};
            border-radius: {c['btn_radius']};
            padding: 8px 12px;
        }}
        QLineEdit:focus, QTextEdit:focus {{
            border: 2px solid {c['primary']};
            padding: 7px 11px;
        }}
        QLabel {{ background: transparent; color: {c['on_background']}; }}
        QStatusBar {{
            background: {c['surface']};
            color: {c['on_surface_variant']};
            border-top: 1px solid {c['surface_variant']};
        }}
    """


def _md3_main(c):
    return f"""
        QMainWindow {{
            background: {c['background']};
        }}

        #sidebar {{
            background: {c['sidebar_bg']};
            border: none;
            border-right: 1px solid {c['surface_variant']};
        }}
        #sidebarTitle {{
            color: {c['sidebar_text']};
            font-size: 11pt;
            font-weight: 600;
            padding: 6px 4px;
            letter-spacing: 1px;
        }}

        #toggleBtn {{
            background: {c['primary_container']};
            color: {c['on_primary_container']};
            border: none;
            padding: 10px 12px;
            border-radius: {c['nav_radius']};
            text-align: left;
            font-weight: 500;
        }}
        #toggleBtn:hover {{
            background: {c['sidebar_hover']};
        }}

        #navBtn {{
            background: transparent;
            color: {c['sidebar_text']};
            border: none;
            padding: 12px 16px;
            text-align: left;
            border-radius: {c['nav_radius']};
            font-size: 10pt;
            font-weight: 500;
        }}
        #navBtn:hover {{
            background: {c['sidebar_hover']};
        }}
        #navBtn:checked {{
            background: {c['sidebar_active']};
            color: {c['primary']};
            font-weight: 600;
        }}
        #navBtn:disabled {{
            color: {c['outline']};
        }}

        #exitBtn {{
            background: {c['exit_btn_bg']};
            color: {c['on_error']};
            border: none;
            padding: 12px;
            border-radius: {c['btn_radius']};
            font-weight: 600;
        }}
        #exitBtn:hover {{
            background: {c['exit_btn_hover']};
        }}

        #settingsBtn {{
            background: {c['secondary_container']};
            color: {c['on_secondary_container']};
            border: none;
            padding: 12px;
            border-radius: {c['btn_radius']};
            font-weight: 500;
        }}
        #settingsBtn:hover {{
            background: {c['sidebar_hover']};
        }}

        #pageTitle {{
            font-size: 22pt;
            font-weight: 400;
            color: {c['on_surface']};
            padding: 8px 0 4px 0;
        }}

        QCalendarWidget {{
            background: {c['surface']};
            color: {c['on_surface']};
            border: none;
        }}
        QCalendarWidget QToolButton {{
            color: {c['on_surface']};
            background: transparent;
            border: none;
            border-radius: {c['btn_radius']};
            padding: 4px 8px;
        }}
        QCalendarWidget QToolButton:hover {{
            background: {c['secondary_container']};
        }}
        QCalendarWidget QMenu {{
            background: {c['surface']};
            color: {c['on_surface']};
            border: 1px solid {c['surface_variant']};
        }}
        QCalendarWidget QAbstractItemView {{
            background: {c['surface']};
            color: {c['on_surface']};
            selection-background-color: {c['primary']};
            selection-color: {c['on_primary']};
            border: none;
        }}

        QMenuBar {{
            background: {c['surface']};
            color: {c['on_surface']};
            border-bottom: 1px solid {c['surface_variant']};
            padding: 2px;
        }}
        QMenuBar::item {{
            background: transparent;
            padding: 6px 12px;
            border-radius: {c['btn_radius']};
        }}
        QMenuBar::item:selected {{
            background: {c['secondary_container']};
        }}

        QScrollBar:vertical {{
            background: transparent;
            width: 10px;
            margin: 0;
        }}
        QScrollBar::handle:vertical {{
            background: {c['outline']};
            border-radius: 5px;
            min-height: 30px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {c['on_surface_variant']};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
        }}
    """


def _md3_dialog(c):
    return f"""
        QDialog {{
            background: {c['background']};
        }}
        QGroupBox {{
            font-weight: 500;
            border: 1px solid {c['surface_variant']};
            border-radius: {c['card_radius']};
            margin-top: 14px;
            padding: 16px 14px 14px 14px;
            background: {c['surface']};
            color: {c['on_surface_variant']};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 16px; padding: 0 6px;
            color: {c['primary']}; font-weight: 600;
        }}
        QRadioButton {{
            color: {c['on_surface']};
            spacing: 8px;
            padding: 6px 0;
            background: transparent;
        }}
        QRadioButton::indicator {{
            width: 18px; height: 18px;
            border-radius: 9px;
            border: 2px solid {c['outline']};
            background: transparent;
        }}
        QRadioButton::indicator:checked {{
            border: 2px solid {c['primary']};
            background: {c['primary']};
        }}
        QPushButton {{
            background: {c['primary']};
            color: {c['on_primary']};
            border: none;
            padding: 8px 24px;
            border-radius: {c['btn_radius']};
            font-weight: 500;
            min-width: 70px;
        }}
        QPushButton:hover {{
            background: {c['primary_container']};
            color: {c['on_primary_container']};
        }}
        QLabel {{ background: transparent; color: {c['on_background']}; }}
    """


# ============================================================
#  MD2 样式（Material Design 2 风格）
#  - 4px 圆角
#  - 扁平化按钮
#  - 阴影质感（用边框模拟 elevation）
#  - 强调色区分选中态
# ============================================================
def _md2_global(c):
    return f"""
        QWidget {{
            background: {c['background']};
            color: {c['on_background']};
        }}
        QGroupBox {{
            font-weight: 500;
            border: 1px solid {c['surface_variant']};
            border-radius: {c['card_radius']};
            margin-top: 14px;
            padding: 16px 14px 14px 14px;
            background: {c['surface']};
            color: {c['on_surface_variant']};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 16px; padding: 0 6px;
            color: {c['primary']}; font-weight: 600;
        }}
        QPushButton {{
            background: {c['primary']};
            color: {c['on_primary']};
            border: none;
            border-bottom: 2px solid {c['primary_dark'] if 'primary_dark' in c else c['primary']};
            padding: 8px 18px;
            border-radius: {c['btn_radius']};
            font-weight: 500;
            min-height: 22px;
            text-transform: uppercase;
        }}
        QPushButton:hover {{
            background: {c['primary_light'] if 'primary_light' in c else c['primary_container']};
        }}
        QPushButton:pressed {{
            border-bottom: 1px solid {c['primary_dark'] if 'primary_dark' in c else c['primary']};
            padding-top: 9px;
        }}
        QPushButton:disabled {{
            background: {c['surface_variant']};
            color: {c['outline']};
            border-bottom: 2px solid {c['outline']};
        }}
        QLineEdit, QTextEdit {{
            background: transparent;
            color: {c['on_surface']};
            border: none;
            border-bottom: 1px solid {c['outline']};
            border-radius: {c['btn_radius']};
            padding: 8px 4px;
        }}
        QLineEdit:focus, QTextEdit:focus {{
            border-bottom: 2px solid {c['primary']};
            padding-bottom: 7px;
        }}
        QLabel {{ background: transparent; color: {c['on_background']}; }}
        QStatusBar {{
            background: {c['surface']};
            color: {c['on_surface_variant']};
            border-top: 1px solid {c['surface_variant']};
        }}
    """


def _md2_main(c):
    return f"""
        QMainWindow {{
            background: {c['background']};
        }}

        #sidebar {{
            background: {c['sidebar_bg']};
            border: none;
            border-right: 1px solid {c['outline']};
        }}
        #sidebarTitle {{
            color: {c['sidebar_text']};
            font-size: 11pt;
            font-weight: 600;
            padding: 6px 4px;
            letter-spacing: 1px;
        }}

        #toggleBtn {{
            background: {c['primary']};
            color: {c['on_primary']};
            border: none;
            border-bottom: 2px solid {c['primary_dark'] if 'primary_dark' in c else c['primary']};
            padding: 10px 12px;
            border-radius: {c['nav_radius']};
            text-align: left;
            font-weight: 500;
        }}
        #toggleBtn:hover {{
            background: {c['primary_light'] if 'primary_light' in c else c['primary_container']};
        }}

        #navBtn {{
            background: transparent;
            color: {c['sidebar_text']};
            border: none;
            padding: 12px 16px;
            text-align: left;
            border-radius: {c['nav_radius']};
            font-size: 10pt;
            font-weight: 500;
        }}
        #navBtn:hover {{
            background: {c['sidebar_hover']};
        }}
        #navBtn:checked {{
            background: {c['sidebar_active']};
            color: {c['primary']};
            font-weight: 600;
            border-left: 3px solid {c['primary']};
            padding-left: 13px;
        }}
        #navBtn:disabled {{
            color: {c['outline']};
        }}

        #exitBtn {{
            background: {c['exit_btn_bg']};
            color: {c['on_error']};
            border: none;
            padding: 12px;
            border-radius: {c['btn_radius']};
            font-weight: 600;
        }}
        #exitBtn:hover {{
            background: {c['exit_btn_hover']};
        }}

        #settingsBtn {{
            background: {c['surface_variant']};
            color: {c['on_surface']};
            border: none;
            padding: 12px;
            border-radius: {c['btn_radius']};
            font-weight: 500;
        }}
        #settingsBtn:hover {{
            background: {c['sidebar_hover']};
        }}

        #pageTitle {{
            font-size: 20pt;
            font-weight: 400;
            color: {c['on_surface']};
            padding: 8px 0 4px 0;
        }}

        QCalendarWidget {{
            background: {c['surface']};
            color: {c['on_surface']};
            border: none;
        }}
        QCalendarWidget QToolButton {{
            color: {c['on_surface']};
            background: transparent;
            border: none;
            border-radius: {c['btn_radius']};
            padding: 4px 8px;
        }}
        QCalendarWidget QToolButton:hover {{
            background: {c['primary_light'] if 'primary_light' in c else c['primary_container']};
        }}
        QCalendarWidget QMenu {{
            background: {c['surface']};
            color: {c['on_surface']};
            border: 1px solid {c['surface_variant']};
        }}
        QCalendarWidget QAbstractItemView {{
            background: {c['surface']};
            color: {c['on_surface']};
            selection-background-color: {c['primary']};
            selection-color: {c['on_primary']};
            border: none;
        }}

        QMenuBar {{
            background: {c['primary']};
            color: {c['on_primary']};
            padding: 2px;
            border: none;
        }}
        QMenuBar::item {{
            background: transparent;
            padding: 6px 12px;
            border-radius: {c['btn_radius']};
        }}
        QMenuBar::item:selected {{
            background: {c['primary_light'] if 'primary_light' in c else c['primary_container']};
        }}

        QScrollBar:vertical {{
            background: transparent;
            width: 8px;
            margin: 0;
        }}
        QScrollBar::handle:vertical {{
            background: {c['outline']};
            border-radius: 4px;
            min-height: 30px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {c['on_surface_variant']};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
        }}
    """


def _md2_dialog(c):
    return f"""
        QDialog {{
            background: {c['background']};
        }}
        QGroupBox {{
            font-weight: 500;
            border: 1px solid {c['surface_variant']};
            border-radius: {c['card_radius']};
            margin-top: 14px;
            padding: 16px 14px 14px 14px;
            background: {c['surface']};
            color: {c['on_surface_variant']};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 16px; padding: 0 6px;
            color: {c['primary']}; font-weight: 600;
        }}
        QRadioButton {{
            color: {c['on_surface']};
            spacing: 8px;
            padding: 6px 0;
            background: transparent;
        }}
        QRadioButton::indicator {{
            width: 18px; height: 18px;
            border-radius: 9px;
            border: 2px solid {c['outline']};
            background: transparent;
        }}
        QRadioButton::indicator:checked {{
            border: 2px solid {c['primary']};
            background: {c['primary']};
        }}
        QPushButton {{
            background: {c['primary']};
            color: {c['on_primary']};
            border: none;
            border-bottom: 2px solid {c['primary_dark'] if 'primary_dark' in c else c['primary']};
            padding: 8px 24px;
            border-radius: {c['btn_radius']};
            font-weight: 500;
            min-width: 70px;
            text-transform: uppercase;
        }}
        QPushButton:hover {{
            background: {c['primary_light'] if 'primary_light' in c else c['primary_container']};
        }}
        QLabel {{ background: transparent; color: {c['on_background']}; }}
    """


# ============================================================
#  Windows 原生风格样式
#  - 零样式覆盖，尽量让 Qt 原生控件显示系统外观
#  - 只统一：背景色、文字色、侧边栏风格
#  - 按钮、输入框等完全交给系统绘制
# ============================================================
def _windows_global(c):
    return f"""
        QWidget {{
            background: {c['background']};
            color: {c['on_background']};
        }}
        QLabel {{ background: transparent; color: {c['on_background']}; }}
        QStatusBar {{
            background: {c['surface']};
            color: {c['on_surface_variant']};
        }}
        QGroupBox {{
            border: 1px solid {c['outline']};
            border-radius: {c['card_radius']};
            margin-top: 14px;
            padding: 12px;
            background: {c['surface']};
            color: {c['on_surface_variant']};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 4px;
            color: {c['on_surface_variant']};
            font-weight: 500;
        }}
    """


def _windows_main(c):
    return f"""
        QMainWindow {{
            background: {c['background']};
        }}

        #sidebar {{
            background: {c['sidebar_bg']};
            border: none;
            border-right: 1px solid {c['outline']};
        }}
        #sidebarTitle {{
            color: {c['sidebar_text']};
            font-size: 11pt;
            font-weight: 600;
            padding: 6px 4px;
            letter-spacing: 1px;
        }}

        #toggleBtn {{
            background: {c['primary']};
            color: {c['on_primary']};
            border: 1px solid {c['outline']};
            padding: 8px 12px;
            border-radius: {c['nav_radius']};
            text-align: left;
            font-weight: 500;
        }}
        #toggleBtn:hover {{
            background: {c['sidebar_hover']};
        }}

        #navBtn {{
            background: transparent;
            color: {c['sidebar_text']};
            border: none;
            padding: 10px 16px;
            text-align: left;
            border-radius: {c['nav_radius']};
            font-size: 10pt;
            font-weight: 500;
        }}
        #navBtn:hover {{
            background: {c['sidebar_hover']};
        }}
        #navBtn:checked {{
            background: {c['sidebar_active']};
            color: {c['on_surface']};
            font-weight: 600;
            border-left: 3px solid {c['primary']};
            padding-left: 13px;
        }}
        #navBtn:disabled {{
            color: {c['outline']};
        }}

        #exitBtn {{
            background: {c['exit_btn_bg']};
            color: {c['on_error']};
            border: 1px solid {c['outline']};
            padding: 10px;
            border-radius: {c['btn_radius']};
            font-weight: 600;
        }}
        #exitBtn:hover {{
            background: {c['exit_btn_hover']};
        }}

        #settingsBtn {{
            background: {c['surface_variant']};
            color: {c['on_surface']};
            border: 1px solid {c['outline']};
            padding: 10px;
            border-radius: {c['btn_radius']};
            font-weight: 500;
        }}
        #settingsBtn:hover {{
            background: {c['sidebar_hover']};
        }}

        #pageTitle {{
            font-size: 18pt;
            font-weight: 600;
            color: {c['on_surface']};
            padding: 8px 0 4px 0;
        }}

        QCalendarWidget {{
            background: {c['surface']};
            color: {c['on_surface']};
        }}
        QCalendarWidget QToolButton {{
            color: {c['on_surface']};
        }}
        QCalendarWidget QAbstractItemView {{
            background: {c['surface']};
            color: {c['on_surface']};
            selection-background-color: {c['primary']};
            selection-color: {c['on_primary']};
        }}

        QScrollBar:vertical {{
            width: 12px;
        }}
    """


def _windows_dialog(c):
    return f"""
        QDialog {{
            background: {c['background']};
        }}
        QGroupBox {{
            border: 1px solid {c['outline']};
            border-radius: {c['card_radius']};
            margin-top: 14px;
            padding: 12px;
            background: {c['surface']};
            color: {c['on_surface_variant']};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 4px;
            color: {c['on_surface_variant']};
            font-weight: 500;
        }}
        QRadioButton {{
            color: {c['on_surface']};
            spacing: 8px;
            padding: 6px 0;
            background: transparent;
        }}
        QLabel {{ background: transparent; color: {c['on_background']}; }}
    """
