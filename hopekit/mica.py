"""
Backdrop 材质管理 — Mica / Acrylic 统一入口

材质分工（WinUI3 规范）:
  - Mica    → 主窗口背景，模糊桌面壁纸（DWMSBT_MAINWINDOW=2）
  - Acrylic → 弹窗/Flyout/Toast 背景，模糊应用后方内容（DWMSBT_TRANSIENT=3）
  - Smoke   → 模态遮罩 rgba(0,0,0,0.3)，纯 QSS

系统版本路径:
  Win11 22621+:  DWMWA_SYSTEMBACKDROP_TYPE=38 (Mica=2 / Acrylic=3 / MicaAlt=4)
  Win11 22000+:  DWMWA_MICA=1029 (仅 default Mica)
  Win10/21H2:    SetWindowCompositionAttribute + ACCENT_ENABLE_ACRYLICBLURBEHIND=5 (仅 Acrylic)
  Win10 早期:    纯色降级
"""

import sys
import ctypes
import platform
from ctypes.wintypes import DWORD, HWND, INT, BOOL


# ============================================================
#  DWM 常量（新路径，Win11 22621+）
# ============================================================
_DWMWA_USE_IMMERSIVE_DARK_MODE = 20
_DWMWA_SYSTEMBACKDROP_TYPE = 38
_DWMWA_MICA = 1029  # Win11 22000+ 老接口

# DWMSBT 枚举
_DWMSBT_AUTO = 0
_DWMSBT_NONE = 1
_DWMSBT_MAINWINDOW = 2   # Mica
_DWMSBT_TRANSIENT = 3     # Acrylic
_DWMSBT_TABBED = 4        # MicaAlt

# ============================================================
#  SetWindowCompositionAttribute 常量（老路径，Win10/21H2）
# ============================================================
_WCA_ACCENT_POLICY = 19

# ACCENT_STATE
_ACCENT_DISABLED = 0
_ACCENT_ENABLE_GRADIENT = 1
_ACCENT_ENABLE_TRANSPARENTGRADIENT = 2
_ACCENT_ENABLE_BLURBEHIND = 3
_ACCENT_ENABLE_ACRYLICBLURBEHIND = 4  # Win10 1803+ / 19045
_ACCENT_ENABLE_ACRYLICBLURBEHIND_ALT = 5  # 某些版本用 5


class _AccentPolicy(ctypes.Structure):
    _fields_ = [
        ("AccentState", INT),
        ("AccentFlags", INT),
        ("GradientColor", DWORD),  # ARGB，A 在高字节
        ("AnimationId", INT),
    ]


class _WinCompAttrData(ctypes.Structure):
    _fields_ = [
        ("attrib", INT),
        ("pvData", ctypes.POINTER(_AccentPolicy)),
        ("cbData", ctypes.c_size_t),
    ]


class _MARGINS(ctypes.Structure):
    """DwmExtendFrameIntoClientArea 的 margin 参数"""
    _fields_ = [
        ("cxLeftWidth", INT),
        ("cxRightWidth", INT),
        ("cyTopHeight", INT),
        ("cyBottomHeight", INT),
    ]


# ============================================================
#  工具函数
# ============================================================
def _is_windows() -> bool:
    return sys.platform == "win32"


def get_windows_build() -> int:
    """返回 Windows NT build number，如 22631。非 Windows 返回 0。"""
    if not _is_windows():
        return 0
    try:
        ver = platform.win32_ver()[1]  # e.g. "10.0.22631"
        return int(ver.split('.')[-1])
    except Exception:
        return 0


def _get_dwmapi():
    if not _is_windows():
        return None
    try:
        return ctypes.windll.dwmapi
    except (AttributeError, OSError):
        return None


def _get_user32():
    if not _is_windows():
        return None
    try:
        return ctypes.windll.user32
    except (AttributeError, OSError):
        return None


def _argb(a: int, r: int, g: int, b: int) -> int:
    """生成 ARGB 值（A 在高字节）：0xAARRGGBB"""
    return (a << 24) | (r << 16) | (g << 8) | b


def _extend_frame(hwnd: int, fully: bool = True) -> bool:
    """
    调用 DwmExtendFrameIntoClientArea 扩展 DWM frame。

    fully=True  → margins={-1,-1,-1,-1}，整个客户区都是 frame
    fully=False → margins={0,0,0,0}，恢复默认（不扩展）

    这是 Win10 Acrylic 正常工作的前提：
      - 不扩展 frame 时，Acrylic 效果会溢出窗口边界
      - 扩展后，Acrylic 被裁剪到窗口可视区域内
    """
    dwm = _get_dwmapi()
    if dwm is None:
        return False
    margins = _MARGINS(-1, -1, -1, -1) if fully else _MARGINS(0, 0, 0, 0)
    try:
        dwm.DwmExtendFrameIntoClientArea(HWND(hwnd), ctypes.byref(margins))
        return True
    except Exception:
        return False


