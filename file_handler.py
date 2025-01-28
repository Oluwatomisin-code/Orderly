import os
import shutil
from watchdog.events import FileSystemEventHandler


class FileHandler(FileSystemEventHandler):
    def __init__(self, rules, monitored_folders):
        self.rules = rules
        self.monitored_folders = monitored_folders

    def on_created(self, event):
        if not event.is_directory:
            self.organize_file(event.src_path)

    def organize_file(self, file_path):
        file_name = os.path.basename(file_path)
        ext = file_name.split(".")[-1].lower()
        if ext in self.rules:
            for folder in self.monitored_folders:
                if file_path.startswith(folder):
                    target_folder = os.path.join(folder, self.rules[ext])
                    os.makedirs(target_folder, exist_ok=True)
                    target_path = os.path.join(target_folder, file_name)
                    shutil.move(file_path, target_path)

    def organize_all(self):
        for folder in self.monitored_folders:
            for file_name in os.listdir(folder):
                file_path = os.path.join(folder, file_name)
                if os.path.isfile(file_path):
                    self.organize_file(file_path)
