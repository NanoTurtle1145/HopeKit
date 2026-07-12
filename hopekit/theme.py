"""
ThemeManager — 多风格主题管理器

风格 (style): md3 / md2 / qt / winui3 / gnome / kde / cupertino / chromeos
模式 (mode):  auto / light / dark

- md3:       Material Design 3，动态强调色 + 大圆角 + 分层 container
- md2:       Material Design 2，Indigo 500 主色 + 扁平化 + 4px 圆角
- qt:        Qt 原生风格，几乎不写样式表，使用 Qt 默认外观
- winui3:    WinUI3 / Fluent Design，系统强调色 + 分层圆角 + 半透明选中态
- gnome:     GNOME / libadwaita，Cantarell 字体 + 6/12px 圆角 + 纯色背景
- kde:       KDE Plasma / Breeze，半透明面板 + 4/8px 圆角
- cupertino: macOS / Apple HIG，SF 字体 + 8/12px 圆角 + 实心选中态
- chromeos:  ChromeOS / Material Desktop，Google Sans + 8/12px 圆角

持久化到本地 JSON。
"""

import json
import os
import shutil
import platform
import sys

from hopekit.paths import config_path, resource_path


class ThemeManager:
    _CONFIG_PATH = config_path("theme.json")

    _MD3_RADII = {
        "card_radius": "16px",
        "btn_radius":  "20px",
        "nav_radius":  "28px",
    }

    _MD2_RADII = {
        "card_radius": "4px",
        "btn_radius":  "4px",
        "nav_radius":  "4px",
    }

    _QT_RADII = {
        "card_radius": "0px",
        "btn_radius":  "0px",
        "nav_radius":  "0px",
    }

    _WINUI3_RADII = {
        "card_radius": "8px",
        "btn_radius":  "4px",
        "nav_radius":  "16px",
    }

    _WIN10FLUENT_RADII = {
        "card_radius": "4px",
        "btn_radius":  "4px",
        "nav_radius":  "4px",
    }

    _GNOME_RADII = {
        "card_radius": "12px",
        "btn_radius":  "6px",
        "nav_radius":  "12px",
    }

    _KDE_RADII = {
        "card_radius": "8px",
        "btn_radius":  "4px",
        "nav_radius":  "8px",
    }

    _CUPERTINO_RADII = {
        "card_radius": "12px",
        "btn_radius":  "8px",
        "nav_radius":  "12px",
    }

    _CHROMEOS_RADII = {
        "card_radius": "12px",
        "btn_radius":  "8px",
        "nav_radius":  "12px",
    }

    @staticmethod
    def _default_style_for_platform() -> str:
        """根据当前系统自动选择最合适的默认主题（优先透明风格）。"""
        if sys.platform == "win32":
            try:
                ver = platform.win32_ver()[1]
                build = int(ver.split('.')[-1])
                if build >= 22621:
                    return "winui3"
                return "win10fluent"
            except (ValueError, IndexError):
                return "win10fluent"
        elif sys.platform == "darwin":
            return "cupertino"
        return "md3"

    def __init__(self):
        self._style = self._default_style_for_platform()
        self._mode = "auto"
        if not self.load():
            self.save()

    # ---- 基本属性 ----
    @property
    def style(self) -> str:
        return self._style

    @property
    def mode(self) -> str:
        return self._mode

    @property
    def is_dark(self) -> bool:
        if self._mode == "dark":
            return True
        if self._mode == "light":
            return False
        return self._read_windows_dark_mode()

    @property
    def colors(self) -> dict:
        accent = self._read_windows_accent()
        if self._style == "md2":
            return self._build_md2_palette(accent, self.is_dark)
        if self._style == "qt":
            return self._build_qt_palette(accent, self.is_dark)
        if self._style == "winui3":
            return self._build_winui3_palette(accent, self.is_dark)
        if self._style == "win10fluent":
            return self._build_win10fluent_palette(accent, self.is_dark)
        if self._style == "gnome":
            return self._build_gnome_palette(accent, self.is_dark)
        if self._style == "kde":
            return self._build_kde_palette(accent, self.is_dark)
        if self._style == "cupertino":
            return self._build_cupertino_palette(accent, self.is_dark)
        if self._style == "chromeos":
            return self._build_chromeos_palette(accent, self.is_dark)
        return self._build_md3_palette(accent, self.is_dark)

    def set_style(self, style: str):
        if style in ("md3", "md2", "qt", "winui3", "win10fluent", "gnome", "kde", "cupertino", "chromeos"):
            self._style = style
            self.save()

    def set_mode(self, mode: str):
        if mode in ("auto", "light", "dark"):
            self._mode = mode
            self.save()

    def load(self) -> bool:
        loaded = False
        try:
            with open(self._CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._apply_config(data)
            loaded = True
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            pass

        if not loaded:
            bundled = resource_path("theme.json")
            if bundled != self._CONFIG_PATH and os.path.isfile(bundled):
                try:
                    with open(bundled, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    self._apply_config(data)
                    os.makedirs(os.path.dirname(self._CONFIG_PATH), exist_ok=True)
                    shutil.copy2(bundled, self._CONFIG_PATH)
                    loaded = True
                except (json.JSONDecodeError, OSError):
                    pass

        return loaded

    def _apply_config(self, data: dict):
        """将 JSON 数据应用到当前配置。"""
        if data.get("style") in (
            "md3", "md2", "qt", "winui3", "win10fluent",
            "gnome", "kde", "cupertino", "chromeos",
        ):
            self._style = data["style"]
        if data.get("mode") in ("auto", "light", "dark"):
            self._mode = data["mode"]

    def save(self):
        try:
            with open(self._CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(
                    {"style": self._style, "mode": self._mode},
                    f, ensure_ascii=False, indent=2,
                )
        except OSError:
            pass

    # ============================================================
    #  Windows 系统色读取
    # ============================================================
    @staticmethod
    def _read_windows_accent() -> tuple:
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\DWM"
            )
            value, _ = winreg.QueryValueEx(key, "AccentColor")
            winreg.CloseKey(key)
            r = value & 0xFF
            g = (value >> 8) & 0xFF
            b = (value >> 16) & 0xFF
            return (r, g, b)
        except Exception:
            return (33, 150, 243)

    @staticmethod
    def _read_windows_dark_mode() -> bool:
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
    #  颜色工具
    # ============================================================
    @staticmethod
    def _mix(c1: tuple, c2: tuple, t: float) -> tuple:
        return (
            round(c1[0] + (c2[0] - c1[0]) * t),
            round(c1[1] + (c2[1] - c1[1]) * t),
            round(c1[2] + (c2[2] - c1[2]) * t),
        )

    @staticmethod
    def _luminance(rgb: tuple) -> float:
        def chan(v):
            v = v / 255.0
            return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
        return 0.2126 * chan(rgb[0]) + 0.7152 * chan(rgb[1]) + 0.0722 * chan(rgb[2])

    @classmethod
    def _on_color(cls, bg: tuple) -> str:
        return "#FFFFFF" if cls._luminance(bg) < 0.5 else "#000000"

    @staticmethod
    def _hex(rgb) -> str:
        if isinstance(rgb, str):
            return rgb
        return "#{:02X}{:02X}{:02X}".format(*rgb)

    @staticmethod
    def _rgba(rgb, alpha: float) -> str:
        """生成 rgba() 字符串，alpha 范围 0.0~1.0"""
        if isinstance(rgb, str):
            return rgb
        r, g, b = int(rgb[0]), int(rgb[1]), int(rgb[2])
        return f"rgba({r},{g},{b},{alpha})"

    # ============================================================
    #  MD3 调色板（之前的实现）
    # ============================================================
    @classmethod
    def _build_md3_palette(cls, accent: tuple, dark: bool) -> dict:
        if dark:
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

        palette = {
            "primary":              cls._hex(primary),
            "on_primary":           on_primary,
            "primary_container":    cls._hex(primary_container),
            "on_primary_container": cls._hex(on_primary_container),
            "secondary":            cls._hex(secondary),
            "on_secondary":         on_secondary,
            "secondary_container":  cls._hex(secondary_container),
            "on_secondary_container": cls._hex(on_secondary_container),
            "surface":              cls._hex(surface),
            "on_surface":           cls._hex(on_surface),
            "surface_variant":      cls._hex(surface_variant),
            "on_surface_variant":   cls._hex(on_surface_variant),
            "background":           cls._hex(background),
            "on_background":        cls._hex(on_background),
            "outline":              cls._hex(outline),
            "outline_variant":      cls._hex(cls._mix(outline, surface, 0.5)),
            "error":                cls._hex(error),
            "on_error":             on_error,
            "shadow":               "#000000",
            "sidebar_bg":           cls._hex(sidebar_bg),
            "sidebar_text":         cls._hex(sidebar_text),
            "sidebar_hover":        cls._hex(sidebar_hover),
            "sidebar_active":       cls._hex(sidebar_active),
            "sidebar_active_border": cls._hex(primary),
            "exit_btn_bg":          cls._hex(error),
            "exit_btn_hover":       cls._hex(cls._mix(error, (255, 255, 255), 0.2)),
        }
        palette.update(cls._MD3_RADII)
        return palette

    # ============================================================
    #  MD2 调色板（Material Design 2 — Indigo 500 + Pink A200）
    #  严格遵循 2014 Google 规范，固定色板，不跟随系统强调色：
    #    primary       = Indigo 500  #3F51B5
    #    primary_dark  = Indigo 700  #303F9F
    #    primary_light = Indigo 100  #C5CAE9
    #    accent        = Pink A200   #FF4081
    #  ❗ 不使用 MD3 的 tonal palette / container 术语
    # ============================================================
    @classmethod
    def _build_md2_palette(cls, accent: tuple, dark: bool) -> dict:
        if dark:
            # MD2 Dark 主题
            primary = (121, 134, 203)        # Indigo 300
            primary_dark = (63, 81, 181)     # Indigo 500
            primary_light = (159, 168, 218)  # Indigo 200
            accent_color = (255, 64, 129)    # Pink A200
            surface = (66, 66, 66)           # Grey 800
            on_surface = (255, 255, 255)
            surface_variant = (97, 97, 97)   # Grey 700
            on_surface_variant = (189, 189, 189)
            background = (48, 48, 48)        # Grey 850
            on_background = (255, 255, 255)
            outline = (97, 97, 97)
            sidebar_bg = (33, 33, 33)        # Grey 900
            sidebar_text = (255, 255, 255)
            sidebar_hover = (66, 66, 66)
            sidebar_active = (63, 81, 181)   # Indigo 500 选中
            error = (229, 115, 115)          # Red 300
            on_error = "#000000"
        else:
            # MD2 Light 主题（标准 Indigo + Pink 色板）
            primary = (63, 81, 181)          # Indigo 500
            primary_dark = (48, 63, 159)     # Indigo 700
            primary_light = (197, 202, 233)  # Indigo 100
            accent_color = (255, 64, 129)    # Pink A200
            surface = (255, 255, 255)
            on_surface = (33, 33, 33)        # Grey 900
            surface_variant = (245, 245, 245)  # Grey 100
            on_surface_variant = (117, 117, 117)  # Grey 600
            background = (250, 250, 250)     # Grey 50
            on_background = (33, 33, 33)
            outline = (189, 189, 189)        # Grey 400
            sidebar_bg = (245, 245, 245)     # Grey 100 (MD2 Drawer 标准)
            sidebar_text = (33, 33, 33)
            sidebar_hover = (238, 238, 238)  # Grey 200
            sidebar_active = (197, 202, 233) # Indigo 100 选中
            error = (211, 47, 47)            # Red 600
            on_error = "#FFFFFF"

        on_primary = "#FFFFFF"
        on_accent = "#FFFFFF"

        palette = {
            # MD2 核心色板（不用 container 术语）
            "primary":              cls._hex(primary),
            "primary_dark":         cls._hex(primary_dark),
            "primary_light":        cls._hex(primary_light),
            "accent":               cls._hex(accent_color),
            "accent_dark":          cls._hex(cls._mix(accent_color, (0, 0, 0), 0.15)),
            "on_primary":           on_primary,
            "on_accent":            on_accent,
            # surface 系列（保留兼容字段，但 MD2 不强调 container）
            "primary_container":    cls._hex(primary_light),
            "on_primary_container": cls._hex(on_surface),
            "secondary":            cls._hex(accent_color),
            "on_secondary":         on_accent,
            "secondary_container":  cls._hex(primary_light),
            "on_secondary_container": cls._hex(on_surface),
            "surface":              cls._hex(surface),
            "on_surface":           cls._hex(on_surface),
            "surface_variant":      cls._hex(surface_variant),
            "on_surface_variant":   cls._hex(on_surface_variant),
            "background":           cls._hex(background),
            "on_background":        cls._hex(on_background),
            "outline":              cls._hex(outline),
            "outline_variant":      cls._hex(cls._mix(outline, surface, 0.5)),
            "error":                cls._hex(error),
            "on_error":             on_error,
            "shadow":               "rgba(0,0,0,0.2)",
            "divider":              cls._hex(outline),
            # 侧边栏（MD2 Drawer 风格）
            "sidebar_bg":           cls._hex(sidebar_bg),
            "sidebar_text":         cls._hex(sidebar_text),
            "sidebar_hover":        cls._hex(sidebar_hover),
            "sidebar_active":       cls._hex(sidebar_active),
            "sidebar_active_border": cls._hex(primary),
            "exit_btn_bg":          cls._hex(error),
            "exit_btn_hover":       cls._hex(cls._mix(error, (0, 0, 0), 0.15)),
        }
        palette.update(cls._MD2_RADII)
        return palette

    # ============================================================
    #  Qt 原生风格调色板
    #  几乎不写样式表，使用 Qt 默认外观。
    #  仅为侧边栏/退出按钮等结构性组件提供最小颜色，
    #  普通 QPushButton / QLineEdit 等完全交给 Qt 原生绘制。
    # ============================================================
    @classmethod
    def _build_qt_palette(cls, accent: tuple, dark: bool) -> dict:
        if dark:
            sidebar_bg = (28, 28, 28)
            sidebar_text = (255, 255, 255)
            sidebar_hover = (51, 51, 51)
            sidebar_active = cls._mix(accent, (51, 51, 51), 0.5)
            error = (202, 54, 54)
            on_error = "#FFFFFF"
            surface = (240, 240, 240)
            on_surface = (0, 0, 0)
            surface_variant = (225, 225, 225)
            on_surface_variant = (109, 109, 109)
            background = (243, 243, 243)
            on_background = (0, 0, 0)
            outline = (204, 204, 204)
        else:
            sidebar_bg = (245, 246, 247)
            sidebar_text = (0, 0, 0)
            sidebar_hover = (229, 229, 229)
            sidebar_active = cls._mix(accent, (229, 229, 229), 0.4)
            error = (196, 43, 43)
            on_error = "#FFFFFF"
            surface = (255, 255, 255)
            on_surface = (0, 0, 0)
            surface_variant = (240, 240, 240)
            on_surface_variant = (109, 109, 109)
            background = (243, 243, 243)
            on_background = (0, 0, 0)
            outline = (204, 204, 204)

        palette = {
            "primary":              cls._hex(accent),
            "on_primary":           "#FFFFFF" if cls._luminance(accent) < 0.5 else "#000000",
            "primary_container":    cls._hex(accent),
            "on_primary_container": "#FFFFFF" if cls._luminance(accent) < 0.5 else "#000000",
            "secondary":            cls._hex(accent),
            "on_secondary":         "#FFFFFF" if cls._luminance(accent) < 0.5 else "#000000",
            "secondary_container":  cls._hex(accent),
            "on_secondary_container": "#FFFFFF" if cls._luminance(accent) < 0.5 else "#000000",
            "surface":              cls._hex(surface),
            "on_surface":           cls._hex(on_surface),
            "surface_variant":      cls._hex(surface_variant),
            "on_surface_variant":   cls._hex(on_surface_variant),
            "background":           cls._hex(background),
            "on_background":        cls._hex(on_background),
            "outline":              cls._hex(outline),
            "outline_variant":      cls._hex(cls._mix(outline, surface, 0.5)),
            "error":                cls._hex(error),
            "on_error":             on_error,
            "shadow":               "rgba(0,0,0,0.12)",
            "sidebar_bg":           cls._hex(sidebar_bg),
            "sidebar_text":         cls._hex(sidebar_text),
            "sidebar_hover":        cls._hex(sidebar_hover),
            "sidebar_active":       cls._hex(sidebar_active),
            "sidebar_active_border": cls._hex(accent),
            "exit_btn_bg":          cls._hex(error),
            "exit_btn_hover":       cls._hex(cls._mix(error, (0, 0, 0), 0.15)),
        }
        palette.update(cls._QT_RADII)
        return palette

    # ============================================================
    #  WinUI3 / Fluent Design 调色板
    #  - 系统强调色（DWM Accent Color）驱动
    #  - 选中态 = AccentFillColorSecondary（半透明强调色）
    #  - 分层圆角：控件 4dp / 卡片 8dp / 导航 8dp
    #  - 中性色：SolidBackgroundFillColorBase / CardBackgroundFillColorDefault
    #  - 文本色：TextFillColorPrimary / TextFillColorSecondary
    #  - 字体：Segoe UI Variable（Win11 默认）
    # ============================================================
    @classmethod
    def _build_winui3_palette(cls, accent: tuple, dark: bool) -> dict:
        if dark:
            # WinUI3 Dark
            background = (32, 32, 32)         # SolidBackgroundFillColorBase
            surface = (45, 45, 45)            # CardBackgroundFillColorDefault
            on_surface = (255, 255, 255)      # TextFillColorPrimary
            surface_variant = (40, 40, 40)
            on_surface_variant = (197, 197, 197)  # TextFillColorSecondary
            outline = (63, 63, 63)            # DividerStroke
            sidebar_bg = (32, 32, 32)
            sidebar_text = (255, 255, 255)
            # hover: ControlFillColorSecondary
            sidebar_hover = cls._rgba(accent, 0.06)
            # 选中态: AccentFillColorSecondary (accent ~25% opacity)
            sidebar_active = cls._rgba(accent, 0.25)
            error = (255, 153, 164)           # SystemFillColorError
            on_error = (0, 0, 0)
        else:
            # WinUI3 Light
            background = (243, 243, 243)      # SolidBackgroundFillColorBase
            surface = (255, 255, 255)         # CardBackgroundFillColorDefault
            on_surface = (26, 26, 26)         # TextFillColorPrimary
            surface_variant = (249, 249, 249)
            on_surface_variant = (96, 96, 96) # TextFillColorSecondary
            outline = (210, 210, 210)         # DividerStroke
            sidebar_bg = (243, 243, 243)
            sidebar_text = (26, 26, 26)
            # hover
            sidebar_hover = cls._rgba(accent, 0.04)
            # 选中态
            sidebar_active = cls._rgba(accent, 0.15)
            error = (196, 43, 28)
            on_error = "#FFFFFF"

        on_accent = cls._on_color(accent)

        palette = {
            "primary":              cls._hex(accent),
            "on_primary":           on_accent,
            # 选中态背景 = AccentFillColorSecondary（主题色 ~60% 不透明度）
            "primary_container":    cls._rgba(accent, 0.6),
            "on_primary_container": on_accent,
            "secondary":            cls._hex(accent),
            "on_secondary":         on_accent,
            # hover 背景 (ControlFillColorSecondary)
            "secondary_container":  cls._rgba(accent, 0.04 if not dark else 0.06),
            "on_secondary_container": cls._hex(on_surface),
            "surface":              cls._hex(surface),
            "on_surface":           cls._hex(on_surface),
            "surface_variant":      cls._hex(surface_variant),
            "on_surface_variant":   cls._hex(on_surface_variant),
            "background":           cls._hex(background),
            "on_background":        cls._hex(on_surface),
            "outline":              cls._hex(outline),
            "outline_variant":      cls._hex(cls._mix(outline, surface, 0.5)),
            "error":                cls._hex(error),
            "on_error":             on_error,
            "shadow":               "rgba(0,0,0,0.12)",
            "sidebar_bg":           cls._hex(sidebar_bg),
            "sidebar_text":         cls._hex(sidebar_text),
            "sidebar_hover":        sidebar_hover,
            # 选中态 = AccentFillColorSecondary
            "sidebar_active":       cls._rgba(accent, 0.6),
            "sidebar_active_border": cls._hex(accent),
            "exit_btn_bg":          cls._hex(error),
            "exit_btn_hover":       cls._hex(cls._mix(error, (0, 0, 0), 0.15)),
        }
        palette.update(cls._WINUI3_RADII)
        return palette

    # ============================================================
    #  Win10 Fluent 早期调色板（2017-2021，无 Mica）
    #  - 材质：Acrylic（SetWindowCompositionAttribute + AccentState=4）
    #  - 字体：Segoe UI（静态，非 Variable）
    #  - 圆角：4dp（按钮/卡片）/ 8dp（对话框）
    #  - 选中态：左侧 4dp 实心主题色竖条 + 文字主题色，背景无色
    #  - 卡片：1dp 底线 #E5E5E5 + 0 1px 2px rgba(0,0,0,0.08)
    #  - 背景：浅=#FFF/#F2F2F2/#F9F9F9，暗=#1A1A1A/#2B2B2B
    #  - 无 container/tertiary 色系
    # ============================================================
    @classmethod
    def _build_win10fluent_palette(cls, accent: tuple, dark: bool) -> dict:
        if dark:
            background = (26, 26, 26)           # #1A1A1A
            surface = (43, 43, 43)              # #2B2B2B
            on_surface = (255, 255, 255)        # TextFillColorPrimary
            surface_variant = (43, 43, 43)
            on_surface_variant = (176, 176, 176) # #B0B0B0 TextFillColorSecondary
            outline = (59, 59, 59)              # #3B3B3B Divider
            sidebar_bg = (43, 43, 43)           # #2B2B2B Nav 背景
            sidebar_text = (255, 255, 255)
            sidebar_hover = "rgba(255,255,255,0.06)"
            sidebar_active = "transparent"
            error = (197, 15, 23)               # #C50F1F
            on_error = "#FFFFFF"
        else:
            background = (255, 255, 255)        # #FFFFFF Content 背景
            surface = (249, 249, 249)           # #F9F9F9
            on_surface = (50, 49, 48)           # #323130 TextFillColorPrimary
            surface_variant = (249, 249, 249)
            on_surface_variant = (96, 94, 92)   # #605E5C TextFillColorSecondary
            outline = (229, 229, 229)           # #E5E5E5 Divider
            sidebar_bg = (249, 249, 249)        # #F9F9F9 Nav 背景（比内容区略深）
            sidebar_text = (50, 49, 48)
            sidebar_hover = "rgba(0,0,0,0.04)"
            sidebar_active = "transparent"
            error = (197, 15, 23)               # #C50F1F
            on_error = "#FFFFFF"

        on_accent = cls._on_color(accent)

        palette = {
            "primary":              cls._hex(accent),
            "on_primary":           on_accent,
            "primary_container":    cls._hex(accent),
            "on_primary_container": on_accent,
            "secondary":            cls._hex(accent),
            "on_secondary":         on_accent,
            "secondary_container":  sidebar_hover,
            "on_secondary_container": cls._hex(on_surface),
            "surface":              cls._hex(surface),
            "on_surface":           cls._hex(on_surface),
            "surface_variant":      cls._hex(surface_variant),
            "on_surface_variant":   cls._hex(on_surface_variant),
            "background":           cls._hex(background),
            "on_background":        cls._hex(on_surface),
            "outline":              cls._hex(outline),
            "outline_variant":      cls._hex(outline),
            "error":                cls._hex(error),
            "on_error":             on_error,
            "shadow":               "rgba(0,0,0,0.08)",
            "sidebar_bg":           cls._hex(sidebar_bg),
            "sidebar_text":         cls._hex(sidebar_text),
            "sidebar_hover":        sidebar_hover,
            "sidebar_active":       sidebar_active,
            "sidebar_active_border": cls._hex(accent),
            "exit_btn_bg":          cls._hex(error),
            "exit_btn_hover":       cls._hex(cls._mix(error, (0, 0, 0), 0.15)),
        }
        palette.update(cls._WIN10FLUENT_RADII)
        return palette

    # ============================================================
    #  GNOME / libadwaita 调色板
    #  - 纯色背景（无 Mica/亚克力），暗色 #242424
    #  - 圆角：6dp（按钮）/ 12dp（卡片/对话框）
    #  - 选中态：强调色低透明度
    #  - hover：rgba(0,0,0,0.05) 浅 / rgba(255,255,255,0.05) 暗
    #  - 字体：Cantarell
    # ============================================================
    @classmethod
    def _build_gnome_palette(cls, accent: tuple, dark: bool) -> dict:
        if dark:
            background = (36, 36, 36)          # libadwaita dark
            surface = (48, 48, 48)             # card
            on_surface = (255, 255, 255)
            surface_variant = (42, 42, 42)
            on_surface_variant = (154, 154, 154)
            outline = (74, 74, 74)
            sidebar_bg = (36, 36, 36)
            sidebar_text = (255, 255, 255)
            sidebar_hover = "rgba(255,255,255,0.05)"
            sidebar_active = cls._rgba(accent, 0.2)
            error = (255, 123, 114)
            on_error = (0, 0, 0)
        else:
            background = (255, 255, 255)
            surface = (246, 245, 244)          # libadwaita light card
            on_surface = (29, 29, 29)
            surface_variant = (246, 245, 244)
            on_surface_variant = (93, 93, 93)
            outline = (220, 218, 216)
            sidebar_bg = (246, 245, 244)
            sidebar_text = (29, 29, 29)
            sidebar_hover = "rgba(0,0,0,0.05)"
            sidebar_active = cls._rgba(accent, 0.15)
            error = (192, 28, 40)
            on_error = "#FFFFFF"

        on_accent = cls._on_color(accent)

        palette = {
            "primary":              cls._hex(accent),
            "on_primary":           on_accent,
            "primary_container":    cls._rgba(accent, 0.15 if not dark else 0.2),
            "on_primary_container": cls._hex(accent),
            "secondary":            cls._hex(accent),
            "on_secondary":         on_accent,
            "secondary_container":  sidebar_hover,
            "on_secondary_container": cls._hex(on_surface),
            "surface":              cls._hex(surface),
            "on_surface":           cls._hex(on_surface),
            "surface_variant":      cls._hex(surface_variant),
            "on_surface_variant":   cls._hex(on_surface_variant),
            "background":           cls._hex(background),
            "on_background":        cls._hex(on_surface),
            "outline":              cls._hex(outline),
            "outline_variant":      cls._hex(cls._mix(outline, surface, 0.5)),
            "error":                cls._hex(error),
            "on_error":             on_error,
            "shadow":               "rgba(0,0,0,0.08)",
            "sidebar_bg":           cls._hex(sidebar_bg),
            "sidebar_text":         cls._hex(sidebar_text),
            "sidebar_hover":        sidebar_hover,
            "sidebar_active":       sidebar_active,
            "sidebar_active_border": cls._hex(accent),
            "exit_btn_bg":          cls._hex(error),
            "exit_btn_hover":       cls._hex(cls._mix(error, (0, 0, 0), 0.15)),
        }
        palette.update(cls._GNOME_RADII)
        return palette

    # ============================================================
    #  KDE Plasma / Breeze 调色板
    #  - 半透明面板：sidebar rgba(255,255,255,0.8) / rgba(0,0,0,0.7)
    #  - 圆角：4dp（按钮）/ 8dp（卡片）
    #  - 选中态：强调色半透明
    #  - 字体：Noto Sans / DejaVu Sans
    # ============================================================
    @classmethod
    def _build_kde_palette(cls, accent: tuple, dark: bool) -> dict:
        if dark:
            background = (49, 54, 59)          # Breeze Dark
            surface = (35, 38, 41)
            on_surface = (255, 255, 255)
            surface_variant = (44, 48, 51)
            on_surface_variant = (163, 165, 168)
            outline = (68, 72, 75)
            sidebar_bg = "rgba(35,38,41,0.8)"
            sidebar_text = (255, 255, 255)
            sidebar_hover = "rgba(255,255,255,0.06)"
            sidebar_active = cls._rgba(accent, 0.3)
            error = (218, 68, 83)
            on_error = "#FFFFFF"
        else:
            background = (239, 240, 241)       # Breeze Light
            surface = (252, 252, 252)
            on_surface = (41, 44, 49)
            surface_variant = (247, 247, 248)
            on_surface_variant = (93, 93, 93)
            outline = (198, 200, 203)
            sidebar_bg = "rgba(252,252,252,0.85)"
            sidebar_text = (41, 44, 49)
            sidebar_hover = "rgba(0,0,0,0.05)"
            sidebar_active = cls._rgba(accent, 0.2)
            error = (218, 68, 83)
            on_error = "#FFFFFF"

        on_accent = cls._on_color(accent)

        palette = {
            "primary":              cls._hex(accent),
            "on_primary":           on_accent,
            "primary_container":    cls._rgba(accent, 0.2 if not dark else 0.3),
            "on_primary_container": cls._hex(accent),
            "secondary":            cls._hex(accent),
            "on_secondary":         on_accent,
            "secondary_container":  sidebar_hover,
            "on_secondary_container": cls._hex(on_surface),
            "surface":              cls._hex(surface),
            "on_surface":           cls._hex(on_surface),
            "surface_variant":      cls._hex(surface_variant),
            "on_surface_variant":   cls._hex(on_surface_variant),
            "background":           cls._hex(background),
            "on_background":        cls._hex(on_surface),
            "outline":              cls._hex(outline),
            "outline_variant":      cls._hex(cls._mix(outline, surface, 0.5)),
            "error":                cls._hex(error),
            "on_error":             on_error,
            "shadow":               "rgba(0,0,0,0.1)",
            "sidebar_bg":           sidebar_bg,
            "sidebar_text":         cls._hex(sidebar_text),
            "sidebar_hover":        sidebar_hover,
            "sidebar_active":       sidebar_active,
            "sidebar_active_border": cls._hex(accent),
            "exit_btn_bg":          cls._hex(error),
            "exit_btn_hover":       cls._hex(cls._mix(error, (0, 0, 0), 0.15)),
        }
        palette.update(cls._KDE_RADII)
        return palette

    # ============================================================
    #  macOS / Cupertino 调色板
    #  - 选中态：实心强调色填充（非半透明）
    #  - 圆角：8dp（按钮）/ 12dp（卡片/侧边栏）
    #  - 暗色 #1e1e1e，卡片 #2d2d2d
    #  - 字体：SF Pro / Helvetica Neue
    # ============================================================
    @classmethod
    def _build_cupertino_palette(cls, accent: tuple, dark: bool) -> dict:
        if dark:
            background = (30, 30, 30)          # macOS dark
            surface = (45, 45, 45)             # card
            on_surface = (255, 255, 255)
            surface_variant = (40, 40, 40)
            on_surface_variant = (152, 152, 157)
            outline = (70, 70, 70)
            sidebar_bg = (38, 38, 38)
            sidebar_text = (255, 255, 255)
            sidebar_hover = "rgba(255,255,255,0.06)"
            # macOS 选中态：实心强调色
            sidebar_active = cls._hex(accent)
            error = (255, 95, 87)
            on_error = "#000000"
        else:
            background = (255, 255, 255)
            surface = (245, 245, 247)          # macOS card
            on_surface = (29, 29, 31)
            surface_variant = (242, 242, 247)
            on_surface_variant = (134, 134, 139)
            outline = (206, 206, 210)
            sidebar_bg = (242, 242, 247)
            sidebar_text = (29, 29, 31)
            sidebar_hover = "rgba(0,0,0,0.05)"
            sidebar_active = cls._hex(accent)
            error = (215, 0, 21)
            on_error = "#FFFFFF"

        on_accent = cls._on_color(accent)

        palette = {
            "primary":              cls._hex(accent),
            "on_primary":           on_accent,
            # macOS 选中态用实心强调色
            "primary_container":    cls._hex(accent),
            "on_primary_container": on_accent,
            "secondary":            cls._hex(accent),
            "on_secondary":         on_accent,
            "secondary_container":  sidebar_hover,
            "on_secondary_container": cls._hex(on_surface),
            "surface":              cls._hex(surface),
            "on_surface":           cls._hex(on_surface),
            "surface_variant":      cls._hex(surface_variant),
            "on_surface_variant":   cls._hex(on_surface_variant),
            "background":           cls._hex(background),
            "on_background":        cls._hex(on_surface),
            "outline":              cls._hex(outline),
            "outline_variant":      cls._hex(cls._mix(outline, surface, 0.5)),
            "error":                cls._hex(error),
            "on_error":             on_error,
            "shadow":               "rgba(0,0,0,0.1)",
            "sidebar_bg":           cls._hex(sidebar_bg),
            "sidebar_text":         cls._hex(sidebar_text),
            "sidebar_hover":        sidebar_hover,
            "sidebar_active":       sidebar_active,
            "sidebar_active_border": cls._hex(accent),
            "exit_btn_bg":          cls._hex(error),
            "exit_btn_hover":       cls._hex(cls._mix(error, (0, 0, 0), 0.15)),
        }
        palette.update(cls._CUPERTINO_RADII)
        return palette

    # ============================================================
    #  ChromeOS / Material Desktop 调色板
    #  - Google Sans 字体
    #  - 圆角：8dp（按钮）/ 12dp（卡片）
    #  - 暗色 #202124，卡片 #292a2d
    #  - 选中态：半透明强调色
    # ============================================================
    @classmethod
    def _build_chromeos_palette(cls, accent: tuple, dark: bool) -> dict:
        if dark:
            background = (32, 33, 36)          # ChromeOS dark
            surface = (41, 42, 45)             # card
            on_surface = (255, 255, 255)
            surface_variant = (38, 39, 42)
            on_surface_variant = (154, 160, 166)
            outline = (63, 64, 67)
            sidebar_bg = (32, 33, 36)
            sidebar_text = (255, 255, 255)
            sidebar_hover = "rgba(255,255,255,0.05)"
            sidebar_active = cls._rgba(accent, 0.25)
            error = (242, 139, 130)
            on_error = "#000000"
        else:
            background = (241, 243, 244)       # ChromeOS light
            surface = (255, 255, 255)          # card
            on_surface = (32, 33, 36)
            surface_variant = (248, 249, 250)
            on_surface_variant = (95, 99, 104)
            outline = (218, 220, 224)
            sidebar_bg = (241, 243, 244)
            sidebar_text = (32, 33, 36)
            sidebar_hover = "rgba(0,0,0,0.05)"
            sidebar_active = cls._rgba(accent, 0.15)
            error = (197, 34, 31)
            on_error = "#FFFFFF"

        on_accent = cls._on_color(accent)

        palette = {
            "primary":              cls._hex(accent),
            "on_primary":           on_accent,
            "primary_container":    cls._rgba(accent, 0.15 if not dark else 0.25),
            "on_primary_container": cls._hex(accent),
            "secondary":            cls._hex(accent),
            "on_secondary":         on_accent,
            "secondary_container":  sidebar_hover,
            "on_secondary_container": cls._hex(on_surface),
            "surface":              cls._hex(surface),
            "on_surface":           cls._hex(on_surface),
            "surface_variant":      cls._hex(surface_variant),
            "on_surface_variant":   cls._hex(on_surface_variant),
            "background":           cls._hex(background),
            "on_background":        cls._hex(on_surface),
            "outline":              cls._hex(outline),
            "outline_variant":      cls._hex(cls._mix(outline, surface, 0.5)),
            "error":                cls._hex(error),
            "on_error":             on_error,
            "shadow":               "rgba(0,0,0,0.1)",
            "sidebar_bg":           cls._hex(sidebar_bg),
            "sidebar_text":         cls._hex(sidebar_text),
            "sidebar_hover":        sidebar_hover,
            "sidebar_active":       sidebar_active,
            "sidebar_active_border": cls._hex(accent),
            "exit_btn_bg":          cls._hex(error),
            "exit_btn_hover":       cls._hex(cls._mix(error, (0, 0, 0), 0.15)),
        }
        palette.update(cls._CHROMEOS_RADII)
        return palette


theme = ThemeManager()