# ============================================================
#  DWM 新路径（Win11 22621+）
# ============================================================
def _dwm_set_backdrop(hwnd: int, backdrop_type: int) -> tuple:
    """通过 DWMWA_SYSTEMBACKDROP_TYPE=38 设置材质（Win11 22621+）"""
    dwm = _get_dwmapi()
    if dwm is None:
        return False, "非 Windows 系统"

    build = get_windows_build()
    if build < 22621:
        return False, f"build {build} < 22621，attr=38 不支持"

    val = DWORD(backdrop_type)
    try:
        res = dwm.DwmSetWindowAttribute(
            HWND(hwnd), _DWMWA_SYSTEMBACKDROP_TYPE,
            ctypes.byref(val), ctypes.sizeof(val),
        )
        if res == 0:
            return True, f"backdrop={backdrop_type} via SYSTEMBACKDROP_TYPE(38)"
        return False, f"DwmSetWindowAttribute(38) 返回 0x{res & 0xFFFFFFFF:08X}"
    except Exception as e:
        return False, f"异常: {e}"


# ============================================================
#  DWM 老路径 Mica（Win11 22000~22620）
# ============================================================
def _dwm_legacy_mica(hwnd: int) -> tuple:
    """Win11 22000+ 老接口 DWMWA_MICA=1029（仅 default Mica）"""
    dwm = _get_dwmapi()
    if dwm is None:
        return False, "非 Windows 系统"

    val = DWORD(1)  # 1=enable
    try:
        res = dwm.DwmSetWindowAttribute(
            HWND(hwnd), _DWMWA_MICA,
            ctypes.byref(val), ctypes.sizeof(val),
        )
        if res == 0:
            return True, "Mica(default) via legacy DWMWA_MICA(1029)"
        return False, f"legacy MICA(1029) 返回 0x{res & 0xFFFFFFFF:08X}"
    except Exception as e:
        return False, f"异常: {e}"


# ============================================================
#  SetWindowCompositionAttribute 老路径 Acrylic（Win10/21H2）
# ============================================================
def _set_acrylic_legacy_internal(hwnd: int, accent_state: int,
                                 base_rgb: tuple, opacity: int) -> tuple:
    """内部方法：调用 SetWindowCompositionAttribute 设置指定的 accent state"""
    user32 = _get_user32()
    if user32 is None:
        return False, "非 Windows 系统"

    try:
        setwca = user32.SetWindowCompositionAttribute
        setwca.argtypes = [HWND, ctypes.POINTER(_WinCompAttrData)]
        setwca.restype = BOOL
    except AttributeError:
        return False, "user32.SetWindowCompositionAttribute 不存在"

    a = int(opacity * 255 / 100)
    grad = _argb(a, *base_rgb)

    # AccentFlags = 2 表示全窗口应用（左/右/上/下边界都启用）
    policy = _AccentPolicy(
        AccentState=accent_state,
        AccentFlags=2,
        GradientColor=grad,
        AnimationId=0,
    )
    data = _WinCompAttrData(
        attrib=_WCA_ACCENT_POLICY,
        pvData=ctypes.pointer(policy),
        cbData=ctypes.sizeof(policy),
    )

    try:
        ok = setwca(HWND(hwnd), ctypes.byref(data))
        if ok:
            return True, f"state={accent_state} base={base_rgb} opacity={opacity}%"
        return False, f"SetWindowCompositionAttribute(state={accent_state}) 返回 False"
    except Exception as e:
        return False, f"异常(state={accent_state}): {e}"


def _set_acrylic_legacy(hwnd: int, base_rgb: tuple, opacity: int) -> tuple:
    """
    Win10 / Win11 21H2 老路径：SetWindowCompositionAttribute + Acrylic

    自动尝试 state=4（标准）和 state=5（备用），哪个成功用哪个。
    AccentFlags=2 确保全窗口应用效果。

    Args:
        hwnd: 窗口句柄
        base_rgb: 基色 (R, G, B)，浅色 (255,255,255) / 深色 (0,0,0)
        opacity: 基色不透明度 0-100，浅色建议 70，深色建议 85
    """
    # 先试 state=4（Win10 1803+ 标准值）
    ok, msg = _set_acrylic_legacy_internal(
        hwnd, _ACCENT_ENABLE_ACRYLICBLURBEHIND, base_rgb, opacity
    )
    if ok:
        return True, f"Acrylic(Win10 legacy) {msg}"

    # 失败则试 state=5（某些 Windows 版本的备用值）
    ok2, msg2 = _set_acrylic_legacy_internal(
        hwnd, _ACCENT_ENABLE_ACRYLICBLURBEHIND_ALT, base_rgb, opacity
    )
    if ok2:
        return True, f"Acrylic(Win10 legacy, alt) {msg2}"

    # 都失败，降级为普通模糊（state=3）
    ok3, msg3 = _set_acrylic_legacy_internal(
        hwnd, _ACCENT_ENABLE_BLURBEHIND, base_rgb, opacity
    )
    if ok3:
        return True, f"BlurBehind(降级) {msg3}"

    return False, f"全部失败: {msg}; {msg2}; {msg3}"


