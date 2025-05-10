# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [
    ('assets/Logo.png', 'assets'),
    ('assets/Logo.icns', 'assets'),
    ('assets/orderly.ico', 'assets'),
    ('assets/folder-add.png', 'assets'),
    ('assets/folder-add-trans.png', 'assets'),
    ('assets/folder-open.png', 'assets'),
    ('assets/play-circle.png', 'assets'),
    ('assets/pause.png', 'assets'),
    ('assets/settings.png', 'assets'),
    ('assets/settingsoo.png', 'assets'),
    ('assets/arrow-left.png', 'assets'),
    ('assets/arrow-circle-down.png', 'assets'),
    ('assets/arrow-circle-up.png', 'assets'),
    ('assets/folder.png', 'assets'),
    ('assets/magicpen.png', 'assets'),
    ('assets/no-folders.png', 'assets'),
    ('assets/splash.png', 'assets'),
    ('assets/minus-circle.png', 'assets'),
    ('assets/tick-circle.png', 'assets')
]
binaries = []
hiddenimports = ['PIL', 'PIL._tkinter_finder', 'customtkinter', 'pystray', 'requests', 'watchdog', 'watchdog.observers', 'watchdog.events', 'tkinter', '_tkinter']
tmp_ret = collect_all('customtkinter')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('pystray')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('PIL')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=True,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [('v', None, 'OPTION')],
    exclude_binaries=True,
    name='Orderly',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets/Logo.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Orderly',
)
app = BUNDLE(
    coll,
    name='Orderly.app',
    icon='assets/Logo.icns',
    bundle_identifier=None,
)
