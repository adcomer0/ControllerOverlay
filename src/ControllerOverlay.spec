# -*- mode: python ; coding: utf-8 -*-
import sys
import pathlib

block_cipher = None

# Directory where the main_assets folder is located
assets_dir = pathlib.Path(__file__).resolve().parent / 'main_assets'

a = Analysis(
    ['ControllerOverlay.py'],
    pathex=['src'],
    binaries=[],
    datas=[(assets_dir, 'main_assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)
