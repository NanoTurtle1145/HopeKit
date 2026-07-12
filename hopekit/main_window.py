"""
MainUi — 主窗口

Navigation Drawer + 分类页面 + 模块按钮网格。
设置项为可折叠二级菜单（主题/关于）。
所有模块由 ModuleRegistry 提供，启动时自动 discover。
"""

from hopekit.qt_compat import (
    QtCore, QtGui, QtWidgets,
    QMainWindow, QApplication,
    QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGridLayout, QGroupBox,
)
from hopekit.theme import theme
from hopekit.paths import resource_path
from hopekit.registry import ModuleRegistry
from hopekit.settings_page import SettingsPage
from hopekit.transparency import (
    is_transparent_theme,
    enable_transparency_before_show,
    enable_transparency_for_central,
    apply_backdrop_to_window,
    disable_transparency,
    apply_transparency_dynamic,
)
from Styles import styles


class MainUi(QMainWindow):
    _DRAWER_WIDTH = 240
    _DRAWER_COLLAPSED = 56

    def __init__(self, version: str = ""):
        self._version = version
        super().__init__()
        self.setWindowTitle(f"HopeKit {version}")
        self.resize(1200, 665)
        self.setMinimumSize(900, 600)
        self._drawer_collapsed = False
        self._nav_buttons = []        # (cat, btn) — 分类导航按钮
        self._page_widgets = {}       # category -> QWidget 映射
        self._transparency_applied = False  # 透明效果是否已应用

        # 透明主题：WA_TranslucentBackground 必须在 show() 之前设置
        enable_transparency_before_show(self)

        self._build_ui()
        self._apply_style()

    # ============================================================
    #  UI 构建
    # ============================================================
    def _build_ui(self):
        central = QtWidgets.QWidget(self)
        self.setCentralWidget(central)

        # 透明主题：central 不自动填充背景
        enable_transparency_for_central(central)

        main_layout = QtWidgets.QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self._build_drawer(central, main_layout)
        self._build_content(central, main_layout)

        self.statusBar()
        menu_bar = QtWidgets.QMenuBar(self)
        self.setMenuBar(menu_bar)

    # ---- Navigation Drawer ----
    def _build_drawer(self, parent, parent_layout):
        self._sidebar = QtWidgets.QFrame(parent)
        self._sidebar.setObjectName("sidebar")
        self._sidebar.setFixedWidth(self._DRAWER_WIDTH)

        sidebar_layout = QtWidgets.QVBoxLayout(self._sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # Drawer 顶部（标题 + 折叠按钮）
        self._drawer_header = QtWidgets.QWidget(self._sidebar)
        header_layout = QtWidgets.QHBoxLayout(self._drawer_header)
        header_layout.setContentsMargins(16, 16, 8, 8)
        header_layout.setSpacing(8)

        self._sidebar_title = QtWidgets.QLabel("HopeKit")
        self._sidebar_title.setObjectName("sidebarTitle")
        header_layout.addWidget(self._sidebar_title)
        header_layout.addStretch(1)

        self._toggle_btn = QPushButton("◀")
        self._toggle_btn.setObjectName("toggleBtn")
        self._toggle_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self._toggle_btn.setFixedSize(32, 32)
        self._toggle_btn.clicked.connect(self._toggle_sidebar)
        header_layout.addWidget(self._toggle_btn)

        sidebar_layout.addWidget(self._drawer_header)

        # 可滚动导航区域
        self._nav_scroll = QtWidgets.QScrollArea(self._sidebar)
        self._nav_scroll.setObjectName("navScroll")
        self._nav_scroll.setWidgetResizable(True)
        self._nav_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._nav_scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

        self._nav_container = QtWidgets.QWidget()
        self._nav_container.setObjectName("navContainer")
        nav_layout = QtWidgets.QVBoxLayout(self._nav_container)
        nav_layout.setContentsMargins(8, 4, 8, 4)
        nav_layout.setSpacing(2)

        # 分类导航按钮
        categories = ModuleRegistry.categories()
        for cat in categories:
            btn = QPushButton(cat)
            btn.setObjectName("navBtn")
            btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            btn.setCheckable(True)
            btn.clicked.connect(
                lambda _checked, c=cat: self._switch_category(c)
            )
            nav_layout.addWidget(btn)
            self._nav_buttons.append((cat, btn))

        nav_layout.addStretch(1)

        # 分割线
        divider = QtWidgets.QFrame()
        divider.setObjectName("navDivider")
        divider.setFixedHeight(1)
        nav_layout.addWidget(divider)

        # 设置（可折叠二级菜单）
        self._build_settings_group(nav_layout)

        self._nav_scroll.setWidget(self._nav_container)
        sidebar_layout.addWidget(self._nav_scroll, 1)

        # 退出按钮
        self._exit_btn = QPushButton("退出")
        self._exit_btn.setObjectName("exitBtn")
        self._exit_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self._exit_btn.clicked.connect(self.close)
        sidebar_layout.addWidget(self._exit_btn)

        parent_layout.addWidget(self._sidebar)

    def _build_settings_group(self, parent_layout):
        """构建设置的可折叠二级菜单（主题/关于）。"""
        header_btn = QPushButton("▶  设置")
        header_btn.setObjectName("navGroupHeader")
        header_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        header_btn.setCheckable(False)

        child_container = QtWidgets.QWidget()
        child_layout = QVBoxLayout(child_container)
        child_layout.setContentsMargins(0, 0, 0, 0)
        child_layout.setSpacing(2)

        # 二级菜单项：与 SettingsPage._SUB_PAGES 对应
        sub_pages = [("theme", "主题"), ("about", "关于")]
        sub_btns = []
        for key, display in sub_pages:
            item_btn = QPushButton(f"  {display}")
            item_btn.setObjectName("navBtn")
            item_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            item_btn.setCheckable(True)
            item_btn.clicked.connect(
                lambda _, k=key: self._switch_settings_sub(k)
            )
            child_layout.addWidget(item_btn)
            sub_btns.append((key, item_btn))

        child_container.setVisible(False)

        def toggle_group():
            expanded = child_container.isVisible()
            child_container.setVisible(not expanded)
            header_btn.setText("▼  设置" if not expanded else "▶  设置")

        header_btn.clicked.connect(toggle_group)

        parent_layout.addWidget(header_btn)
        parent_layout.addWidget(child_container)

        self._settings_header_btn = header_btn
        self._settings_child_container = child_container
        self._settings_sub_btns = sub_btns

    # ---- 内容区 ----
    def _build_content(self, parent, parent_layout):
        content = QtWidgets.QWidget(parent)
        content.setObjectName("contentArea")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(16, 16, 16, 16)
        content_layout.setSpacing(12)

        # 顶部标题栏
        self._build_content_header(content_layout)

        # StackedWidget: 各分类页面 + 设置页
        self._stack = QtWidgets.QStackedWidget()

        categories = ModuleRegistry.categories()
        for cat in categories:
            page = self._build_category_page(cat)
            self._stack.addWidget(page)
            self._page_widgets[cat] = page

        # 设置页面（非插件，单独构建）
        self._settings_page = SettingsPage()
        self._settings_page.set_main_window(self)
        self._stack.addWidget(self._settings_page)
        self._page_widgets["设置"] = self._settings_page

        content_layout.addWidget(self._stack, 1)
        parent_layout.addWidget(content, 1)

        # 默认选中第一个分类
        if categories:
            self._switch_category(categories[0])

    def _build_content_header(self, parent_layout):
        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setSpacing(12)

        logo = QtWidgets.QLabel()
        pix = QtGui.QPixmap(resource_path("logo.jpg"))
        if not pix.isNull():
            logo.setPixmap(pix.scaledToHeight(72, QtCore.Qt.TransformationMode.SmoothTransformation))
        logo.setFixedSize(72, 72)
        header_layout.addWidget(logo, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)

        title_box = QtWidgets.QVBoxLayout()
        title_box.setSpacing(2)
        title_lbl = QtWidgets.QLabel(f"HopeKit {self._version}")
        title_lbl.setStyleSheet("font-size:16pt; font-weight:600; color:#333;")
        tip = QtWidgets.QLabel(
            '<span style="font-size:18pt; color:#0000ff;">你今天看起来很聪明！</span>'
        )
        title_box.addWidget(title_lbl)
        title_box.addWidget(tip)
        header_layout.addLayout(title_box)
        header_layout.addStretch(1)
        parent_layout.addLayout(header_layout)

    def _build_category_page(self, category: str):
        page = QtWidgets.QWidget()
        layout = QVBoxLayout(page)
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
            btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
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
                btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
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
                btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
                if info["enabled"]:
                    btn.clicked.connect(lambda _=False, n=name: self._open_module(n))
                else:
                    btn.setEnabled(False)
                row.addWidget(lbl)
                row.addStretch(1)
                row.addWidget(btn)
                contact_layout.addLayout(row)
            parent_layout.addWidget(contact_box)

    # ============================================================
    #  导航逻辑
    # ============================================================
    def _switch_category(self, category: str):
        """切换到分类页面，更新导航按钮选中状态。"""
        if category in self._page_widgets:
            self._stack.setCurrentWidget(self._page_widgets[category])
        for cat, btn in self._nav_buttons:
            btn.setChecked(cat == category)
        # 取消设置子项的选中状态
        for _, btn in self._settings_sub_btns:
            btn.setChecked(False)

    def _switch_settings_sub(self, sub_key: str):
        """切换到设置页面并定位到指定子页面。"""
        self._stack.setCurrentWidget(self._settings_page)
        self._settings_page._switch_sub(sub_key)
        # 取消分类按钮选中
        for _, btn in self._nav_buttons:
            btn.setChecked(False)
        # 更新设置子项选中状态
        for key, btn in self._settings_sub_btns:
            btn.setChecked(key == sub_key)

    def _toggle_sidebar(self):
        self._drawer_collapsed = not self._drawer_collapsed
        if self._drawer_collapsed:
            self._sidebar.setFixedWidth(self._DRAWER_COLLAPSED)
            self._toggle_btn.setText("▶")
            self._sidebar_title.setVisible(False)
            self._nav_scroll.setVisible(False)
            self._exit_btn.setText("×")
            self._drawer_header.layout().setContentsMargins(12, 16, 12, 8)
        else:
            self._sidebar.setFixedWidth(self._DRAWER_WIDTH)
            self._toggle_btn.setText("◀")
            self._sidebar_title.setVisible(True)
            self._nav_scroll.setVisible(True)
            self._exit_btn.setText("退出")
            self._drawer_header.layout().setContentsMargins(16, 16, 8, 8)

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
        self._switch_settings_sub("theme")
        self._settings_page.refresh_theme_display()

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
        if self.isVisible():
            if is_transparent_theme():
                if not self._transparency_applied:
                    ok = apply_transparency_dynamic(self)
                    if ok:
                        self._transparency_applied = True
            else:
                if self._transparency_applied:
                    self._clear_transparency()

    def _apply_transparency(self):
        """应用透明效果（DWM 材质）"""
        if not is_transparent_theme():
            return
        try:
            ok = apply_backdrop_to_window(self, kind=None)
            if ok:
                self._transparency_applied = True
        except Exception as e:
            import traceback
            print(f"[{theme.style}] 透明效果异常: {e}", flush=True)
            traceback.print_exc()

    def _clear_transparency(self):
        """清除透明效果（主题切换时调用）"""
        try:
            disable_transparency(self)
            self._transparency_applied = False
            self.update()
            self.repaint()
        except Exception as e:
            print(f"[Transparency] 清除透明效果异常: {e}", flush=True)

    def showEvent(self, event):
        """窗口显示时尝试开启透明效果（hwnd 在 show 后才有效）"""
        super().showEvent(event)
        # spontaneous=True 是系统触发（如最小化恢复），跳过
        if event.spontaneous() or self._transparency_applied:
            return
        self._apply_transparency()
