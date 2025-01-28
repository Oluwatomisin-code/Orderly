# import os
# import shutil
# from tkinter import Tk, Label, Button, Listbox, filedialog, Scrollbar, END, SINGLE, messagebox, simpledialog
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler

# # Predefined file type rules
# DEFAULT_RULES = {
#     # Images
#     "jpg": "Images",
#     "jpeg": "Images",
#     "png": "Images",
#     "gif": "Images",
#     "bmp": "Images",
#     "tiff": "Images",
#     "webp": "Images",
#     "svg": "Images",
    
#     # Documents
#     "pdf": "Documents",
#     "doc": "Documents",
#     "docx": "Documents",
#     "xls": "Documents",
#     "xlsx": "Documents",
#     "ppt": "Documents",
#     "pptx": "Documents",
#     "txt": "Documents",
#     "rtf": "Documents",
#     "odt": "Documents",
#     "epub": "Documents",
    
#     # Videos
#     "mp4": "Videos",
#     "avi": "Videos",
#     "mkv": "Videos",
#     "mov": "Videos",
#     "flv": "Videos",
#     "wmv": "Videos",
#     "webm": "Videos",
    
#     # Audios
#     "mp3": "Audios",
#     "wav": "Audios",
#     "aac": "Audios",
#     "ogg": "Audios",
#     "flac": "Audios",
#     "wma": "Audios",
#     "m4a": "Audios",
    
#     # Compressed/Archives
#     "zip": "Archives",
#     "rar": "Archives",
#     "7z": "Archives",
#     "tar": "Archives",
#     "gz": "Archives",
#     "bz2": "Archives",
#     "xz": "Archives",
    
#     # Code/Executables
#     "exe": "Executables",
#     "msi": "Executables",
#     "sh": "Scripts",
#     "py": "Scripts",
#     "js": "Scripts",
#     "html": "Web_Files",
#     "css": "Web_Files",
#     "php": "Web_Files",
#     "java": "Code_Files",
#     "cpp": "Code_Files",
#     "c": "Code_Files",
#     "cs": "Code_Files",
#     "rb": "Code_Files",
#     "go": "Code_Files",
#     "ts": "Code_Files",
    
#     # Miscellaneous
#     "iso": "Disk_Images",
#     "dmg": "Disk_Images",
#     "apk": "Apps",
#     "ipa": "Apps",
#     "torrent": "Torrents",
# }


# class FileHandler(FileSystemEventHandler):
#     def __init__(self, rules, monitored_folders):
#         self.rules = rules
#         self.monitored_folders = monitored_folders

#     def on_created(self, event):
#         if not event.is_directory:
#             self.organize_file(event.src_path)

#     def organize_file(self, file_path):
#         file_name = os.path.basename(file_path)
#         ext = file_name.split(".")[-1].lower()
#         if ext in self.rules:
#             for folder in self.monitored_folders:
#                 if file_path.startswith(folder):
#                     target_folder = os.path.join(folder, self.rules[ext])
#                     os.makedirs(target_folder, exist_ok=True)
#                     target_path = os.path.join(target_folder, file_name)
#                     shutil.move(file_path, target_path)

#     def organize_all(self):
#         for folder in self.monitored_folders:
#             for file_name in os.listdir(folder):
#                 file_path = os.path.join(folder, file_name)
#                 if os.path.isfile(file_path):
#                     self.organize_file(file_path)

# class DownloadOrganizer:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Orderly")
        
#         # Initialize variables
#         self.rules = {**DEFAULT_RULES}
#         self.monitored_folders = []
#         self.observers = []

#         # Set default folders
#         self.add_default_folders()

#         # GUI components
#         Label(root, text="Monitored Folders:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
#         self.folder_listbox = Listbox(root, height=10, width=60, selectmode=SINGLE)
#         self.folder_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
#         Button(root, text="Add Folder", command=self.add_folder).grid(row=1, column=2, padx=10, pady=10)
#         Button(root, text="Remove Folder", command=self.remove_folder).grid(row=2, column=2, padx=10, pady=10)

#         Label(root, text="Extension Rules:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
#         self.rule_listbox = Listbox(root, height=10, width=60, selectmode=SINGLE)
#         self.rule_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
#         Button(root, text="Add Rule", command=self.add_rule).grid(row=4, column=2, padx=10, pady=10)
#         Button(root, text="Remove Rule", command=self.remove_rule).grid(row=5, column=2, padx=10, pady=10)

#         Button(root, text="Start Monitoring", command=self.start_monitoring).grid(row=6, column=0, pady=10)
#         Button(root, text="Stop Monitoring", command=self.stop_monitoring).grid(row=6, column=1, pady=10)

#         # Populate UI
#         self.update_rule_listbox()
#         self.update_folder_listbox()

