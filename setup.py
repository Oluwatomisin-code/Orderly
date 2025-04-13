from setuptools import setup

APP = ['main.py']
DATA_FILES = [
    'Logo.png',
    'arrow-left.png',
    'arrow-circle-down.png',
    'arrow-circle-up.png',
    'folder.png',
    'folder-add.png',
    'folder-open.png',
    'magicpen.png',
    'minus-circle.png',
    'pause.png',
    'play-circle.png',
    'settings.png',
    'tick-circle.png'
]

OPTIONS = {
    'argv_emulation': True,
    'packages': ['customtkinter', 'PIL', 'watchdog'],
    'iconfile': 'Logo.icns',
    'plist': {
        'CFBundleName': 'Orderly',
        'CFBundleDisplayName': 'Orderly',
        'CFBundleGetInfoString': "Organize your downloads automatically",
        'CFBundleIdentifier': "com.ordely.app",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHumanReadableCopyright': u"Copyright © 2024, Your Name, All Rights Reserved"
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    name="Orderly"
)
