"""
ThemeManager — Material Design 3 主题管理器
跟随 Windows 强调色 + 深浅色模式 + 持久化
"""

import json

from hopekit.paths import config_path


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

    _RADII = {
        "card_radius": "16px",
        "btn_radius":  "20px",
        "nav_radius":  "28px",
    }

    def __init__(self):
        self._mode = "auto"
        self.load()

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
        return self._build_palette(accent, self.is_dark)

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
            return (103, 80, 164)

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

    @classmethod
    def _build_palette(cls, accent: tuple, dark: bool) -> dict:
        r, g, b = accent

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


theme = ThemeManager()
