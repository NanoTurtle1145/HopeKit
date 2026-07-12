"""
最小可复现 demo：PySide6 + Win10 Acrylic 透明效果

版本要求：PySide6 6.6+ + Win10 build 1803+

正确组合：
  1. WA_TranslucentBackground（show 前）→ WS_EX_LAYERED
  2. WA_NoSystemBackground（central）→ 禁止 Qt 自动填色
  3. SetWindowCompositionAttribute + ACCENT_ENABLE_ACRYLICBLURBEHIND（showEvent 里）
"""

import sys
import ctypes
from ctypes.wintypes import DWORD, HWND, INT, BOOL

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel, QVBoxLayout
from PySide6.QtCore import Qt


# ============================================================
# DWM 常量（Win10 Acrylic 老路径）
# ============================================================
_WCA_ACCENT_POLICY = 19
_ACCENT_ENABLE_ACRYLICBLURBEHIND = 4


class _AccentPolicy(ctypes.Structure):
    _fields_ = [
        ("AccentState", INT),
        ("AccentFlags", INT),
        ("GradientColor", DWORD),
        ("AnimationId", INT),
    ]


class _WinCompAttrData(ctypes.Structure):
    _fields_ = [
        ("attrib", INT),
        ("pvData", ctypes.POINTER(_AccentPolicy)),
        ("cbData", ctypes.c_size_t),
    ]


def _argb(a, r, g, b):
    return (a << 24) | (r << 16) | (g << 8) | b


def set_acrylic(hwnd, dark=False):
    """设置 Win10 Acrylic 效果"""
    user32 = ctypes.windll.user32
    try:
        setwca = user32.SetWindowCompositionAttribute
        setwca.argtypes = [HWND, ctypes.POINTER(_WinCompAttrData)]
        setwca.restype = BOOL
    except AttributeError:
        return False, "SetWindowCompositionAttribute 不存在"

    base_rgb = (0, 0, 0) if dark else (255, 255, 255)
    # ⚠️ 关键：降低基色不透明度，让模糊效果更明显
    # 不透明度越低（alpha 越小），桌面模糊越清晰可见
    opacity = 60 if dark else 30  # 从 70/85 降到 30/60
    a = int(opacity * 255 / 100)
    grad = _argb(a, *base_rgb)

    policy = _AccentPolicy(
        AccentState=_ACCENT_ENABLE_ACRYLICBLURBEHIND,
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
        return ok, f"Acrylic OK: state=4, base={base_rgb}, opacity={opacity}%"
    except Exception as e:
        return False, f"异常: {e}"


# ============================================================
# 主窗口
# ============================================================
class AcrylicDemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Win10 Acrylic Demo")
        self.resize(800, 500)

        # ⚠️ 关键1：WA_TranslucentBackground 必须在 show() 之前设置
        # Qt6.6+ 会强制走 WS_EX_LAYERED，这是 Acrylic 正常工作的前提
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        # ⚠️ 关键2：central widget 用 WA_NoSystemBackground 禁止 Qt 自动填色
        # 不要设 QSS background: transparent，会冲突
        central = QWidget()
        central.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        central.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setCentralWidget(central)

        # 布局：左侧半透明 sidebar + 右侧不透明内容区
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 左侧 sidebar：低透明度，让 Acrylic 效果清晰透出
        sidebar = QWidget()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet("background: rgba(243, 243, 243, 0.30);")  # 从 0.70 降到 0.30
        layout.addWidget(sidebar)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.addWidget(QLabel("← 侧边栏（透 Acrylic）"))
        sidebar_layout.addWidget(QLabel("背景应该看到桌面模糊"))

        # 右侧内容区：不透明，保证可读性
        content = QWidget()
        content.setStyleSheet("background: #fafafa;")
        layout.addWidget(content, 1)

        content_layout = QVBoxLayout(content)
        content_layout.addWidget(QLabel("→ 内容区（不透明）"))
        content_layout.addWidget(QLabel("这里文字清晰可读"))

        self._acrylic_applied = False

    def showEvent(self, e):
        super().showEvent(e)
        if e.spontaneous() or self._acrylic_applied:
            return

        # ⚠️ 关键3：HWND 在 show() 之后才有效
        hwnd = int(self.winId())
        print(f"[Demo] hwnd={hwnd}", flush=True)

        ok, msg = set_acrylic(hwnd, dark=False)
        print(f"[Demo] Acrylic: {ok}, {msg}", flush=True)

        self._acrylic_applied = ok


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AcrylicDemoWindow()
    window.show()
    sys.exit(app.exec())
