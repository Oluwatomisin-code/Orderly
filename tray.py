import sys
from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading
import platform
from tkinter import Tk
import os

def get_resource_path(relative_path):
    """Get the correct resource path for both development and bundled app"""
    if getattr(sys, 'frozen', False):
        # Running in a bundle
        base_path = sys._MEIPASS
    else:
        # Running in development
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SystemTray:
    def __init__(self, root: Tk):
        self.root = root
        self.icon = None
        if platform.system() == 'Darwin':
            from Foundation import NSObject
            from AppKit import NSApplication, NSStatusBar
            NSApplication.sharedApplication()
            # Hide dock icon
            NSApplication.sharedApplication().setActivationPolicy_(1)  # 1 = NSApplicationActivationPolicyAccessory
        self.root.protocol('WM_DELETE_WINDOW', self.handle_close)
        self.setup_tray_icon()

    def handle_close(self):
        """Handle window close button (red X) click"""
        # Just hide the window instead of quitting
        self.hide_window()
        # Optional: Show a notification that app is still running
        if self.icon:
            self.icon.notify("Orderly is still running in the background")

    def setup_tray_icon(self):
        """Setup system tray icon on the main thread"""
        try:
            # Load icon image using resource path
            icon_image = Image.open(get_resource_path(os.path.join("assets","Logo.png")))

            # Create menu items
            menu = Menu(
                MenuItem("Show", self.show_window),
                MenuItem("Hide", self.hide_window),
                MenuItem("Quit", self.quit_app)  # Changed "Exit" to "Quit" for consistency
            )

            # Create system tray icon
            self.icon = Icon(
                name="Orderly",
                icon=icon_image,
                title="Orderly",
                menu=menu
            )

            # Start icon in a separate thread
            threading.Thread(target=self.run_icon, daemon=True).start()

        except Exception as e:
            print(f"Error setting up system tray: {str(e)}")

    def run_icon(self):
        """Run the system tray icon"""
        try:
            self.icon.run()
        except Exception as e:
            print(f"Error running system tray: {str(e)}")

    def show_window(self, icon=None, item=None):
        """Show the main window"""
        self.root.deiconify()
        self.root.lift()
        if platform.system() == 'Darwin':  # macOS
            self.root.attributes('-topmost', True)
            self.root.attributes('-topmost', False)

    def hide_window(self, icon=None, item=None):
        """Hide the main window"""
        self.root.withdraw()

    def quit_app(self, icon=None, item=None):
        """Completely quit the application"""
        if self.icon:
            self.icon.stop()
        self.root.quit()

    def stop(self):
        """Stop the system tray icon"""
        if self.icon:
            self.icon.stop()

# def run_tray_icon(app):
#     return SystemTray(app.root)

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
