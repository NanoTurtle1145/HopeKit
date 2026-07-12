"""
Transparency Manager — 窗口透明效果模块化管理

统一处理 Qt 窗口属性和 DWM 材质的交互：
  - WA_TranslucentBackground（必须在 show() 前设置）
  - WA_NoSystemBackground + WA_StyledBackground（central widget）
  - DWM 材质应用（Mica/Acrylic）
  - 材质清除和窗口恢复

支持的主题：
  - winui3: Win11 Mica / Win10 Acrylic
  - win10fluent: Win10 Acrylic（无 Mica）
"""

import sys
from hopekit.qt_compat import QtCore
from hopekit.theme import theme


def is_transparent_theme() -> bool:
    """判断当前主题是否需要透明效果"""
    return theme.style in ("winui3", "win10fluent")


def enable_transparency_before_show(window):
    """
    在窗口 show() 之前调用，设置 WA_TranslucentBackground。
    
    Qt6.6+ 的 WA_TranslucentBackground 会强制走 WS_EX_LAYERED，
    这是 Win10 Acrylic 老路径正常工作的前提。
    
    注意：不要同时给窗口设 QSS background: transparent，会冲突。
    """
    if not is_transparent_theme():
        return
    
    try:
        window.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True
        )
    except (AttributeError, TypeError):
        pass


def enable_transparency_for_central(central_widget):
    """
    给 central widget 设置透明属性。
    
    WA_NoSystemBackground 禁止 Qt 自动填色，
    WA_StyledBackground 允许 QSS 样式生效。
    
    注意：不要给 central 设 QSS background: transparent，
    会与 WA_TranslucentBackground 冲突。
    """
    if not is_transparent_theme():
        return
    
    try:
        central_widget.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_NoSystemBackground, True
        )
        central_widget.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_StyledBackground, True
        )
    except (AttributeError, TypeError):
        pass


def apply_backdrop_to_window(window, kind: str = "acrylic") -> bool:
    """
    在窗口 showEvent 中调用，应用 DWM 材质。
    
    根据主题和系统版本自动选择材质类型：
      - win10fluent: 始终用 Acrylic
      - winui3: Win11 22621+ Mica，否则 Acrylic
    
    Args:
        window: QMainWindow / QWidget 实例
        kind: 材质类型（"mica" / "acrylic"），为 None 时自动选择
    
    Returns:
        是否成功应用材质
    """
    if not is_transparent_theme():
        return False
    
    if not sys.platform == "win32":
        return False
    
    try:
        from hopekit import mica
    except ImportError:
        return False
    
    try:
        hwnd = int(window.winId())
    except (AttributeError, TypeError):
        return False
    
    if hwnd == 0:
        return False
    
    if kind is None:
        if theme.style == "win10fluent":
            kind = "acrylic"
        else:
            build = mica.get_windows_build()
            kind = "mica" if build >= 22621 else "acrylic"
    
    ok, msg = mica.apply_backdrop(hwnd, kind=kind, dark=theme.is_dark)
    
    if ok:
        print(f"[{theme.style}] {kind}: {ok}, {msg}", flush=True)
    else:
        print(f"[{theme.style}] 材质失败: {msg}", flush=True)
        disable_transparency(window)
    
    return ok


def disable_transparency(window):
    """
    禁用透明效果，恢复不透明状态。
    
    用于：
      - 材质应用失败时降级
      - 主题切换到非透明主题时
    """
    try:
        window.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, False
        )
    except (AttributeError, TypeError):
        pass
    
    central = getattr(window, "centralWidget", lambda: None)()
    if central:
        try:
            central.setAttribute(
                QtCore.Qt.WidgetAttribute.WA_NoSystemBackground, False
            )
        except (AttributeError, TypeError):
            pass
    
    try:
        from hopekit import mica
        hwnd = int(window.winId())
        if hwnd != 0:
            mica.apply_backdrop(hwnd, kind="none")
    except (ImportError, AttributeError, TypeError):
        pass
