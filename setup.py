from setuptools import setup

APP = ['main.py']  # Your main script
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pystray', 'watchdog', 'threading','requests','tkinter', 'Pillow'],  # Include necessary packages
    'plist': {
        'CFBundleName': 'Orderly',
        'CFBundleDisplayName': 'Orderly',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleIdentifier': 'com.example.orderly',
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
