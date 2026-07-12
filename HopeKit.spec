# -*- mode: python ; coding: utf-8 -*-
"""
HopeKit 2.1.0 PyInstaller 打包配置 — 全量收集模式
"""

import re, os, sys
from pathlib import Path

_spec_dir = SPECPATH
sys.path.insert(0, _spec_dir)

# ── 读取版本号 ──
_version_path = os.path.join(_spec_dir, "hopekit", "version.py")
with open(_version_path, "r", encoding="utf-8") as _f:
    _m = re.search(r'VERSION\s*=\s*"([^"]+)"', _f.read())
VERSION = _m.group(1) if _m else "0.0.0"


# ── 递归发现所有 Python 模块 ──
def _find_modules(root_dir: str, package: str) -> list:
    """递归扫描目录下的所有 .py 模块，返回 module name 列表。"""
    modules = []
    root = Path(root_dir)
    if not root.is_dir():
        return modules
    for py_file in sorted(root.rglob("*.py")):
        if py_file.name.startswith("__") and py_file.name != "__init__.py":
            continue  # 跳过 __pycache__ 等
        rel = py_file.relative_to(root)
        parts = list(rel.parts)
        parts[-1] = parts[-1][:-3]  # 去掉 .py
        if parts[-1] == "__init__":
            parts = parts[:-1]  # package 本身
        if not parts:
            continue
        module_name = f"{package}.{'.'.join(parts)}"
        if module_name not in modules:
            modules.append(module_name)
    return modules


_hiddenimports = []
_hiddenimports += _find_modules(os.path.join(_spec_dir, "hopekit"), "hopekit")
_hiddenimports += _find_modules(os.path.join(_spec_dir, "plugins"), "plugins")
_hiddenimports += _find_modules(os.path.join(_spec_dir, "Styles"), "Styles")
_hiddenimports += _find_modules(os.path.join(_spec_dir, "examples"), "examples")

# ctypes 子模块（DWM API 需要）
_hiddenimports += ["ctypes", "ctypes.wintypes"]

print(f"[spec] 发现 {len(_hiddenimports)} 个隐式模块", flush=True)

# ── 数据目录（全部打包） ──
# Tree() 返回 3 元组 (dest, src, type)，Analysis 需要 2 元组 (src, dest)
from PyInstaller.building.datastruct import Tree

def _tree_data(root_dir: str, prefix: str) -> list:
    """调用 Tree 并转为 (src, dest) 格式。"""
    toc = Tree(root_dir, prefix=prefix, excludes=["__pycache__", "*.pyc"])
    return [(src, dst) for (dst, src, _typ) in toc]

_datas = [
    ('logo.jpg', '.'),
    ('theme.json', '.'),
]
_datas += _tree_data(os.path.join(_spec_dir, "hopekit"), "hopekit")
_datas += _tree_data(os.path.join(_spec_dir, "plugins"), "plugins")
_datas += _tree_data(os.path.join(_spec_dir, "Styles"), "Styles")
_datas += _tree_data(os.path.join(_spec_dir, "examples"), "examples")

# ── 排除系统 DLL（交给 ctypes.windll 从系统加载） ──
_exclude_dlls = [
    "api-ms-win-*",
    "vcruntime140.dll",
    "msvcp140.dll",
    "ucrtbase.dll",
]


a = Analysis(
    ['hopekitmain.py'],
    pathex=[_spec_dir],
    binaries=[],
    datas=_datas,
    hiddenimports=_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# ── 过滤系统 DLL ──
from fnmatch import fnmatch
a.binaries = [b for b in a.binaries if not any(fnmatch(b[0].lower(), pat.lower()) for pat in _exclude_dlls)]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='HopeKit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='HopeKit',
)
