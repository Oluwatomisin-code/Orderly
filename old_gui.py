from tkinter import Tk, Label, Button, Listbox, filedialog, Scrollbar, END, SINGLE, messagebox, simpledialog
from watchdog.observers import Observer
from file_handler import FileHandler

from config import DEFAULT_RULES, DEFAULT_FOLDERS


class DownloadOrganizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Orderly")
        self.rules = {**DEFAULT_RULES}
        self.monitored_folders = DEFAULT_FOLDERS
        self.observers = []

        # GUI components
        Label(root, text="Monitored Folders:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.folder_listbox = Listbox(root, height=10, width=60, selectmode=SINGLE)
        self.folder_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        Button(root, text="Add Folder", command=self.add_folder).grid(row=1, column=2, padx=10, pady=10)
        Button(root, text="Remove Folder", command=self.remove_folder).grid(row=2, column=2, padx=10, pady=10)

        Label(root, text="Extension Rules:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.rule_listbox = Listbox(root, height=10, width=60, selectmode=SINGLE)
        self.rule_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        Button(root, text="Add Rule", command=self.add_rule).grid(row=4, column=2, padx=10, pady=10)
        Button(root, text="Remove Rule", command=self.remove_rule).grid(row=5, column=2, padx=10, pady=10)

        Button(root, text="Start Monitoring", command=self.start_monitoring).grid(row=6, column=0, pady=10)
        Button(root, text="Stop Monitoring", command=self.stop_monitoring).grid(row=6, column=1, pady=10)

        self.update_rule_listbox()
        self.update_folder_listbox()

    def add_folder(self):
        folder = filedialog.askdirectory()
        if folder not in self.monitored_folders:
            self.monitored_folders.append(folder)
            self.update_folder_listbox()

    def remove_folder(self):
        selected = self.folder_listbox.curselection()
        if selected:
            folder = self.folder_listbox.get(selected)
            self.monitored_folders.remove(folder)
            self.update_folder_listbox()

    def update_folder_listbox(self):
        self.folder_listbox.delete(0, END)
        for folder in self.monitored_folders:
            self.folder_listbox.insert(END, folder)

    def add_rule(self):
        ext = simpledialog.askstring("Extension", "Enter file extension (e.g., jpg):").strip().lower()
        folder = filedialog.askdirectory()
        if ext and folder:
            self.rules[ext] = folder
            self.update_rule_listbox()

    def remove_rule(self):
        selected = self.rule_listbox.curselection()
        if selected:
            rule_text = self.rule_listbox.get(selected)
            ext = rule_text.split(":")[0]
            del self.rules[ext]
            self.update_rule_listbox()

    def update_rule_listbox(self):
        self.rule_listbox.delete(0, END)
        for ext, folder in self.rules.items():
            self.rule_listbox.insert(END, f"{ext}: {folder}")

    def start_monitoring(self):
        self.stop_monitoring()
        handler = FileHandler(self.rules, self.monitored_folders)
        handler.organize_all()

        for folder in self.monitored_folders:
            observer = Observer()
            observer.schedule(handler, folder, recursive=False)
            observer.start()
            self.observers.append(observer)

    def stop_monitoring(self):
        for observer in self.observers:
            observer.stop()
            observer.join()
        self.observers = []
