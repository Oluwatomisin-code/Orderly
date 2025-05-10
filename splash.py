import customtkinter as ctk
from PIL import Image
import os
import sys

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SplashScreen(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        
        # Remove window decorations
        self.overrideredirect(True)
        
        # Match main window dimensions
        width = 450
        height = 550
        
        # Center the splash screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        # Load splash image
        splash_image = ctk.CTkImage(
            light_image=Image.open(get_resource_path("assets/splash.png")),
            dark_image=Image.open(get_resource_path("assets/splash.png")),
            size=(width, height)
        )
        
        # Create and pack the image label
        splash_label = ctk.CTkLabel(self, image=splash_image, text="")
        splash_label.pack(fill="both", expand=True)
        
        # Bring splash window to front
        self.lift()
        self.attributes('-topmost', True)
        
        # Update the window
        self.update()
