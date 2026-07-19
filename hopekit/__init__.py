"""
HopeKit — PySide6 桌面应用脚手架核心包（Web UI 重构版）

子模块：
- qt_compat: PySide6 单绑定 + QWebEngine 集成
- paths: 资源/配置路径处理
- theme: 多风格主题管理（md3/md2/qt/winui3/win10fluent/gnome/kde/cupertino/chromeos）
- registry: 模块注册器 + 实例缓存
- web_ui: WebUIHost — QWebEngineView 宿主
- web_bridge: PythonBridge — QWebChannel 桥接对象
- main_window: MainUi — Web UI 宿主主窗口
- settings_dialog: 旧版设置对话框（保留兼容）
"""

from hopekit import qt_compat
from hopekit.paths import resource_path, config_path
from hopekit.theme import theme, ThemeManager
from hopekit.registry import ModuleRegistry, discover_plugins
from hopekit.settings_dialog import SettingsDialog
from hopekit.web_ui import WebUIHost
from hopekit.web_bridge import PythonBridge
from hopekit.main_window import MainUi
from hopekit.version import VERSION

__version__ = VERSION

__all__ = [
    "qt_compat",
    "resource_path",
    "config_path",
    "theme",
    "ThemeManager",
    "ModuleRegistry",
    "discover_plugins",
    "SettingsDialog",
    "WebUIHost",
    "PythonBridge",
    "MainUi",
    "__version__",
]