# ============================================================
#  暗色标题栏
# ============================================================
def _set_dark_titlebar(hwnd: int, dark: bool) -> bool:
    """设置暗色标题栏（Win10 1809+）"""
    dwm = _get_dwmapi()
    if dwm is None:
        return False
    try:
        val = DWORD(1 if dark else 0)
        dwm.DwmSetWindowAttribute(
            HWND(hwnd), _DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(val), ctypes.sizeof(val),
        )
        return True
    except Exception:
        return False


# ============================================================
#  统一入口
# ============================================================
def apply_backdrop(hwnd: int, kind: str = "mica", dark: bool = False,
                   base_rgb: tuple = None, opacity: int = None) -> tuple:
    """
    统一材质入口，根据系统版本自动选择新/老路径。

    Args:
        hwnd: 窗口句柄（必须在 show() 之后获取）
        kind: 材质类型
              "mica"     → 主窗口 Mica（Win11 22621+: attr=38,val=2; 22000+: 1029）
              "mica_alt" → MicaAlt（仅 22621+，attr=38,val=4）
              "acrylic"  → Acrylic（22621+: attr=38,val=3; <22621: 老路径 AccentState=5）
              "none"     → 清除材质
        dark: 是否暗色模式（设置暗色标题栏）
        base_rgb: Acrylic 基色，None 则自动取（浅色 255,255,255 / 深色 0,0,0）
        opacity: Acrylic 不透明度，None 则自动取（浅色 70 / 深色 85）

    Returns:
        (成功?, 说明文字)
    """
    if not _is_windows():
        return False, "非 Windows 系统"

    if hwnd == 0:
        return False, "hwnd=0，窗口未映射"

    build = get_windows_build()

    # 暗色标题栏
    _set_dark_titlebar(hwnd, dark)

    if kind == "none":
        # 清除材质
        if build < 22621:
            # Win10：禁用 Accent
            _set_acrylic_legacy_internal(
                hwnd, _ACCENT_DISABLED, (255, 255, 255), 0
            )
        else:
            # Win11：清除 DWM 材质 + 恢复 frame
            _dwm_set_backdrop(hwnd, _DWMSBT_NONE)
            _extend_frame(hwnd, fully=False)
        return True, "材质已清除"

    # ---- Mica ----
    if kind == "mica":
        if build >= 22621:
            return _dwm_set_backdrop(hwnd, _DWMSBT_MAINWINDOW)
        elif build >= 22000:
            return _dwm_legacy_mica(hwnd)
        else:
            return False, f"Win10(build {build})不支持 Mica，降级纯色"

    if kind == "mica_alt":
        if build >= 22621:
            return _dwm_set_backdrop(hwnd, _DWMSBT_TABBED)
        else:
            return False, f"MicaAlt 需 build 22621+，当前 {build}"

    # ---- Acrylic ----
    if kind == "acrylic":
        # 自动基色/不透明度
        if base_rgb is None:
            base_rgb = (0, 0, 0) if dark else (255, 255, 255)
        if opacity is None:
            opacity = 85 if dark else 70

        if build >= 22621:
            # Win11 22H2+：新路 DWMSBT_TRANSIENT=3
            return _dwm_set_backdrop(hwnd, _DWMSBT_TRANSIENT)
        else:
            # Win10 / Win11 21H2：老路径 SetWindowCompositionAttribute
            return _set_acrylic_legacy(hwnd, base_rgb, opacity)

    return False, f"未知 kind: {kind}"


def apply_to_window(window, kind: str = "mica", dark: bool = False) -> bool:
    """
    便捷方法：给 QWidget/QMainWindow 开启材质。

    必须在 window.show() 之后调用（showEvent 里最佳）。

    Args:
        window: QWidget 实例（顶层窗口）
        kind: "mica" / "mica_alt" / "acrylic" / "none"
        dark: 是否暗色模式
    """
    if not _is_windows():
        return False

    try:
        hwnd = int(window.winId())
    except (AttributeError, TypeError):
        return False

    if hwnd == 0:
        return False

    ok, msg = apply_backdrop(hwnd, kind=kind, dark=dark)
    if ok:
        try:
            window.setAttribute(window.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        except AttributeError:
            pass
        return True

    return False
