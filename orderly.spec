# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('Logo.png', '.'), ('folder-add.png', '.'), ('folder-open.png', '.'), ('play-circle.png', '.'), ('pause.png', '.'), ('settings.png', '.'), ('arrow-left.png', '.'), ('arrow-circle-down.png', '.'), ('arrow-circle-up.png', '.'), ('folder.png', '.'), ('magicpen.png', '.')]
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
    icon=['Logo.icns'],
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
    icon='Logo.icns',
    bundle_identifier=None,
    info_plist={
        'LSUIElement': True,  
        'LSBackgroundOnly': True,  
        'CFBundleName': 'Orderly',
        'CFBundleDisplayName': 'Orderly',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,
    },
)
