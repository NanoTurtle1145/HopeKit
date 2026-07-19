"""
样式表模块 — 按主题风格返回对应 QSS

风格: md3 / md2 / qt / winui3 / gnome / kde / cupertino / chromeos
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
    s = theme.style
    if s == "md2":       return _md2_global(colors)
    if s == "qt":        return _qt_global(colors)
    if s == "winui3":    return _winui3_global(colors)
    if s == "win10fluent": return _win10fluent_global(colors)
    if s == "gnome":     return _gnome_global(colors)
    if s == "kde":       return _kde_global(colors)
    if s == "cupertino": return _cupertino_global(colors)
    if s == "chromeos":  return _chromeos_global(colors)
    return _md3_global(colors)


def main_stylesheet(colors):
    s = theme.style
    if s == "md2":       return _md2_main(colors)
    if s == "qt":        return _qt_main(colors)
    if s == "winui3":    return _winui3_main(colors)
    if s == "win10fluent": return _win10fluent_main(colors)
    if s == "gnome":     return _gnome_main(colors)
    if s == "kde":       return _kde_main(colors)
    if s == "cupertino": return _cupertino_main(colors)
    if s == "chromeos":  return _chromeos_main(colors)
    return _md3_main(colors)


def dialog_stylesheet(colors):
    s = theme.style
    if s == "md2":       return _md2_dialog(colors)
    if s == "qt":        return _qt_dialog(colors)
    if s == "winui3":    return _winui3_dialog(colors)
    if s == "win10fluent": return _win10fluent_dialog(colors)
    if s == "gnome":     return _gnome_dialog(colors)
    if s == "kde":       return _kde_dialog(colors)
    if s == "cupertino": return _cupertino_dialog(colors)
    if s == "chromeos":  return _chromeos_dialog(colors)
    return _md3_dialog(colors)


def main_host_stylesheet(colors):
    """
    Web UI 宿主主窗口的极简 QSS。
    主界面由 QWebEngineView 渲染（HTML/CSS/JS），这里仅做：
    - QMainWindow 透明（让 DWM 材质透出）
    - #webUIHost 容器透明
    - QMenuBar 极简（保留菜单条但视觉上不抢戏）
    - QStatusBar 同步配色
    """
    bg = colors.get('background', '#FFFFFF')
    surface = colors.get('surface', '#F5F5F7')
    on_surface = colors.get('on_surface', '#1D1D1F')
    outline = colors.get('outline_variant', '#E5E5EA')

    # 透明主题（winui3 / win10fluent）：背景透明让 DWM 材质透出
    transparent = theme.style in ("winui3", "win10fluent")
    host_bg = "transparent" if transparent else bg

    return f"""
        QMainWindow {{
            background: {host_bg};
        }}
        #webUIHost {{
            background: transparent;
            border: none;
        }}
        QWebEngineView {{
            background: transparent;
            border: none;
        }}
        QMenuBar {{
            background: transparent;
            color: {on_surface};
            border: none;
            border-bottom: 1px solid {outline};
            padding: 2px 6px;
            font-size: 13px;
        }}
        QMenuBar::item {{
            background: transparent;
            padding: 4px 10px;
            border-radius: 4px;
        }}
        QMenuBar::item:selected {{
            background: {colors.get('sidebar_hover', 'rgba(0,0,0,0.05)')};
        }}
        QStatusBar {{
            background: {host_bg};
            color: {colors.get('on_surface_variant', '#6D6D72')};
            border: none;
            border-top: 1px solid {outline};
            font-size: 12px;
            padding: 2px 8px;
        }}
    """


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

        /* ---- Navigation Drawer ---- */
        #sidebar {{
            background: {c['sidebar_bg']};
            border: none;
            border-right: 1px solid {c['outline_variant']};
        }}
        #sidebarTitle {{
            color: {c['on_surface_variant']};
            font-size: 18pt;
            font-weight: 400;
        }}
        #toggleBtn {{
            background: transparent;
            border: none;
            border-radius: 16px;
            font-size: 14pt;
        }}
        #toggleBtn:hover {{
            background: {c['secondary_container']};
        }}
        #navScroll {{
            background: transparent;
            border: none;
        }}
        /* 分类组标题 */
        #navGroupHeader {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 12px 16px 6px 16px;
            text-align: left;
            font-size: 12pt;
            font-weight: 600;
        }}
        /* 导航项（MD3: 选中=primary-container, 未选中=on-surface-variant） */
        #navBtn {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 12px 16px;
            text-align: left;
            border-radius: 28px;
            font-size: 10pt;
            font-weight: 500;
        }}
        #navBtn:hover {{
            background: {c['secondary_container']};
        }}
        #navBtn:checked {{
            background: {c['primary_container']};
            color: {c['on_primary_container']};
            font-weight: 600;
        }}
        #navBtn:disabled {{
            color: {c['outline']};
        }}
        /* 组间分割线（MD3: outline-variant） */
        #navDivider {{
            background: {c['outline_variant']};
            margin: 4px 16px;
            border: none;
        }}
        #exitBtn {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 12px 16px;
            text-align: left;
            border-radius: 28px;
            font-size: 10pt;
            font-weight: 500;
        }}
        #exitBtn:hover {{
            background: {c['error']};
            color: {c['on_error']};
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

        /* ---- 二级菜单（设置页面子导航）---- */
        #subNav {{
            background: {c['surface']};
            border: none;
            border-right: 1px solid {c['surface_variant']};
        }}
        #subNavTitle {{
            color: {c['on_surface']};
            font-size: 11pt;
            font-weight: 600;
            padding: 6px 4px;
            letter-spacing: 1px;
        }}
        #subNavBtn {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 10px 14px;
            text-align: left;
            border-radius: {c['nav_radius']};
            font-size: 10pt;
            font-weight: 500;
        }}
        #subNavBtn:hover {{
            background: {c['secondary_container']};
        }}
        #subNavBtn:checked {{
            background: {c['secondary_container']};
            color: {c['primary']};
            font-weight: 600;
        }}

        /* ---- 右下角导入 FAB 按钮（MD3 FAB, 16dp radius, primary-container 背景）---- */
        #importFab {{
            background-color: {c['primary_container']};
            color: {c['on_primary_container']};
            border: none;
            border-radius: 16px;
            font-size: 20pt;
            font-weight: 400;
            min-width: 56px;
            min-height: 56px;
            padding: 0;
        }}
        #importFab:hover {{
            background-color: {c['primary']};
            color: {c['on_primary']};
        }}

        /* ---- 模块卡片（基于 animation-vocabulary）---- */
        #moduleCard {{
            background: {c['surface']};
            border: 1px solid {c['outline']};
            border-radius: {c['card_radius']};
            margin-bottom: 8px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            transition: box-shadow 200ms ease-out, border-color 200ms ease-out, transform 150ms ease-out;
        }}
        #moduleCard:hover {{
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
            border-color: {c['primary']};
        }}
        #moduleCard:pressed {{
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            transform: scale(0.98);
        }}

        /* ---- Toggle Switch（基于 animation-vocabulary）---- */
        #toggleSwitch {{
            background: {c['outline']};
            border: none;
            border-radius: 12px;
            min-width: 44px;
            min-height: 24px;
            padding: 0;
            margin: 0;
            transition: background 200ms ease-out;
        }}
        #toggleSwitch:checked {{
            background: {c['primary']};
        }}
        #toggleSwitch::indicator {{
            width: 20px;
            height: 20px;
            background: white;
            border-radius: 10px;
            margin: 2px;
            transition: margin-left 200ms ease-out;
        }}
        #toggleSwitch:checked::indicator {{
            margin-left: 22px;
        }}

        /* ---- 查看按钮 ---- */
        #viewBtn {{
            background: {c['primary']};
            color: {c['on_primary']};
            border: none;
            border-radius: {c['btn_radius']};
            padding: 4px 12px;
            font-size: 9pt;
            font-weight: 500;
            transition: background 200ms ease-out, transform 100ms ease-out;
        }}
        #viewBtn:hover {{
            background: {c['primary_container']};
            color: {c['on_primary_container']};
        }}
        #viewBtn:pressed {{
            transform: scale(0.95);
        }}
        #viewBtn:disabled {{
            background: {c['surface_variant']};
            color: {c['outline']};
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
#  MD2 样式（Material Design 2 — 严格遵循 2014 Google 规范）
#  - 全局 4dp 圆角
#  - Card: elevation 2dp (rest) → 8dp (hover)，用边框+背景色模拟
#  - RaisedButton: primary 填充，hover 变 primary_dark
#  - 输入框: 下划线式（MD2 TextField 标准）
#  - AppBar: primary 色背景
#  - Drawer: 侧边栏 Grey 100 背景
#  - ❗ 不用 MD3 的 tonal palette / container 术语
# ============================================================
def _md2_global(c):
    pd = c.get('primary_dark', c['primary'])
    pl = c.get('primary_light', c['primary_container'])
    return f"""
        QWidget {{
            background: {c['background']};
            color: {c['on_background']};
        }}
        /* MD2 Card: elevation=2dp，用 1px border 模拟阴影 */
        QGroupBox {{
            font-weight: 500;
            border: 1px solid {c['divider']};
            border-radius: {c['card_radius']};
            margin-top: 14px;
            padding: 16px 14px 14px 14px;
            background: {c['surface']};
            color: {c['on_surface']};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 16px; padding: 0 6px;
            color: {c['primary']}; font-weight: 600;
        }}
        /* MD2 RaisedButton: primary 填充, hover→primary_dark */
        QPushButton {{
            background-color: {c['primary']};
            color: {c['on_primary']};
            border: none;
            padding: 8px 18px;
            border-radius: {c['btn_radius']};
            font-weight: 500;
            min-height: 22px;
        }}
        QPushButton:hover {{
            background-color: {pd};
        }}
        QPushButton:pressed {{
            background-color: {pd};
        }}
        QPushButton:disabled {{
            background-color: {c['surface_variant']};
            color: {c['outline']};
        }}
        /* MD2 TextField: 下划线式 */
        QLineEdit, QTextEdit {{
            background-color: transparent;
            color: {c['on_surface']};
            border: none;
            border-bottom: 1px solid {c['outline']};
            border-radius: 0px;
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
            border-top: 1px solid {c['divider']};
        }}
    """


def _md2_main(c):
    pd = c.get('primary_dark', c['primary'])
    pl = c.get('primary_light', c['primary_container'])
    return f"""
        QMainWindow {{
            background: {c['background']};
        }}

        /* ---- Navigation Drawer (MD2) ---- */
        #sidebar {{
            background: {c['sidebar_bg']};
            border: none;
            border-right: 1px solid {c['outline_variant']};
        }}
        #sidebarTitle {{
            color: {c['sidebar_text']};
            font-size: 18pt;
            font-weight: 400;
        }}
        #toggleBtn {{
            background: transparent;
            border: none;
            border-radius: {c['nav_radius']};
            font-size: 14pt;
        }}
        #toggleBtn:hover {{
            background: {c['sidebar_hover']};
        }}
        #navScroll {{
            background: transparent;
            border: none;
        }}
        /* 分类组标题 */
        #navGroupHeader {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 12px 16px 6px 16px;
            text-align: left;
            font-size: 12pt;
            font-weight: 600;
        }}
        /* 导航项（MD2: 选中=primary_light, 未选中=text-secondary） */
        #navBtn {{
            background: transparent;
            color: {c['on_surface_variant']};
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
            background: {pl};
            color: {c['primary']};
            font-weight: 600;
        }}
        #navBtn:disabled {{
            color: {c['outline']};
        }}
        /* 组间分割线 */
        #navDivider {{
            background: {c['outline_variant']};
            margin: 4px 16px;
            border: none;
        }}
        #exitBtn {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 12px 16px;
            text-align: left;
            border-radius: {c['nav_radius']};
            font-size: 10pt;
            font-weight: 500;
        }}
        #exitBtn:hover {{
            background: {c['exit_btn_bg']};
            color: {c['on_error']};
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
            background-color: {pl};
        }}
        QCalendarWidget QMenu {{
            background: {c['surface']};
            color: {c['on_surface']};
            border: 1px solid {c['divider']};
        }}
        QCalendarWidget QAbstractItemView {{
            background: {c['surface']};
            color: {c['on_surface']};
            selection-background-color: {c['primary']};
            selection-color: {c['on_primary']};
            border: none;
        }}

        /* MD2 AppBar: primary 色背景 */
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
            background-color: {pd};
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

        /* ---- 二级菜单（设置页面子导航）---- */
        #subNav {{
            background: {c['surface']};
            border: none;
            border-right: 1px solid {c['divider']};
        }}
        #subNavTitle {{
            color: {c['on_surface']};
            font-size: 11pt;
            font-weight: 600;
            padding: 6px 4px;
            letter-spacing: 1px;
        }}
        #subNavBtn {{
            background-color: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 10px 14px;
            text-align: left;
            border-radius: {c['nav_radius']};
            font-size: 10pt;
            font-weight: 500;
        }}
        #subNavBtn:hover {{
            background-color: {c['sidebar_hover']};
        }}
        #subNavBtn:checked {{
            background-color: {c['primary_light']};
            color: {c['primary']};
            font-weight: 600;
        }}

        /* ---- 右下角导入 FAB 按钮（MD2 FAB: accent 色, 56dp 圆形, elevation=6dp）---- */
        #importFab {{
            background-color: {c['accent']};
            color: {c['on_accent']};
            border: none;
            border-radius: 28px;
            font-size: 24pt;
            font-weight: 300;
            min-width: 56px;
            min-height: 56px;
            padding: 0;
        }}
        #importFab:hover {{
            background-color: {c['accent_dark']};
        }}
        #importFab:pressed {{
            transform: scale(0.95);
        }}

        /* ---- 模块卡片（基于 animation-vocabulary）---- */
        #moduleCard {{
            background: {c['surface']};
            border: 1px solid {c['divider']};
            border-radius: {c['card_radius']};
            margin-bottom: 8px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
            transition: box-shadow 200ms ease-out, border-color 200ms ease-out, transform 150ms ease-out;
        }}
        #moduleCard:hover {{
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
            border-color: {c['primary']};
        }}
        #moduleCard:pressed {{
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
            transform: scale(0.98);
        }}

        /* ---- Toggle Switch（基于 animation-vocabulary）---- */
        #toggleSwitch {{
            background: {c['outline']};
            border: none;
            border-radius: 12px;
            min-width: 44px;
            min-height: 24px;
            padding: 0;
            margin: 0;
            transition: background 200ms ease-out;
        }}
        #toggleSwitch:checked {{
            background: {c['primary']};
        }}
        #toggleSwitch::indicator {{
            width: 20px;
            height: 20px;
            background: white;
            border-radius: 10px;
            margin: 2px;
            transition: margin-left 200ms ease-out;
        }}
        #toggleSwitch:checked::indicator {{
            margin-left: 22px;
        }}

        /* ---- 查看按钮 ---- */
        #viewBtn {{
            background: {c['primary']};
            color: {c['on_primary']};
            border: none;
            border-radius: {c['btn_radius']};
            padding: 4px 12px;
            font-size: 9pt;
            font-weight: 500;
            transition: background 200ms ease-out, transform 100ms ease-out;
        }}
        #viewBtn:hover {{
            background: {c['primary_dark']};
        }}
        #viewBtn:pressed {{
            transform: scale(0.95);
        }}
        #viewBtn:disabled {{
            background: {c['surface_variant']};
            color: {c['outline']};
        }}
    """


def _md2_dialog(c):
    pd = c.get('primary_dark', c['primary'])
    pl = c.get('primary_light', c['primary_container'])
    return f"""
        QDialog {{
            background: {c['background']};
        }}
        QGroupBox {{
            font-weight: 500;
            border: 1px solid {c['divider']};
            border-radius: {c['card_radius']};
            margin-top: 14px;
            padding: 16px 14px 14px 14px;
            background: {c['surface']};
            color: {c['on_surface']};
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
            background-color: {c['primary']};
            color: {c['on_primary']};
            border: none;
            padding: 8px 24px;
            border-radius: {c['btn_radius']};
            font-weight: 500;
            min-width: 70px;
        }}
        QPushButton:hover {{
            background-color: {pd};
        }}
        QLabel {{ background: transparent; color: {c['on_background']}; }}
    """


# ============================================================
#  Qt 原生风格样式
#  - 几乎不写样式表，完全使用 Qt 默认控件外观
#  - 仅为侧边栏、退出按钮等结构性自定义组件提供最小样式
#  - 普通 QPushButton / QLineEdit / QGroupBox 等完全交给 Qt 原生绘制
# ============================================================
def _qt_global(c):
    return ""


def _qt_main(c):
    return f"""
        #sidebar {{
            background: {c['sidebar_bg']};
            border-right: 1px solid {c['outline']};
        }}
        #sidebarTitle {{
            color: {c['sidebar_text']};
            font-size: 18pt;
            font-weight: 400;
        }}
        #toggleBtn {{
            border: none;
            font-size: 14pt;
        }}
        #navScroll {{
            background: transparent;
            border: none;
        }}
        #navGroupHeader {{
            border: none;
            padding: 12px 16px 6px 16px;
            text-align: left;
            font-size: 12pt;
            font-weight: 600;
        }}
        #navBtn {{
            color: {c['sidebar_text']};
            border: none;
            padding: 10px 16px;
            text-align: left;
            font-size: 10pt;
        }}
        #navBtn:hover {{
            background: {c['sidebar_hover']};
        }}
        #navBtn:checked {{
            background: {c['sidebar_active']};
            font-weight: 600;
            border-left: 3px solid {c['primary']};
            padding-left: 13px;
        }}
        #navDivider {{
            background: {c['outline_variant']};
            margin: 4px 16px;
            border: none;
        }}
        #exitBtn {{
            color: {c['sidebar_text']};
            border: none;
            padding: 10px 16px;
            text-align: left;
            font-size: 10pt;
        }}
        #exitBtn:hover {{
            background: {c['exit_btn_bg']};
            color: {c['on_error']};
        }}

        #pageTitle {{
            font-size: 18pt;
            font-weight: 600;
            padding: 8px 0 4px 0;
        }}

        #subNav {{
            border-right: 1px solid {c['outline']};
        }}
        #subNavTitle {{
            font-size: 11pt;
            font-weight: 600;
            padding: 6px 4px;
        }}
        #subNavBtn {{
            border: none;
            padding: 10px 14px;
            text-align: left;
            font-size: 10pt;
        }}
        #subNavBtn:hover {{
            background: {c['sidebar_hover']};
        }}
        #subNavBtn:checked {{
            background: {c['sidebar_active']};
            font-weight: 600;
            border-left: 3px solid {c['primary']};
            padding-left: 11px;
        }}
    """


def _qt_dialog(c):
    return ""


# ============================================================
#  WinUI3 / Fluent Design 样式
#  - Segoe UI Variable 字体
#  - 分层圆角：控件 4dp / 卡片 8dp / 导航 8dp
#  - 选中态 = 半透明强调色 (AccentFillColorSecondary)
#  - Hover = 极淡强调色 (ControlFillColorSecondary)
#  - 卡片/按钮有细微边框 (CardStrokeDefault)
#  - NavigationView: 左0dp右16dp（QSS 限制用 8dp 近似）
# ============================================================
def _winui3_global(c):
    return f"""
        QWidget {{
            color: {c['on_background']};
            font-family: "Segoe UI Variable", "Segoe UI", sans-serif;
        }}
        QGroupBox {{
            font-weight: 500;
            border: 1px solid {c['outline']};
            border-radius: {c['card_radius']};
            margin-top: 14px;
            padding: 16px 14px 14px 14px;
            background: rgba(255, 255, 255, 0.70);
            color: {c['on_surface_variant']};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 16px; padding: 0 6px;
            color: {c['primary']}; font-weight: 600;
        }}
        QPushButton {{
            background: {c['surface']};
            color: {c['on_surface']};
            border: 1px solid {c['outline']};
            padding: 8px 18px;
            border-radius: {c['btn_radius']};
            font-weight: 500;
            min-height: 22px;
        }}
        QPushButton:hover {{
            background: {c['secondary_container']};
            border-color: {c['primary']};
        }}
        QPushButton:pressed {{
            background: {c['primary_container']};
        }}
        QPushButton:disabled {{
            background: {c['surface_variant']};
            color: {c['outline']};
            border-color: {c['outline']};
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
            border-top: 1px solid {c['outline']};
        }}
    """


def _winui3_main(c):
    return f"""
        /* ---- NavigationView (WinUI3) ---- */
        #sidebar {{
            background: rgba(243, 243, 243, 0.30);
            border: none;
            border-right: 1px solid {c['outline']};
        }}
        #sidebarTitle {{
            color: {c['on_surface']};
            font-size: 18pt;
            font-weight: 400;
        }}
        #toggleBtn {{
            background: transparent;
            border: none;
            border-radius: {c['btn_radius']};
            font-size: 14pt;
        }}
        #toggleBtn:hover {{
            background: {c['secondary_container']};
        }}
        #navScroll {{
            background: transparent;
            border: none;
        }}
        #navScroll > QWidget {{
            background: transparent;
        }}
        #navContainer {{
            background: transparent;
        }}
        /* 分类组标题 */
        #navGroupHeader {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 12px 16px 6px 16px;
            text-align: left;
            font-size: 12pt;
            font-weight: 600;
        }}
        /* 导航项 (WinUI3: 选中=AccentFillColorSecondary 60%透, 文字=on-accent) */
        #navBtn {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 10px 16px;
            text-align: left;
            border-radius: {c['nav_radius']};
            font-size: 10pt;
            font-weight: 500;
        }}
        #navBtn:hover {{
            background: {c['secondary_container']};
            color: {c['on_surface']};
        }}
        #navBtn:checked {{
            background: {c['primary_container']};
            color: {c['on_primary_container']};
            font-weight: 600;
        }}
        #navBtn:disabled {{
            color: {c['outline']};
        }}
        /* 组间分割线 (WinUI3: DividerStroke) */
        #navDivider {{
            background: {c['outline_variant']};
            margin: 4px 16px;
            border: none;
        }}
        #exitBtn {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 10px 16px;
            text-align: left;
            border-radius: {c['nav_radius']};
            font-size: 10pt;
            font-weight: 500;
        }}
        #exitBtn:hover {{
            background: {c['exit_btn_bg']};
            color: {c['on_error']};
        }}

        #pageTitle {{
            font-size: 20pt;
            font-weight: 400;
            color: {c['on_surface']};
            padding: 8px 0 4px 0;
            background: transparent;
        }}

        /* 内容区：半透明，让 Acrylic 透出来 */
        #contentArea {{
            background: transparent;
        }}

        QStackedWidget {{
            background: transparent;
        }}
        QStackedWidget > QWidget {{
            background: transparent;
        }}

        QScrollArea {{
            background: transparent;
            border: none;
        }}
        QScrollArea > QWidget > QWidget {{
            background: transparent;
        }}

        QGroupBox {{
            background: rgba(255, 255, 255, 0.70);
        }}

        QCalendarWidget {{
            background: rgba(255, 255, 255, 0.70);
            color: {c['on_surface']};
            border: 1px solid {c['outline']};
            border-radius: {c['card_radius']};
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
            border: 1px solid {c['outline']};
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
            border-bottom: 1px solid {c['outline']};
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
            width: 12px;
            margin: 0;
        }}
        QScrollBar::handle:vertical {{
            background: {c['outline']};
            border-radius: 6px;
            min-height: 30px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {c['on_surface_variant']};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
        }}

        /* ---- 二级菜单（设置页面子导航）---- */
        #subNav {{
            background: {c['surface']};
            border: none;
            border-right: 1px solid {c['outline']};
        }}
        #subNavTitle {{
            color: {c['on_surface']};
            font-size: 11pt;
            font-weight: 600;
            padding: 6px 4px;
        }}
        #subNavBtn {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 10px 14px;
            text-align: left;
            border-radius: {c['nav_radius']};
            font-size: 10pt;
            font-weight: 500;
        }}
        #subNavBtn:hover {{
            background: {c['secondary_container']};
            color: {c['on_surface']};
        }}
        #subNavBtn:checked {{
            background: {c['primary_container']};
            color: {c['on_primary_container']};
            font-weight: 600;
        }}

        /* ---- 导入按钮 (WinUI3: 圆角矩形, accent 色, 8dp 圆角) ---- */
        #importFab {{
            background: {c['primary']};
            color: {c['on_primary']};
            border: none;
            border-radius: {c['card_radius']};
            font-size: 16pt;
            font-weight: 500;
            min-width: 48px;
            min-height: 48px;
            padding: 0;
        }}
        #importFab:hover {{
            background: {c['primary']};
            border: 1px solid {c['primary']};
        }}
        #importFab:pressed {{
            transform: scale(0.95);
        }}

        /* ---- 模块卡片（基于 animation-vocabulary）---- */
        #moduleCard {{
            background: rgba(255, 255, 255, 0.70);
            border: 1px solid {c['outline']};
            border-radius: {c['card_radius']};
            margin-bottom: 8px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
            transition: box-shadow 200ms ease-out, border-color 200ms ease-out, transform 150ms ease-out;
        }}
        #moduleCard:hover {{
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            border-color: {c['primary']};
        }}
        #moduleCard:pressed {{
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
            transform: scale(0.98);
        }}

        /* ---- Toggle Switch（基于 animation-vocabulary）---- */
        #toggleSwitch {{
            background: {c['outline']};
            border: none;
            border-radius: 12px;
            min-width: 44px;
            min-height: 24px;
            padding: 0;
            margin: 0;
            transition: background 200ms ease-out;
        }}
        #toggleSwitch:checked {{
            background: {c['primary']};
        }}
        #toggleSwitch::indicator {{
            width: 20px;
            height: 20px;
            background: white;
            border-radius: 10px;
            margin: 2px;
            transition: margin-left 200ms ease-out;
        }}
        #toggleSwitch:checked::indicator {{
            margin-left: 22px;
        }}

        /* ---- 查看按钮 ---- */
        #viewBtn {{
            background: {c['primary']};
            color: {c['on_primary']};
            border: none;
            border-radius: {c['btn_radius']};
            padding: 4px 12px;
            font-size: 9pt;
            font-weight: 500;
            transition: background 200ms ease-out, transform 100ms ease-out;
        }}
        #viewBtn:hover {{
            opacity: 0.9;
        }}
        #viewBtn:pressed {{
            transform: scale(0.95);
        }}
        #viewBtn:disabled {{
            background: {c['surface_variant']};
            color: {c['outline']};
        }}
    """


def _winui3_dialog(c):
    return f"""
        QDialog {{
            background: {c['background']};
        }}
        QGroupBox {{
            font-weight: 500;
            border: 1px solid {c['outline']};
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
            background: {c['primary']};
            border: 1px solid {c['primary']};
        }}
        QLabel {{ background: transparent; color: {c['on_background']}; }}
    """


# ============================================================
#  Win10 Fluent 早期样式（2017-2021，无 Mica）
#  - 字体：Segoe UI（静态，非 Variable）
#  - 圆角：4dp（按钮/卡片）/ 8dp（对话框）
#  - 选中态：左侧 4dp 实心主题色竖条 + 文字主题色，背景无色
#  - 卡片：1dp 底线 #E5E5E5 + 0 1px 2px rgba(0,0,0,0.08)
#  - 材质：Acrylic（SetWindowCompositionAttribute + AccentState=4）
#  - 背景：浅=#FFF/#F2F2F2/#F9F9F9，暗=#1A1A1A/#2B2B2B
# ============================================================
def _win10fluent_global(c):
    return f"""
        QWidget {{
            color: {c['on_background']};
            font-family: "Segoe UI", sans-serif;
        }}
        QGroupBox {{
            font-weight: 500;
            border: 1px solid {c['outline']};
            border-radius: {c['card_radius']};
            margin-top: 14px;
            padding: 16px 14px 14px 14px;
            background: rgba(255, 255, 255, 0.70);
            color: {c['on_surface_variant']};
            box-shadow: 0 1px 2px {c['shadow']};
            border-bottom: 1px solid {c['outline']};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 16px; padding: 0 6px;
            color: {c['primary']}; font-weight: 600;
        }}
        QPushButton {{
            background: rgba(255, 255, 255, 0.80);
            color: {c['on_surface']};
            border: 1px solid {c['outline']};
            padding: 8px 18px;
            border-radius: {c['btn_radius']};
            font-weight: 500;
            min-height: 22px;
        }}
        QPushButton:hover {{
            border-color: {c['primary']};
        }}
        QPushButton:pressed {{
            background: {c['primary']};
            color: {c['on_primary']};
            border-color: {c['primary']};
        }}
        QPushButton:disabled {{
            background: rgba(255, 255, 255, 0.50);
            color: {c['outline']};
            border-color: {c['outline']};
        }}
        QLineEdit, QTextEdit {{
            background: rgba(255, 255, 255, 0.80);
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
            background: rgba(255, 255, 255, 0.50);
            color: {c['on_surface_variant']};
            border-top: 1px solid {c['outline']};
        }}
    """


def _win10fluent_main(c):
    return f"""
        /* ---- NavigationView (Win10 Fluent) ---- */
        #sidebar {{
            background: rgba(249, 249, 249, 0.30);
            border: none;
            border-right: 1px solid {c['outline']};
        }}
        #sidebarTitle {{
            color: {c['on_surface']};
            font-size: 18pt;
            font-weight: 400;
        }}
        #toggleBtn {{
            background: transparent;
            border: none;
            border-radius: {c['btn_radius']};
            font-size: 14pt;
        }}
        #toggleBtn:hover {{
            background: {c['sidebar_hover']};
        }}
        #navScroll {{
            background: transparent;
            border: none;
        }}
        #navScroll > QWidget {{
            background: transparent;
        }}
        #navContainer {{
            background: transparent;
        }}
        /* 分类组标题 */
        #navGroupHeader {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 12px 16px 6px 16px;
            text-align: left;
            font-size: 12pt;
            font-weight: 600;
        }}
        /* 导航项 (Win10 Fluent: 选中=左侧4dp竖条+文字主题色, 背景无色) */
        #navBtn {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            border-left: 4px solid transparent;
            padding: 10px 16px;
            text-align: left;
            border-radius: 0;
            font-size: 10pt;
            font-weight: 500;
        }}
        #navBtn:hover {{
            background: {c['sidebar_hover']};
            color: {c['on_surface']};
        }}
        #navBtn:checked {{
            border-left: 4px solid {c['primary']};
            color: {c['primary']};
            font-weight: 600;
            padding-left: 12px;
        }}
        #navBtn:disabled {{
            color: {c['outline']};
        }}
        /* 组间分割线 (Win10 Fluent: DividerStroke) */
        #navDivider {{
            background: {c['outline']};
            margin: 4px 16px;
            border: none;
        }}
        #exitBtn {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            border-left: 4px solid transparent;
            padding: 10px 16px;
            text-align: left;
            border-radius: 0;
            font-size: 10pt;
            font-weight: 500;
        }}
        #exitBtn:hover {{
            background: {c['exit_btn_bg']};
            color: {c['on_error']};
            border-left: 4px solid {c['exit_btn_bg']};
            padding-left: 12px;
        }}

        #pageTitle {{
            font-size: 20pt;
            font-weight: 400;
            color: {c['on_surface']};
            padding: 8px 0 4px 0;
            background: transparent;
        }}

        /* 内容区：透明，让 Acrylic 透出来 */
        #contentArea {{
            background: transparent;
        }}

        QStackedWidget {{
            background: transparent;
        }}
        QStackedWidget > QWidget {{
            background: transparent;
        }}

        QScrollArea {{
            background: transparent;
            border: none;
        }}
        QScrollArea > QWidget > QWidget {{
            background: transparent;
        }}

        QCalendarWidget {{
            background: rgba(255, 255, 255, 0.70);
            color: {c['on_surface']};
            border: 1px solid {c['outline']};
            border-radius: {c['card_radius']};
        }}
        QCalendarWidget QToolButton {{
            color: {c['on_surface']};
            background: transparent;
            border: none;
            border-radius: {c['btn_radius']};
            padding: 4px 8px;
        }}
        QCalendarWidget QToolButton:hover {{
            background: {c['sidebar_hover']};
        }}
        QCalendarWidget QMenu {{
            background: rgba(255, 255, 255, 0.90);
            color: {c['on_surface']};
            border: 1px solid {c['outline']};
        }}
        QCalendarWidget QAbstractItemView {{
            background: rgba(255, 255, 255, 0.70);
            color: {c['on_surface']};
            selection-background-color: {c['primary']};
            selection-color: {c['on_primary']};
            border: none;
        }}

        QMenuBar {{
            background: rgba(255, 255, 255, 0.50);
            color: {c['on_surface']};
            border-bottom: 1px solid {c['outline']};
            padding: 2px;
        }}
        QMenuBar::item {{
            background: transparent;
            padding: 6px 12px;
            border-radius: {c['btn_radius']};
        }}
        QMenuBar::item:selected {{
            background: {c['sidebar_hover']};
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

        /* ---- 二级菜单（设置页面子导航）---- */
        #subNav {{
            background: {c['surface']};
            border: none;
            border-right: 1px solid {c['outline']};
        }}
        #subNavTitle {{
            color: {c['on_surface']};
            font-size: 11pt;
            font-weight: 600;
            padding: 6px 4px;
        }}
        #subNavBtn {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            border-left: 4px solid transparent;
            padding: 10px 14px;
            text-align: left;
            border-radius: 0;
            font-size: 10pt;
            font-weight: 500;
        }}
        #subNavBtn:hover {{
            background: {c['sidebar_hover']};
            color: {c['on_surface']};
        }}
        #subNavBtn:checked {{
            border-left: 4px solid {c['primary']};
            color: {c['primary']};
            font-weight: 600;
            padding-left: 10px;
        }}

        /* ---- 导入按钮 (Win10 Fluent: 圆角矩形, 主题色) ---- */
        #importFab {{
            background: {c['primary']};
            color: {c['on_primary']};
            border: none;
            border-radius: {c['card_radius']};
            font-size: 16pt;
            font-weight: 500;
            min-width: 48px;
            min-height: 48px;
            padding: 0;
        }}
        #importFab:hover {{
            background: {c['primary']};
            border: 1px solid {c['primary']};
        }}
        #importFab:pressed {{
            transform: scale(0.95);
        }}

        /* ---- 模块卡片（基于 animation-vocabulary）---- */
        #moduleCard {{
            background: rgba(255, 255, 255, 0.70);
            border: 1px solid {c['outline']};
            border-radius: {c['card_radius']};
            margin-bottom: 8px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
            transition: box-shadow 200ms ease-out, border-color 200ms ease-out, transform 150ms ease-out;
        }}
        #moduleCard:hover {{
            box-shadow: 0 3px 8px rgba(0, 0, 0, 0.12);
            border-color: {c['primary']};
        }}
        #moduleCard:pressed {{
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
            transform: scale(0.98);
        }}

        /* ---- Toggle Switch（基于 animation-vocabulary）---- */
        #toggleSwitch {{
            background: {c['outline']};
            border: none;
            border-radius: 12px;
            min-width: 44px;
            min-height: 24px;
            padding: 0;
            margin: 0;
            transition: background 200ms ease-out;
        }}
        #toggleSwitch:checked {{
            background: {c['primary']};
        }}
        #toggleSwitch::indicator {{
            width: 20px;
            height: 20px;
            background: white;
            border-radius: 10px;
            margin: 2px;
            transition: margin-left 200ms ease-out;
        }}
        #toggleSwitch:checked::indicator {{
            margin-left: 22px;
        }}

        /* ---- 查看按钮 ---- */
        #viewBtn {{
            background: {c['primary']};
            color: {c['on_primary']};
            border: none;
            border-radius: {c['btn_radius']};
            padding: 4px 12px;
            font-size: 9pt;
            font-weight: 500;
            transition: background 200ms ease-out, transform 100ms ease-out;
        }}
        #viewBtn:hover {{
            opacity: 0.9;
        }}
        #viewBtn:pressed {{
            transform: scale(0.95);
        }}
        #viewBtn:disabled {{
            background: {c['surface_variant']};
            color: {c['outline']};
        }}
    """


def _win10fluent_dialog(c):
    return f"""
        QDialog {{
            background: transparent;
        }}
        QGroupBox {{
            font-weight: 500;
            border: 1px solid {c['outline']};
            border-radius: {c['card_radius']};
            margin-top: 14px;
            padding: 16px 14px 14px 14px;
            background: rgba(255, 255, 255, 0.70);
            color: {c['on_surface_variant']};
            box-shadow: 0 1px 2px {c['shadow']};
            border-bottom: 1px solid {c['outline']};
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
            background: {c['primary']};
            border: 1px solid {c['primary']};
        }}
        QLabel {{ background: transparent; color: {c['on_background']}; }}
    """


# ============================================================
#  GNOME / libadwaita 样式
#  - Cantarell / Inter 字体
#  - 圆角：6dp（按钮）/ 12dp（卡片/导航）
#  - 按钮：无边框，hover 用 sidebar_hover 色（不变边框色）
#  - 选中态：半透明强调色 (primary_container)
#  - QGroupBox：1px solid outline 边框
#  - 暗色 shadow: rgba(0,0,0,0.08)
# ============================================================
def _gnome_global(c):
    return f"""
        QWidget {{
            background: {c['background']};
            color: {c['on_background']};
            font-family: "Cantarell", "Inter", sans-serif;
        }}
        QGroupBox {{
            font-weight: 500;
            border: 1px solid {c['outline']};
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
        /* GNOME 按钮：无边框，hover 用 sidebar_hover，不变边框色 */
        QPushButton {{
            background: transparent;
            color: {c['on_surface']};
            border: none;
            padding: 8px 18px;
            border-radius: {c['btn_radius']};
            font-weight: 500;
            min-height: 22px;
        }}
        QPushButton:hover {{
            background: {c['sidebar_hover']};
        }}
        QPushButton:disabled {{
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
            border-top: 1px solid {c['outline']};
        }}
        QStackedWidget, QScrollArea, #contentArea {{
            background: {c['surface']};
        }}
    """


def _gnome_main(c):
    return f"""
        QMainWindow {{
            background: {c['background']};
        }}

        /* ---- Navigation Drawer (GNOME) ---- */
        #sidebar {{
            background: {c['sidebar_bg']};
            border: none;
            border-right: 1px solid {c['outline']};
        }}
        #sidebarTitle {{
            color: {c['on_surface']};
            font-size: 18pt;
            font-weight: 400;
        }}
        #toggleBtn {{
            background: transparent;
            border: none;
            border-radius: {c['btn_radius']};
            font-size: 14pt;
        }}
        #toggleBtn:hover {{
            background: {c['sidebar_hover']};
        }}
        #navScroll {{
            background: transparent;
            border: none;
        }}
        /* 分类组标题 */
        #navGroupHeader {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 12px 16px 6px 16px;
            text-align: left;
            font-size: 12pt;
            font-weight: 600;
        }}
        /* 导航项 (GNOME: 选中=半透明强调色, hover=sidebar_hover) */
        #navBtn {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 10px 16px;
            text-align: left;
            border-radius: {c['nav_radius']};
            font-size: 10pt;
            font-weight: 500;
        }}
        #navBtn:hover {{
            background: {c['sidebar_hover']};
            color: {c['on_surface']};
        }}
        #navBtn:checked {{
            background: {c['primary_container']};
            color: {c['on_primary_container']};
            font-weight: 600;
        }}
        #navBtn:disabled {{
            color: {c['outline']};
        }}
        /* 组间分割线 (GNOME: outline) */
        #navDivider {{
            background: {c['outline_variant']};
            margin: 4px 16px;
            border: none;
        }}
        #exitBtn {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 10px 16px;
            text-align: left;
            border-radius: {c['nav_radius']};
            font-size: 10pt;
            font-weight: 500;
        }}
        #exitBtn:hover {{
            background: {c['exit_btn_bg']};
            color: {c['on_error']};
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
            border: 1px solid {c['outline']};
            border-radius: {c['card_radius']};
        }}
        QCalendarWidget QToolButton {{
            color: {c['on_surface']};
            background: transparent;
            border: none;
            border-radius: {c['btn_radius']};
            padding: 4px 8px;
        }}
        QCalendarWidget QToolButton:hover {{
            background: {c['sidebar_hover']};
        }}
        QCalendarWidget QMenu {{
            background: {c['surface']};
            color: {c['on_surface']};
            border: 1px solid {c['outline']};
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
            border-bottom: 1px solid {c['outline']};
            padding: 2px;
        }}
        QMenuBar::item {{
            background: transparent;
            padding: 6px 12px;
            border-radius: {c['btn_radius']};
        }}
        QMenuBar::item:selected {{
            background: {c['sidebar_hover']};
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

        /* ---- 二级菜单（设置页面子导航）---- */
        #subNav {{
            background: {c['surface']};
            border: none;
            border-right: 1px solid {c['outline']};
        }}
        #subNavTitle {{
            color: {c['on_surface']};
            font-size: 11pt;
            font-weight: 600;
            padding: 6px 4px;
        }}
        #subNavBtn {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 10px 14px;
            text-align: left;
            border-radius: {c['nav_radius']};
            font-size: 10pt;
            font-weight: 500;
        }}
        #subNavBtn:hover {{
            background: {c['sidebar_hover']};
            color: {c['on_surface']};
        }}
        #subNavBtn:checked {{
            background: {c['primary_container']};
            color: {c['on_primary_container']};
            font-weight: 600;
        }}

        /* ---- 导入按钮 (GNOME: 圆角矩形, primary_container 背景) ---- */
        #importFab {{
            background: {c['primary_container']};
            color: {c['on_primary_container']};
            border: none;
            border-radius: {c['card_radius']};
            font-size: 16pt;
            font-weight: 500;
            min-width: 48px;
            min-height: 48px;
            padding: 0;
        }}
        #importFab:hover {{
            background: {c['primary']};
            color: {c['on_primary']};
        }}
        #importFab:pressed {{
            transform: scale(0.95);
        }}

        /* ---- 模块卡片（基于 animation-vocabulary）---- */
        #moduleCard {{
            background: {c['surface']};
            border: 1px solid {c['outline']};
            border-radius: {c['card_radius']};
            margin-bottom: 8px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
            transition: box-shadow 200ms ease-out, border-color 200ms ease-out, transform 150ms ease-out;
        }}
        #moduleCard:hover {{
            box-shadow: 0 3px 6px rgba(0, 0, 0, 0.08);
            border-color: {c['primary']};
        }}
        #moduleCard:pressed {{
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
            transform: scale(0.98);
        }}

        /* ---- Toggle Switch（基于 animation-vocabulary）---- */
        #toggleSwitch {{
            background: {c['outline']};
            border: none;
            border-radius: 12px;
            min-width: 44px;
            min-height: 24px;
            padding: 0;
            margin: 0;
            transition: background 200ms ease-out;
        }}
        #toggleSwitch:checked {{
            background: {c['primary']};
        }}
        #toggleSwitch::indicator {{
            width: 20px;
            height: 20px;
            background: white;
            border-radius: 10px;
            margin: 2px;
            transition: margin-left 200ms ease-out;
        }}
        #toggleSwitch:checked::indicator {{
            margin-left: 22px;
        }}

        /* ---- 查看按钮 ---- */
        #viewBtn {{
            background: {c['primary']};
            color: {c['on_primary']};
            border: none;
            border-radius: {c['btn_radius']};
            padding: 4px 12px;
            font-size: 9pt;
            font-weight: 500;
            transition: background 200ms ease-out, transform 100ms ease-out;
        }}
        #viewBtn:hover {{
            background: {c['primary_container']};
            color: {c['on_primary_container']};
        }}
        #viewBtn:pressed {{
            transform: scale(0.95);
        }}
        #viewBtn:disabled {{
            background: {c['surface_variant']};
            color: {c['outline']};
        }}
    """


def _gnome_dialog(c):
    return f"""
        QDialog {{
            background: {c['background']};
        }}
        QGroupBox {{
            font-weight: 500;
            border: 1px solid {c['outline']};
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
        /* GNOME 对话框按钮：suggested-action 风格，primary 填充 */
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
#  KDE Plasma / Breeze 样式
#  - Noto Sans / DejaVu Sans 字体
#  - 圆角：4dp（按钮）/ 8dp（卡片/导航）
#  - 按钮：1px outline 边框，hover 时边框变 primary
#  - 选中态：半透明强调色 (primary_container)
#  - sidebar 背景为 rgba 半透明值（来自调色板）
#  - QGroupBox：outline 边框
# ============================================================
def _kde_global(c):
    return f"""
        QWidget {{
            background: {c['background']};
            color: {c['on_background']};
            font-family: "Noto Sans", "DejaVu Sans", sans-serif;
        }}
        QGroupBox {{
            font-weight: 500;
            border: 1px solid {c['outline']};
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
        /* KDE 按钮：1px outline 边框，hover 时边框变 primary */
        QPushButton {{
            background: {c['surface']};
            color: {c['on_surface']};
            border: 1px solid {c['outline']};
            padding: 8px 18px;
            border-radius: {c['btn_radius']};
            font-weight: 500;
            min-height: 22px;
        }}
        QPushButton:hover {{
            background: {c['secondary_container']};
            border-color: {c['primary']};
        }}
        QPushButton:pressed {{
            background: {c['primary_container']};
        }}
        QPushButton:disabled {{
            background: {c['surface_variant']};
            color: {c['outline']};
            border-color: {c['outline']};
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
            border-top: 1px solid {c['outline']};
        }}
        QStackedWidget, QScrollArea, #contentArea {{
            background: {c['surface']};
        }}
    """


def _kde_main(c):
    return f"""
        QMainWindow {{
            background: {c['background']};
        }}

        /* ---- Navigation Drawer (KDE) ---- */
        #sidebar {{
            background: {c['sidebar_bg']};
            border: none;
            border-right: 1px solid {c['outline']};
        }}
        #sidebarTitle {{
            color: {c['on_surface']};
            font-size: 18pt;
            font-weight: 400;
        }}
        #toggleBtn {{
            background: transparent;
            border: none;
            border-radius: {c['btn_radius']};
            font-size: 14pt;
        }}
        #toggleBtn:hover {{
            background: {c['sidebar_hover']};
        }}
        #navScroll {{
            background: transparent;
            border: none;
        }}
        /* 分类组标题 */
        #navGroupHeader {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 12px 16px 6px 16px;
            text-align: left;
            font-size: 12pt;
            font-weight: 600;
        }}
        /* 导航项 (KDE: 选中=半透明强调色, hover=sidebar_hover) */
        #navBtn {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 10px 16px;
            text-align: left;
            border-radius: {c['nav_radius']};
            font-size: 10pt;
            font-weight: 500;
        }}
        #navBtn:hover {{
            background: {c['sidebar_hover']};
            color: {c['on_surface']};
        }}
        #navBtn:checked {{
            background: {c['primary_container']};
            color: {c['on_primary_container']};
            font-weight: 600;
        }}
        #navBtn:disabled {{
            color: {c['outline']};
        }}
        /* 组间分割线 (KDE: outline) */
        #navDivider {{
            background: {c['outline_variant']};
            margin: 4px 16px;
            border: none;
        }}
        #exitBtn {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 10px 16px;
            text-align: left;
            border-radius: {c['nav_radius']};
            font-size: 10pt;
            font-weight: 500;
        }}
        #exitBtn:hover {{
            background: {c['exit_btn_bg']};
            color: {c['on_error']};
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
            border: 1px solid {c['outline']};
            border-radius: {c['card_radius']};
        }}
        QCalendarWidget QToolButton {{
            color: {c['on_surface']};
            background: transparent;
            border: none;
            border-radius: {c['btn_radius']};
            padding: 4px 8px;
        }}
        QCalendarWidget QToolButton:hover {{
            background: {c['sidebar_hover']};
        }}
        QCalendarWidget QMenu {{
            background: {c['surface']};
            color: {c['on_surface']};
            border: 1px solid {c['outline']};
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
            border-bottom: 1px solid {c['outline']};
            padding: 2px;
        }}
        QMenuBar::item {{
            background: transparent;
            padding: 6px 12px;
            border-radius: {c['btn_radius']};
        }}
        QMenuBar::item:selected {{
            background: {c['sidebar_hover']};
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

        /* ---- 二级菜单（设置页面子导航）---- */
        #subNav {{
            background: {c['surface']};
            border: none;
            border-right: 1px solid {c['outline']};
        }}
        #subNavTitle {{
            color: {c['on_surface']};
            font-size: 11pt;
            font-weight: 600;
            padding: 6px 4px;
        }}
        #subNavBtn {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 10px 14px;
            text-align: left;
            border-radius: {c['nav_radius']};
            font-size: 10pt;
            font-weight: 500;
        }}
        #subNavBtn:hover {{
            background: {c['sidebar_hover']};
            color: {c['on_surface']};
        }}
        #subNavBtn:checked {{
            background: {c['primary_container']};
            color: {c['on_primary_container']};
            font-weight: 600;
        }}

        /* ---- 导入按钮 (KDE: 圆角矩形, primary_container 背景) ---- */
        #importFab {{
            background: {c['primary_container']};
            color: {c['on_primary_container']};
            border: none;
            border-radius: {c['card_radius']};
            font-size: 16pt;
            font-weight: 500;
            min-width: 48px;
            min-height: 48px;
            padding: 0;
        }}
        #importFab:hover {{
            background: {c['primary']};
            color: {c['on_primary']};
        }}
        #importFab:pressed {{
            transform: scale(0.95);
        }}

        /* ---- 模块卡片（基于 animation-vocabulary）---- */
        #moduleCard {{
            background: {c['surface']};
            border: 1px solid {c['outline']};
            border-radius: {c['card_radius']};
            margin-bottom: 8px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
            transition: box-shadow 200ms ease-out, border-color 200ms ease-out, transform 150ms ease-out;
        }}
        #moduleCard:hover {{
            box-shadow: 0 3px 6px rgba(0, 0, 0, 0.08);
            border-color: {c['primary']};
        }}
        #moduleCard:pressed {{
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
            transform: scale(0.98);
        }}

        /* ---- Toggle Switch（基于 animation-vocabulary）---- */
        #toggleSwitch {{
            background: {c['outline']};
            border: none;
            border-radius: 12px;
            min-width: 44px;
            min-height: 24px;
            padding: 0;
            margin: 0;
            transition: background 200ms ease-out;
        }}
        #toggleSwitch:checked {{
            background: {c['primary']};
        }}
        #toggleSwitch::indicator {{
            width: 20px;
            height: 20px;
            background: white;
            border-radius: 10px;
            margin: 2px;
            transition: margin-left 200ms ease-out;
        }}
        #toggleSwitch:checked::indicator {{
            margin-left: 22px;
        }}

        /* ---- 查看按钮 ---- */
        #viewBtn {{
            background: {c['primary']};
            color: {c['on_primary']};
            border: none;
            border-radius: {c['btn_radius']};
            padding: 4px 12px;
            font-size: 9pt;
            font-weight: 500;
            transition: background 200ms ease-out, transform 100ms ease-out;
        }}
        #viewBtn:hover {{
            background: {c['primary_container']};
            color: {c['on_primary_container']};
        }}
        #viewBtn:pressed {{
            transform: scale(0.95);
        }}
        #viewBtn:disabled {{
            background: {c['surface_variant']};
            color: {c['outline']};
        }}
    """


def _kde_dialog(c):
    return f"""
        QDialog {{
            background: {c['background']};
        }}
        QGroupBox {{
            font-weight: 500;
            border: 1px solid {c['outline']};
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
        /* KDE 对话框按钮：primary 填充 */
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
#  macOS / Cupertino 样式
#  - SF Pro Display / SF Pro Text / Helvetica Neue 字体
#  - 圆角：8dp（按钮）/ 12dp（卡片/导航）
#  - 按钮：系统灰背景（非 primary 色），hover 变深
#  - 选中态：实心强调色 (primary_container = accent hex)
#  - QGroupBox：极淡 outline 边框，圆角 12px
# ============================================================
def _cupertino_global(c):
    return f"""
        QWidget {{
            background: {c['background']};
            color: {c['on_background']};
            font-family: "SF Pro Display", "SF Pro Text", "Helvetica Neue", sans-serif;
        }}
        /* QGroupBox：极淡 outline 边框，圆角 12px */
        QGroupBox {{
            font-weight: 500;
            border: 1px solid {c['outline_variant']};
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
        /* macOS 按钮：系统灰背景（非 primary），hover 变深 */
        QPushButton {{
            background: {c['surface_variant']};
            color: {c['on_surface']};
            border: none;
            padding: 8px 18px;
            border-radius: {c['btn_radius']};
            font-weight: 500;
            min-height: 22px;
        }}
        QPushButton:hover {{
            background: {c['outline']};
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
            border-top: 1px solid {c['outline']};
        }}
        QStackedWidget, QScrollArea, #contentArea {{
            background: {c['surface']};
        }}
    """


def _cupertino_main(c):
    return f"""
        QMainWindow {{
            background: {c['background']};
        }}

        /* ---- Navigation Drawer (macOS) ---- */
        #sidebar {{
            background: {c['sidebar_bg']};
            border: none;
            border-right: 1px solid {c['outline']};
        }}
        #sidebarTitle {{
            color: {c['on_surface']};
            font-size: 18pt;
            font-weight: 400;
        }}
        #toggleBtn {{
            background: transparent;
            border: none;
            border-radius: {c['btn_radius']};
            font-size: 14pt;
        }}
        #toggleBtn:hover {{
            background: {c['sidebar_hover']};
        }}
        #navScroll {{
            background: transparent;
            border: none;
        }}
        /* 分类组标题 */
        #navGroupHeader {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 12px 16px 6px 16px;
            text-align: left;
            font-size: 12pt;
            font-weight: 600;
        }}
        /* 导航项 (macOS: 选中=实心强调色, hover=sidebar_hover) */
        #navBtn {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 10px 16px;
            text-align: left;
            border-radius: {c['nav_radius']};
            font-size: 10pt;
            font-weight: 500;
        }}
        #navBtn:hover {{
            background: {c['sidebar_hover']};
            color: {c['on_surface']};
        }}
        #navBtn:checked {{
            background: {c['primary_container']};
            color: {c['on_primary_container']};
            font-weight: 600;
        }}
        #navBtn:disabled {{
            color: {c['outline']};
        }}
        /* 组间分割线 (macOS: outline) */
        #navDivider {{
            background: {c['outline_variant']};
            margin: 4px 16px;
            border: none;
        }}
        #exitBtn {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 10px 16px;
            text-align: left;
            border-radius: {c['nav_radius']};
            font-size: 10pt;
            font-weight: 500;
        }}
        #exitBtn:hover {{
            background: {c['exit_btn_bg']};
            color: {c['on_error']};
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
            border: 1px solid {c['outline']};
            border-radius: {c['card_radius']};
        }}
        QCalendarWidget QToolButton {{
            color: {c['on_surface']};
            background: transparent;
            border: none;
            border-radius: {c['btn_radius']};
            padding: 4px 8px;
        }}
        QCalendarWidget QToolButton:hover {{
            background: {c['sidebar_hover']};
        }}
        QCalendarWidget QMenu {{
            background: {c['surface']};
            color: {c['on_surface']};
            border: 1px solid {c['outline']};
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
            border-bottom: 1px solid {c['outline']};
            padding: 2px;
        }}
        QMenuBar::item {{
            background: transparent;
            padding: 6px 12px;
            border-radius: {c['btn_radius']};
        }}
        QMenuBar::item:selected {{
            background: {c['sidebar_hover']};
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

        /* ---- 二级菜单（设置页面子导航）---- */
        #subNav {{
            background: {c['surface']};
            border: none;
            border-right: 1px solid {c['outline']};
        }}
        #subNavTitle {{
            color: {c['on_surface']};
            font-size: 11pt;
            font-weight: 600;
            padding: 6px 4px;
        }}
        #subNavBtn {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 10px 14px;
            text-align: left;
            border-radius: {c['nav_radius']};
            font-size: 10pt;
            font-weight: 500;
        }}
        #subNavBtn:hover {{
            background: {c['sidebar_hover']};
            color: {c['on_surface']};
        }}
        #subNavBtn:checked {{
            background: {c['primary_container']};
            color: {c['on_primary_container']};
            font-weight: 600;
        }}

        /* ---- 导入按钮 (macOS: 圆角矩形, 实心强调色) ---- */
        #importFab {{
            background: {c['primary']};
            color: {c['on_primary']};
            border: none;
            border-radius: {c['card_radius']};
            font-size: 16pt;
            font-weight: 500;
            min-width: 48px;
            min-height: 48px;
            padding: 0;
        }}
        #importFab:hover {{
            background: {c['primary_container']};
            color: {c['on_primary_container']};
        }}
        #importFab:pressed {{
            transform: scale(0.95);
        }}

        /* ---- 模块卡片（基于 animation-vocabulary）---- */
        #moduleCard {{
            background: {c['surface']};
            border: 1px solid {c['outline']};
            border-radius: {c['card_radius']};
            margin-bottom: 8px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            transition: box-shadow 200ms ease-out, border-color 200ms ease-out, transform 150ms ease-out;
        }}
        #moduleCard:hover {{
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
            border-color: {c['primary']};
        }}
        #moduleCard:pressed {{
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            transform: scale(0.98);
        }}

        /* ---- Toggle Switch（基于 animation-vocabulary）---- */
        #toggleSwitch {{
            background: {c['outline']};
            border: none;
            border-radius: 12px;
            min-width: 44px;
            min-height: 24px;
            padding: 0;
            margin: 0;
            transition: background 200ms ease-out;
        }}
        #toggleSwitch:checked {{
            background: {c['primary']};
        }}
        #toggleSwitch::indicator {{
            width: 20px;
            height: 20px;
            background: white;
            border-radius: 10px;
            margin: 2px;
            transition: margin-left 200ms ease-out;
        }}
        #toggleSwitch:checked::indicator {{
            margin-left: 22px;
        }}

        /* ---- 查看按钮 ---- */
        #viewBtn {{
            background: {c['primary']};
            color: {c['on_primary']};
            border: none;
            border-radius: {c['btn_radius']};
            padding: 4px 12px;
            font-size: 9pt;
            font-weight: 500;
            transition: background 200ms ease-out, transform 100ms ease-out;
        }}
        #viewBtn:hover {{
            background: {c['primary_container']};
            color: {c['on_primary_container']};
        }}
        #viewBtn:pressed {{
            transform: scale(0.95);
        }}
        #viewBtn:disabled {{
            background: {c['surface_variant']};
            color: {c['outline']};
        }}
    """


def _cupertino_dialog(c):
    return f"""
        QDialog {{
            background: {c['background']};
        }}
        /* QGroupBox：极淡 outline 边框，圆角 12px */
        QGroupBox {{
            font-weight: 500;
            border: 1px solid {c['outline_variant']};
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
        /* macOS 对话框按钮：系统灰背景（非 primary），hover 变深 */
        QPushButton {{
            background: {c['surface_variant']};
            color: {c['on_surface']};
            border: none;
            padding: 8px 24px;
            border-radius: {c['btn_radius']};
            font-weight: 500;
            min-width: 70px;
        }}
        QPushButton:hover {{
            background: {c['outline']};
        }}
        QLabel {{ background: transparent; color: {c['on_background']}; }}
    """


# ============================================================
#  ChromeOS / Material Desktop 样式
#  - Google Sans / Roboto 字体
#  - 圆角：8dp（按钮）/ 12dp（卡片/导航）
#  - 按钮：primary 填充，hover 变深
#  - 选中态：半透明强调色 (primary_container)
#  - 类似 MD3 但圆角更小
# ============================================================
def _chromeos_global(c):
    return f"""
        QWidget {{
            background: {c['background']};
            color: {c['on_background']};
            font-family: "Google Sans", "Roboto", sans-serif;
        }}
        QGroupBox {{
            font-weight: 500;
            border: 1px solid {c['outline']};
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
        /* ChromeOS 按钮：primary 填充，hover 变深 */
        QPushButton {{
            background: {c['primary']};
            color: {c['on_primary']};
            border: none;
            padding: 8px 18px;
            border-radius: {c['btn_radius']};
            font-weight: 500;
            min-height: 22px;
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
            border-top: 1px solid {c['outline']};
        }}
        QStackedWidget, QScrollArea, #contentArea {{
            background: {c['surface']};
        }}
    """


def _chromeos_main(c):
    return f"""
        QMainWindow {{
            background: {c['background']};
        }}

        /* ---- Navigation Drawer (ChromeOS) ---- */
        #sidebar {{
            background: {c['sidebar_bg']};
            border: none;
            border-right: 1px solid {c['outline']};
        }}
        #sidebarTitle {{
            color: {c['on_surface']};
            font-size: 18pt;
            font-weight: 400;
        }}
        #toggleBtn {{
            background: transparent;
            border: none;
            border-radius: {c['btn_radius']};
            font-size: 14pt;
        }}
        #toggleBtn:hover {{
            background: {c['secondary_container']};
        }}
        #navScroll {{
            background: transparent;
            border: none;
        }}
        /* 分类组标题 */
        #navGroupHeader {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 12px 16px 6px 16px;
            text-align: left;
            font-size: 12pt;
            font-weight: 600;
        }}
        /* 导航项 (ChromeOS: 选中=半透明强调色, hover=secondary_container) */
        #navBtn {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 10px 16px;
            text-align: left;
            border-radius: {c['nav_radius']};
            font-size: 10pt;
            font-weight: 500;
        }}
        #navBtn:hover {{
            background: {c['secondary_container']};
            color: {c['on_surface']};
        }}
        #navBtn:checked {{
            background: {c['primary_container']};
            color: {c['on_primary_container']};
            font-weight: 600;
        }}
        #navBtn:disabled {{
            color: {c['outline']};
        }}
        /* 组间分割线 (ChromeOS: outline) */
        #navDivider {{
            background: {c['outline_variant']};
            margin: 4px 16px;
            border: none;
        }}
        #exitBtn {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 10px 16px;
            text-align: left;
            border-radius: {c['nav_radius']};
            font-size: 10pt;
            font-weight: 500;
        }}
        #exitBtn:hover {{
            background: {c['exit_btn_bg']};
            color: {c['on_error']};
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
            border: 1px solid {c['outline']};
            border-radius: {c['card_radius']};
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
            border: 1px solid {c['outline']};
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
            border-bottom: 1px solid {c['outline']};
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

        /* ---- 二级菜单（设置页面子导航）---- */
        #subNav {{
            background: {c['surface']};
            border: none;
            border-right: 1px solid {c['outline']};
        }}
        #subNavTitle {{
            color: {c['on_surface']};
            font-size: 11pt;
            font-weight: 600;
            padding: 6px 4px;
        }}
        #subNavBtn {{
            background: transparent;
            color: {c['on_surface_variant']};
            border: none;
            padding: 10px 14px;
            text-align: left;
            border-radius: {c['nav_radius']};
            font-size: 10pt;
            font-weight: 500;
        }}
        #subNavBtn:hover {{
            background: {c['secondary_container']};
            color: {c['on_surface']};
        }}
        #subNavBtn:checked {{
            background: {c['primary_container']};
            color: {c['on_primary_container']};
            font-weight: 600;
        }}

        /* ---- 导入按钮 (ChromeOS: 圆角矩形, primary 背景) ---- */
        #importFab {{
            background: {c['primary']};
            color: {c['on_primary']};
            border: none;
            border-radius: {c['card_radius']};
            font-size: 16pt;
            font-weight: 500;
            min-width: 48px;
            min-height: 48px;
            padding: 0;
        }}
        #importFab:hover {{
            background: {c['primary_container']};
            color: {c['on_primary_container']};
        }}
        #importFab:pressed {{
            transform: scale(0.95);
        }}

        /* ---- 模块卡片（基于 animation-vocabulary）---- */
        #moduleCard {{
            background: {c['surface']};
            border: 1px solid {c['outline']};
            border-radius: {c['card_radius']};
            margin-bottom: 8px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            transition: box-shadow 200ms ease-out, border-color 200ms ease-out, transform 150ms ease-out;
        }}
        #moduleCard:hover {{
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
            border-color: {c['primary']};
        }}
        #moduleCard:pressed {{
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            transform: scale(0.98);
        }}

        /* ---- Toggle Switch（基于 animation-vocabulary）---- */
        #toggleSwitch {{
            background: {c['outline']};
            border: none;
            border-radius: 12px;
            min-width: 44px;
            min-height: 24px;
            padding: 0;
            margin: 0;
            transition: background 200ms ease-out;
        }}
        #toggleSwitch:checked {{
            background: {c['primary']};
        }}
        #toggleSwitch::indicator {{
            width: 20px;
            height: 20px;
            background: white;
            border-radius: 10px;
            margin: 2px;
            transition: margin-left 200ms ease-out;
        }}
        #toggleSwitch:checked::indicator {{
            margin-left: 22px;
        }}

        /* ---- 查看按钮 ---- */
        #viewBtn {{
            background: {c['primary']};
            color: {c['on_primary']};
            border: none;
            border-radius: {c['btn_radius']};
            padding: 4px 12px;
            font-size: 9pt;
            font-weight: 500;
            transition: background 200ms ease-out, transform 100ms ease-out;
        }}
        #viewBtn:hover {{
            background: {c['primary_container']};
            color: {c['on_primary_container']};
        }}
        #viewBtn:pressed {{
            transform: scale(0.95);
        }}
        #viewBtn:disabled {{
            background: {c['surface_variant']};
            color: {c['outline']};
        }}
    """


def _chromeos_dialog(c):
    return f"""
        QDialog {{
            background: {c['background']};
        }}
        QGroupBox {{
            font-weight: 500;
            border: 1px solid {c['outline']};
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
        /* ChromeOS 对话框按钮：primary 填充 */
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
