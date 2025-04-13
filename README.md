# Orderly
An auto folder organizer (Desktop App) including downloads

pyinstaller --name="Orderly" \
            --windowed \
            --debug all \
            --icon=Logo.icns \
            --add-data="Logo.png:." \
            --add-data="folder-add.png:." \
            --add-data="folder-open.png:." \
            --add-data="play-circle.png:." \
            --add-data="pause.png:." \
            --add-data="settings.png:." \
            --add-data="arrow-left.png:." \
            --add-data="arrow-circle-down.png:." \
            --add-data="arrow-circle-up.png:." \
            --add-data="folder.png:." \
            --add-data="magicpen.png:." \
            --hidden-import=PIL \
            --hidden-import=PIL._tkinter_finder \
            --hidden-import=customtkinter \
            --hidden-import=pystray \
            --hidden-import=requests \
            --hidden-import=watchdog \
            --hidden-import=watchdog.observers \
            --hidden-import=watchdog.events \
            --hidden-import=tkinter \
            --hidden-import=_tkinter \
            --collect-all customtkinter \
            --collect-all pystray \
            --collect-all PIL \
            main.py


create-dmg \         
  --volname "Orderly" \
  --volicon "Logo.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "Orderly.app" 175 120 \
  --hide-extension "Orderly.app" \
  --app-drop-link 425 120 \
  "Orderly.dmg" \
  "dist/Orderly.app"