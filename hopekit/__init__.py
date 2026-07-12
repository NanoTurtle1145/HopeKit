"""
HopeKit — PyQt 桌面应用脚手架核心包

子模块：
- qt_compat: PySide6 / PyQt6 兼容层
- paths: 资源/配置路径处理
- theme: MD3/MD2/Qt 原生主题管理
- registry: 模块注册器 + 实例缓存
- settings_dialog: 设置对话框
- main_window: 主窗口
"""

from hopekit import qt_compat
from hopekit.paths import resource_path, config_path
from hopekit.theme import theme, ThemeManager
from hopekit.registry import ModuleRegistry, discover_plugins
from hopekit.settings_dialog import SettingsDialog
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
    "MainUi",
    "__version__",
]
