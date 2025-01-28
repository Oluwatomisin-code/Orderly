import sys
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw


class SystemTrayApp:
    def __init__(self, app):
        self.app = app
        self.tray_icon = None

    def setup_tray_icon(self):
        icon_image = self.create_image()
        menu = Menu(
            MenuItem("Open GUI", lambda: self.app.root.deiconify()),
            MenuItem("Exit", self.exit_application),
        )
        self.tray_icon = Icon("Orderly", icon_image, "Orderly", menu)
        self.tray_icon.run()

    def create_image(self):
        image = Image.new("RGB", (64, 64), color=(0, 128, 255))
        draw = ImageDraw.Draw(image)
        draw.rectangle((16, 16, 48, 48), fill=(255, 255, 255))
        return image

    def exit_application(self):
        if self.tray_icon:
            self.tray_icon.stop()
        self.app.stop_monitoring()
        sys.exit(0)
