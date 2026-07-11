"""
ThemeManager — 多风格主题管理器

风格 (style): md3 / md2 / windows
模式 (mode):  auto / light / dark

- md3: Material Design 3，动态强调色 + 大圆角 + 分层 container
- md2: Material Design 2，Blue 500 主色 + 扁平化 + 阴影 + 4px 圆角
- windows: Windows 原生风格，最小样式覆盖，跟随系统色

持久化到本地 JSON。
"""

import json

from hopekit.paths import config_path


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

    _WINDOWS_RADII = {
        "card_radius": "0px",
        "btn_radius":  "0px",
        "nav_radius":  "0px",
    }

    def __init__(self):
        self._style = "md3"
        self._mode = "auto"
        self.load()

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
        if self._style == "windows":
            return self._build_windows_palette(accent, self.is_dark)
        return self._build_md3_palette(accent, self.is_dark)

    def set_style(self, style: str):
        if style in ("md3", "md2", "windows"):
            self._style = style
            self.save()

    def set_mode(self, mode: str):
        if mode in ("auto", "light", "dark"):
            self._mode = mode
            self.save()

    def load(self):
        try:
            with open(self._CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data.get("style") in ("md3", "md2", "windows"):
                self._style = data["style"]
            if data.get("mode") in ("auto", "light", "dark"):
                self._mode = data["mode"]
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            pass

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
            "error":                cls._hex(error),
            "on_error":             cls._hex(on_error),
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
    #  MD2 调色板（Material Design 2 — Blue 500 主色 + 扁平化 + 阴影）
    # ============================================================
    @classmethod
    def _build_md2_palette(cls, accent: tuple, dark: bool) -> dict:
        if dark:
            primary = (100, 181, 246)      # Blue 300
            primary_dark = (66, 165, 245)   # Blue 400
            primary_light = (144, 202, 249) # Blue 200
            surface = (66, 66, 66)          # Grey 800
            on_surface = (250, 250, 250)    # Grey 50
            surface_variant = (97, 97, 97)  # Grey 700
            on_surface_variant = (224, 224, 224)  # Grey 300
            background = (48, 48, 48)       # Grey 850
            on_background = (250, 250, 250)
            outline = (158, 158, 158)       # Grey 500
            sidebar_bg = (55, 55, 55)
            sidebar_text = (245, 245, 245)
            sidebar_hover = (80, 80, 80)
            sidebar_active = (100, 181, 246)
            accent_color = (255, 82, 82)    # Red A200
            error = (239, 83, 80)           # Red A200 alt
            on_error = "#FFFFFF"
        else:
            primary = accent if accent != (103, 80, 164) else (33, 150, 243)
            primary_dark = cls._mix(primary, (0, 0, 0), 0.2)
            primary_light = cls._mix(primary, (255, 255, 255), 0.3)
            surface = (255, 255, 255)       # White
            on_surface = (33, 33, 33)       # Grey 900
            surface_variant = (245, 245, 245)  # Grey 100
            on_surface_variant = (117, 117, 117)  # Grey 600
            background = (250, 250, 250)    # Grey 50
            on_background = (33, 33, 33)
            outline = (189, 189, 189)       # Grey 400
            sidebar_bg = (250, 250, 250)
            sidebar_text = (33, 33, 33)
            sidebar_hover = (238, 238, 238) # Grey 200
            sidebar_active = (224, 224, 224)  # Grey 300
            accent_color = (255, 82, 82)    # Red A200
            error = (211, 47, 47)           # Red 600
            on_error = "#FFFFFF"

        on_primary = cls._on_color(primary)
        on_secondary = on_primary

        palette = {
            "primary":              cls._hex(primary),
            "primary_dark":         cls._hex(primary_dark),
            "primary_light":        cls._hex(primary_light),
            "on_primary":           on_primary,
            "primary_container":    cls._hex(primary_light),
            "on_primary_container": cls._hex(on_surface),
            "secondary":            cls._hex(primary),
            "on_secondary":         on_secondary,
            "secondary_container":  cls._hex(primary_light),
            "on_secondary_container": cls._hex(on_surface),
            "surface":              cls._hex(surface),
            "on_surface":           cls._hex(on_surface),
            "surface_variant":      cls._hex(surface_variant),
            "on_surface_variant":   cls._hex(on_surface_variant),
            "background":           cls._hex(background),
            "on_background":        cls._hex(on_background),
            "outline":              cls._hex(outline),
            "error":                cls._hex(error),
            "on_error":             on_error,
            "shadow":               "rgba(0,0,0,0.24)",
            "divider":              cls._hex(outline),
            "sidebar_bg":           cls._hex(sidebar_bg),
            "sidebar_text":         cls._hex(sidebar_text),
            "sidebar_hover":        cls._hex(sidebar_hover),
            "sidebar_active":       cls._hex(sidebar_active),
            "sidebar_active_border": cls._hex(primary),
            "exit_btn_bg":          cls._hex(accent_color),
            "exit_btn_hover":       cls._hex(cls._mix(accent_color, (0, 0, 0), 0.15)),
        }
        palette.update(cls._MD2_RADII)
        return palette

    # ============================================================
    #  Windows 原生风格调色板
    #  尽量少改 Qt 原生控件外观，只统一背景/文字/强调色，让系统风格透出来
    # ============================================================
    @classmethod
    def _build_windows_palette(cls, accent: tuple, dark: bool) -> dict:
        if dark:
            window = (32, 32, 32)          # 近似 Windows 深色背景
            window_text = (255, 255, 255)
            btn_face = (45, 45, 45)
            btn_text = (255, 255, 255)
            highlight = accent
            highlight_text = (255, 255, 255)
            gray_text = (166, 166, 166)
            surface = (45, 45, 45)
            on_surface = (255, 255, 255)
            background = (32, 32, 32)
            on_background = (255, 255, 255)
            outline = (85, 85, 85)
            sidebar_bg = (28, 28, 28)
            sidebar_text = (255, 255, 255)
            sidebar_hover = (51, 51, 51)
            sidebar_active = cls._mix(accent, (51, 51, 51), 0.5)
            error = (202, 54, 54)
            on_error = "#FFFFFF"
        else:
            window = (255, 255, 255)
            window_text = (0, 0, 0)
            btn_face = (240, 240, 240)
            btn_text = (0, 0, 0)
            highlight = accent
            highlight_text = "#FFFFFF" if cls._luminance(accent) < 0.5 else "#000000"
            gray_text = (109, 109, 109)
            surface = (255, 255, 255)
            on_surface = (0, 0, 0)
            background = (243, 243, 243)
            on_background = (0, 0, 0)
            outline = (204, 204, 204)
            sidebar_bg = (245, 246, 247)
            sidebar_text = (0, 0, 0)
            sidebar_hover = (229, 229, 229)
            sidebar_active = cls._mix(accent, (229, 229, 229), 0.4)
            error = (196, 43, 43)
            on_error = "#FFFFFF"

        palette = {
            "primary":              cls._hex(accent),
            "on_primary":           highlight_text,
            "primary_container":    cls._hex(btn_face),
            "on_primary_container": cls._hex(window_text),
            "secondary":            cls._hex(accent),
            "on_secondary":         highlight_text,
            "secondary_container":  cls._hex(btn_face),
            "on_secondary_container": cls._hex(window_text),
            "surface":              cls._hex(surface),
            "on_surface":           cls._hex(on_surface),
            "surface_variant":      cls._hex(btn_face),
            "on_surface_variant":   cls._hex(gray_text),
            "background":           cls._hex(background),
            "on_background":        cls._hex(on_background),
            "outline":              cls._hex(outline),
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
            "btn_face":             cls._hex(btn_face),
            "btn_text":             cls._hex(btn_text),
        }
        palette.update(cls._WINDOWS_RADII)
        return palette


theme = ThemeManager()