#     def add_default_folders(self):
#         downloads = os.path.join(os.path.expanduser("~"), "Downloads")
#         documents = os.path.join(os.path.expanduser("~"), "Documents")
#         self.monitored_folders = [downloads, documents]

#     def add_folder(self):
#         folder = filedialog.askdirectory()
#         if folder and folder not in self.monitored_folders:
#             self.monitored_folders.append(folder)
#             self.update_folder_listbox()

#     def remove_folder(self):
#         selected = self.folder_listbox.curselection()
#         if selected:
#             folder = self.folder_listbox.get(selected)
#             self.monitored_folders.remove(folder)
#             self.update_folder_listbox()
#         else:
#             messagebox.showerror("Error", "Please select a folder to remove.")

#     def update_folder_listbox(self):
#         self.folder_listbox.delete(0, END)
#         for folder in self.monitored_folders:
#             self.folder_listbox.insert(END, folder)

#     def add_rule(self):
#         ext = simpledialog.askstring("Extension", "Enter file extension (e.g., jpg):").strip().lower()
#         folder = filedialog.askdirectory(title="Select Target Folder")
#         if ext and folder:
#             self.rules[ext] = folder
#             self.update_rule_listbox()

#     def remove_rule(self):
#         selected = self.rule_listbox.curselection()
#         if selected:
#             rule_text = self.rule_listbox.get(selected)
#             ext = rule_text.split(":")[0]
#             del self.rules[ext]
#             self.update_rule_listbox()
#         else:
#             messagebox.showerror("Error", "Please select a rule to remove.")

#     def update_rule_listbox(self):
#         self.rule_listbox.delete(0, END)
#         for ext, folder in self.rules.items():
#             self.rule_listbox.insert(END, f"{ext}: {folder}")

#     def start_monitoring(self):
#         self.stop_monitoring()

#         # Organize all existing files immediately
#         handler = FileHandler(self.rules, self.monitored_folders)
#         handler.organize_all()

#         # Start monitoring
#         for folder in self.monitored_folders:
#             observer = Observer()
#             observer.schedule(handler, folder, recursive=False)
#             observer.start()
#             self.observers.append(observer)

#         messagebox.showinfo("Started", "Monitoring started successfully!")

#     def stop_monitoring(self):
#         for observer in self.observers:
#             observer.stop()
#             observer.join()
#         self.observers = []
#         messagebox.showinfo("Stopped", "Monitoring stopped successfully!")

# # Run the application
# if __name__ == "__main__":
#     root = Tk()
#     app = DownloadOrganizer(root)
#     root.protocol("WM_DELETE_WINDOW", lambda: app.stop_monitoring() or root.destroy())
#     root.mainloop()

# from tkinter import Tk
# from gui import DownloadOrganizer
# from tray import SystemTrayApp
# import threading

# if __name__ == "__main__":
#     root = Tk()
#     app = DownloadOrganizer(root)

#     # Initialize and run the system tray
#     tray_app = SystemTrayApp(app)
#     threading.Thread(target=tray_app.setup_tray_icon, daemon=True).start()

#     root.protocol("WM_DELETE_WINDOW", lambda: app.stop_monitoring() or root.destroy())
#     root.mainloop()
from tkinter import Tk
from gui import DownloadOrganizer
from tray import SystemTrayApp
from updater import AppUpdater
import threading
from tkinter import messagebox

CURRENT_VERSION = "1.0.0"
REPO_OWNER = "oluwatomisin-code"
REPO_NAME = "Orderly"

def check_for_updates_periodically(updater, interval=3600):
    import time
    while True:
        update_info = updater.check_for_update()
        if update_info["update_available"]:
            latest_version = update_info["latest_version"]
            download_url = update_info["download_url"]
            prompt = f"A new version ({latest_version}) is available. Would you like to update now?"
            if messagebox.askyesno("Update Available", prompt):
                updater.download_and_apply_update(download_url, target_dir=".")
        time.sleep(interval)

if __name__ == "__main__":
    root = Tk()
    app = DownloadOrganizer(root)

    updater = AppUpdater(REPO_OWNER, REPO_NAME, CURRENT_VERSION)

    # Check for updates at startup
    update_info = updater.check_for_update()
    if update_info["update_available"]:
        latest_version = update_info["latest_version"]
        download_url = update_info["download_url"]
        prompt = f"A new version ({latest_version}) is available. Would you like to update now?"
        if messagebox.askyesno("Update Available", prompt):
            updater.download_and_apply_update(download_url, target_dir=".")

    # Start periodic update checking in a separate thread
    threading.Thread(target=check_for_updates_periodically, args=(updater,), daemon=True).start()

    # Initialize and run the system tray
    tray_app = SystemTrayApp(app)
    threading.Thread(target=tray_app.setup_tray_icon, daemon=True).start()

    root.protocol("WM_DELETE_WINDOW", lambda: app.stop_monitoring() or root.destroy())
    root.mainloop()
