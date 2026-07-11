def global_stylesheet(colors):
    c = colors
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


def main_stylesheet(colors):
    c = colors
    return f"""
        QMainWindow {{
            background: {c['background']};
        }}

        /* ---- 侧边栏（MD3 Navigation Drawer 风格）---- */
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

        /* ---- 折叠按钮 ---- */
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

        /* ---- 导航按钮（MD3 NavigationBar item）---- */
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

        /* ---- 退出按钮（MD3 Error 风格）---- */
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

        /* ---- 设置按钮 ---- */
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

        /* ---- 页面标题 ---- */
        #pageTitle {{
            font-size: 22pt;
            font-weight: 400;
            color: {c['on_surface']};
            padding: 8px 0 4px 0;
        }}

        /* ---- 日历 ---- */
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

        /* ---- 菜单栏 ---- */
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

        /* ---- 滚动条（MD3 风格）---- */
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


def dialog_stylesheet(colors):
    c = colors
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

