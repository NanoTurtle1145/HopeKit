"""
路径处理 — 兼容 PyInstaller 打包
"""

import os
import sys


def resource_path(relative: str) -> str:
    """只读资源路径（logo 等），打包后从 _MEIPASS 解压目录加载。"""
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS  # type: ignore[attr-defined]
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative)


def config_path(filename: str) -> str:
    """可读写配置文件路径（theme.json），放在 exe 同目录便于持久化。"""
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, filename)
