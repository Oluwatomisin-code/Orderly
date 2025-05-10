# Orderly
An auto folder organizer (Desktop App) including downloads

pyinstaller --name="Orderly" \
            --windowed \
            --debug all \
            --icon=assets/Logo.icns \
            --add-data="assets/Logo.png:." \
            --add-data="assets/folder-add.png:." \
            --add-data="assets/folder-open.png:." \
            --add-data="assets/play-circle.png:." \
            --add-data="assets/pause.png:." \
            --add-data="assets/settings.png:." \
            --add-data="assets/arrow-left.png:." \
            --add-data="assets/arrow-circle-down.png:." \
            --add-data="assets/arrow-circle-up.png:." \
            --add-data="assets/folder.png:." \
            --add-data="assets/magicpen.png:." \
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