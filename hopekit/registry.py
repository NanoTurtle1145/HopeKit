"""
ModuleRegistry — 插件注册器 + 实例缓存

加模块 = 写一个装饰器，主文件零修改。

两种模式：
  - kind="window"（默认）：factory 返回 QDialog/QMainWindow，点击按钮弹出，关闭后复用实例
  - kind="page"：factory 返回 QWidget，直接嵌入 StackedWidget 页面

用法:
    from hopekit.registry import ModuleRegistry

    # 弹窗型
    @ModuleRegistry.register("my_tool", icon="🔧", title="我的工具", category="tools")
    def my_tool_factory(main_window):
        from my_module import MyDialog
        return MyDialog()

    # 页面型（嵌入主区域）
    @ModuleRegistry.register("my_page", icon="📊", title="面板", category="dashboard", kind="page")
    def my_page_factory(main_window):
        from my_module import MyPanel
        return MyPanel()
"""

import importlib
import os
import sys
from typing import Callable, Dict, List, Optional


class ModuleRegistry:
    """全局模块注册表，装饰器式注册 + 实例缓存。"""

    _modules: Dict[str, dict] = {}
    _categories: List[str] = []
    _instances: Dict[str, object] = {}

    @classmethod
    def register(
        cls,
        name: str,
        icon: str = "📦",
        title: str = "",
        description: str = "",
        category: str = "tools",
        kind: str = "window",
        enabled: bool = True,
    ):
        """
        装饰器：注册一个模块。

        Args:
            name: 唯一标识
            icon: 按钮图标（emoji 或文字）
            title: 按钮显示文本（默认等于 name）
            description: 模块描述（卡片副标题，可为空）
            category: 所属分类（tools / links / 自定义）
            kind: "window"（弹窗）或 "page"（嵌入主区域）
            enabled: 是否启用（False 则按钮置灰）
        """
        def decorator(factory: Callable) -> Callable:
            cls._modules[name] = {
                "icon": icon,
                "title": title or name,
                "description": description,
                "category": category,
                "kind": kind,
                "factory": factory,
                "enabled": enabled,
            }
            if category not in cls._categories:
                cls._categories.append(category)
            return factory
        return decorator

    @classmethod
    def all(cls) -> Dict[str, dict]:
        """返回所有注册的模块。"""
        return dict(cls._modules)

    @classmethod
    def by_category(cls, category: str) -> Dict[str, dict]:
        """返回指定分类下的所有模块。"""
        return {
            name: info
            for name, info in cls._modules.items()
            if info["category"] == category
        }

    @classmethod
    def categories(cls) -> List[str]:
        """返回所有分类名（按注册顺序）。"""
        return list(cls._categories)

    @classmethod
    def get(cls, name: str) -> Optional[dict]:
        """根据 name 获取模块元信息。"""
        return cls._modules.get(name)

    @classmethod
    def set_enabled(cls, name: str, enabled: bool):
        """设置模块启用状态。"""
        if name in cls._modules:
            cls._modules[name]["enabled"] = enabled

    @classmethod
    def get_or_create(cls, name: str, main_window=None):
        """
        获取或创建模块实例（带缓存）。

        - 首次调用：执行 factory 创建实例并缓存
        - 后续调用：返回已缓存的实例
        - 实例被 Qt 析构后（C++ 对象删除）：自动重建

        Returns:
            模块实例（QWidget），或 None（模块不存在/未启用/factory 返回 None）
        """
        info = cls._modules.get(name)
        if not info or not info["enabled"]:
            return None

        cached = cls._instances.get(name)
        if cached is not None:
            try:
                # 检查底层 C++ 对象是否还活着
                cached.isVisible()
                return cached
            except RuntimeError:
                # 对象已被 Qt 析构，重建
                del cls._instances[name]

        try:
            instance = info["factory"](main_window)
        except Exception as e:
            print(f"[ERROR] Failed to create module '{name}': {e}", file=sys.stderr)
            return None

        if instance is not None:
            cls._instances[name] = instance
        return instance

    @classmethod
    def get_instance(cls, name: str):
        """返回已缓存的实例（不创建），不存在返回 None。"""
        return cls._instances.get(name)

    @classmethod
    def clear_instances(cls):
        """清空实例缓存（切换主题等需要重建时用）。"""
        cls._instances.clear()

    @classmethod
    def clear(cls):
        """清空注册表 + 实例（测试用）。"""
        cls._modules.clear()
        cls._categories.clear()
        cls._instances.clear()


# PyInstaller 打包时 plugins/ 目录可能不存在，兜底用 hardcoded 列表
_FROZEN_PLUGINS = [
    "plugins.caidan",
    "plugins.calculator",
    "plugins.calendar",
    "plugins.chat_room_plugin",
    "plugins.copyright",
    "plugins.links",
    "plugins.shit_window",
    "plugins.shutdown",
]


def discover_plugins(plugins_dir: str = "plugins") -> int:
    """
    自动扫描 plugins/ 目录，import 所有 .py 文件，触发装饰器注册。

    支持两种模式：
      - 开发/PyInstaller+datas：通过 os.listdir 扫描目录
      - PyInstaller frozen（目录不存在）：回退到 _FROZEN_PLUGINS 硬编码列表

    Returns:
        加载的插件模块数量
    """
    count = 0
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    plugins_path = os.path.join(base_dir, plugins_dir)

    if os.path.isdir(plugins_path):
        # 开发模式 / PyInstaller 已将 plugins/ 作为 data 目录
        if plugins_path not in sys.path:
            sys.path.insert(0, base_dir)
        for filename in sorted(os.listdir(plugins_path)):
            if filename.startswith("_") or not filename.endswith(".py"):
                continue
            module_name = f"{plugins_dir}.{filename[:-3]}"
            try:
                importlib.import_module(module_name)
                count += 1
            except Exception as e:
                print(f"[WARN] Failed to load plugin {module_name}: {e}", file=sys.stderr)
    else:
        # PyInstaller frozen：目录不存在，回退到硬编码列表
        print(f"[discover] plugins/ 目录不存在，使用 frozen 兜底列表", flush=True)
        for module_name in _FROZEN_PLUGINS:
            try:
                importlib.import_module(module_name)
                count += 1
            except Exception as e:
                print(f"[WARN] Failed to load plugin {module_name}: {e}", file=sys.stderr)

    return count
