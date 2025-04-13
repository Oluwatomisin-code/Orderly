import os
import sys
if sys.platform == 'darwin':  # macOS specific
    os.environ['PYTHON_HIDE_DOCK_ICON'] = '1'

from tkinter import Tk
from gui import App
from tray import SystemTray
from updater import Updater
import threading
from tkinter import messagebox
import customtkinter as ctk
import signal
import sys
import pystray
from PIL import Image
import platform
import logging
import os

CURRENT_VERSION = "1.0.0"
REPO_OWNER = "oluwatomisin-code"
REPO_NAME = "Orderly"

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=os.path.expanduser('~/orderly_debug.log'),
    filemode='w'
)

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def check_for_updates_periodically(updater):
    while True:
        try:
            logging.debug("Checking for updates...")
            update_info = updater.check_for_update()
            if update_info.get("update_available"):
                logging.info(f"Update available: {update_info['latest_version']}")
        except Exception as e:
            logging.error(f"Update check failed: {e}")
        threading.Event().wait(3600)

def signal_handler(sig, frame):
    """Handle cleanup when app is terminated"""
    sys.exit(0)

class OrderlyApp:
    def __init__(self):
        self.root = None
        self.app = None
        self.tray = None
        self.updater = None
        
    def setup_window(self):
        try:
            # Create and configure main window
            self.root = ctk.CTk()
            self.root.title("Orderly")
            self.root.geometry("450x550")
            
            # Initialize the main app
            self.app = App(self.root)
            
            # Don't withdraw window on startup
            self.root.deiconify()
            
            # Prevent immediate closing
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            return True
        except Exception as e:
            logging.exception("Failed to setup window")
            return False

    def setup_tray(self):
        try:
            # Initialize system tray after window
            self.tray = SystemTray(self.root)
            return True
        except Exception as e:
            logging.exception("Failed to setup tray")
            return False

    def setup_updater(self):
        try:
            # Initialize updater
            self.updater = Updater(
                repo_owner="oluwatomisin",
                repo_name="Orderly",
                current_version="1.0.0"
            )
            
            # Start update checker in background
            update_thread = threading.Thread(
                target=self.check_for_updates_periodically,
                daemon=True
            )
            update_thread.start()
            return True
        except Exception as e:
            logging.exception("Failed to setup updater")
            return False

    def check_for_updates_periodically(self):
        while True:
            try:
                update_info = self.updater.check_for_update()
                if update_info.get("update_available"):
                    logging.info(f"Update available: {update_info['latest_version']}")
            except Exception as e:
                logging.error(f"Update check failed: {e}")
            threading.Event().wait(3600)

    def on_closing(self):
        try:
            # Hide window instead of closing
            self.root.withdraw()
        except Exception as e:
            logging.exception("Error in on_closing")
            self.quit_app()

    def quit_app(self):
        try:
            if self.tray:
                self.tray.icon.stop()
            if self.root:
                self.root.quit()
        except Exception as e:
            logging.exception("Error while quitting")
            sys.exit(1)

    def run(self):
        try:
            # Setup components
            if not self.setup_window():
                return
            
            if not self.setup_tray():
                return
            
            if not self.setup_updater():
                return
            
            # Start the main loop
            self.root.mainloop()
            
        except Exception as e:
            logging.exception("Critical error in run")
            sys.exit(1)

def main():
    app = OrderlyApp()
    app.run()

if __name__ == "__main__":
    main()

class SystemTray:
    def __init__(self, root):
        self.root = root
        self.icon = None
        self.setup_tray_icon()

    def setup_tray_icon(self):
        try:
            # Load the tray icon image
            image = Image.open("Logo.png")
            
            # Create the menu
            menu = (
                pystray.MenuItem("Show", self.show_window),
                pystray.MenuItem("Hide", self.hide_window),
                pystray.MenuItem("Quit", self.quit_app)
            )
            
            # Create the icon
            self.icon = pystray.Icon("Orderly", image, "Orderly", menu)
            
            # Start the icon in a separate thread
            icon_thread = threading.Thread(target=self.run_icon)
            icon_thread.daemon = True
            icon_thread.start()
            
        except Exception as e:
            print(f"Error setting up tray icon: {e}")
            raise

    def run_icon(self):
        try:
            self.icon.run()
        except Exception as e:
            print(f"Error running tray icon: {e}")

    def show_window(self, _=None):
        self.root.after(0, self.root.deiconify)
        self.root.after(0, self.root.lift)

    def hide_window(self, _=None):
        self.root.after(0, self.root.withdraw)

    def quit_app(self, _=None):
        try:
            if self.icon:
                self.icon.stop()
            self.root.after(0, self.root.quit)
        except Exception as e:
            print(f"Error quitting app: {e}")
