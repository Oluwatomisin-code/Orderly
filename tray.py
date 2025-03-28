import sys
from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading
import platform
from tkinter import Tk

class SystemTray:
    def __init__(self, root: Tk):
        self.root = root
        self.icon = None
        self.setup_tray_icon()

    def setup_tray_icon(self):
        """Setup system tray icon on the main thread"""
        try:
            # Load icon image
            icon_image = Image.open("Logo.png")  # Make sure this image exists

            # Create menu items
            menu = Menu(
                MenuItem("Show", self.show_window),
                MenuItem("Hide", self.hide_window),
                MenuItem("Exit", self.quit_app)
            )

            # Create system tray icon
            self.icon = Icon(
                name="Orderly",
                icon=icon_image,
                title="Orderly",
                menu=menu
            )

            # Start icon in a way that doesn't block the main thread
            threading.Thread(target=self.run_icon, daemon=True).start()

        except Exception as e:
            print(f"Error setting up system tray: {str(e)}")

    def run_icon(self):
        """Run the system tray icon"""
        try:
            self.icon.run()
        except Exception as e:
            print(f"Error running system tray: {str(e)}")

    def show_window(self, icon, item):
        """Show the main window"""
        self.root.deiconify()
        self.root.lift()
        if platform.system() == 'Darwin':  # macOS
            self.root.attributes('-topmost', True)
            self.root.attributes('-topmost', False)

    def hide_window(self, icon, item):
        """Hide the main window"""
        self.root.withdraw()

    def quit_app(self, icon, item):
        """Quit the application"""
        icon.stop()
        self.root.quit()

    def stop(self):
        """Stop the system tray icon"""
        if self.icon:
            self.icon.stop()

# Helper function to handle the platform-specific threading logic
def run_tray_icon(app):
    tray_app = SystemTray(app.root)
    
    print(sys.platform, 'platform')
    
    # Check if the application is being run on macOS
    if sys.platform == "darwin":
        # Run the tray icon setup on the main thread for macOS
        threading.Thread(target=tray_app.setup_tray_icon, daemon=True).start()
    else:
        # For other platforms (Windows/Linux), run this directly
        tray_app.setup_tray_icon()

# Example Usage:
# Assuming your main application class is called `DownloadOrganizer`, you would pass that to `run_tray_icon`.
# from your_application import DownloadOrganizer

# If you are using Tkinter, for example:
# root = ctk.CTk()
# app = DownloadOrganizer(root)
# run_tray_icon(app)
