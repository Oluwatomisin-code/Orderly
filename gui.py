import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import platform
import sys

from db import DBHandler
from file_handler import FileHandler

def get_resource_path(relative_path):
    """Get the correct resource path for both development and bundled app"""
    if getattr(sys, 'frozen', False):
        # Running in a bundle
        base_path = sys._MEIPASS
    else:
        # Running in development
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Orderly")
        self.root.geometry("450x550")
        
        # Add window icon
        try:
            icon = Image.open(get_resource_path(os.path.join("assets","Logo.png")))
            # Convert PIL image to PhotoImage
            from tkinter import PhotoImage
            icon_photo = PhotoImage(file=get_resource_path(os.path.join("assets","Logo.png")))
            self.root.iconphoto(True, icon_photo)
        except Exception as e:
            print(f"Error setting window icon: {str(e)}")
        
        ctk.set_appearance_mode("system")  # Dark mode
        self.root.configure(bg="#181818")  # Dark mode
        
        self.db = DBHandler()
        self.monitored_folders = self.db.fetch_folders()
        self.rules = self.db.fetch_rules()
        self.observers = {}
        self.monitoring = self.db.fetch_monitoring_status()
        self.popup = None  # Popup reference
        
        # Load icons
        self.empty_state_icon = ctk.CTkImage(
            light_image=Image.open(get_resource_path(os.path.join("assets","no-folders.png"))),
            dark_image=Image.open(get_resource_path(os.path.join("assets","no-folders.png"))),
            size=(120, 80)
        )
        
        # Add these as new instance variables
        self.main_view = ctk.CTkFrame(root, fg_color="transparent")
        self.main_view.pack(fill="both", expand=True)
        
        # # Header Frame
        # self.header = ctk.CTkFrame(self.main_view, fg_color="transparent")
        # self.header.pack(fill="x", padx=10, pady=10)
        
        # Header Frame (initially hidden)
        self.header = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.header.pack(fill="x", padx=10, pady=10)  # Always pack it to maintain layout order
        self.header.pack_forget()  # Hide it initially
        
        self.folder_text = ctk.CTkLabel(self.header, text="Folders", font=("Arial", 14))
        self.folder_text.pack(side="left", padx=10)
        
        upload_icon_loaded = ctk.CTkImage(
            light_image=Image.open(get_resource_path(os.path.join("assets","folder-add.png"))),
            dark_image=Image.open(get_resource_path(os.path.join("assets","folder-add.png"))),
            size=(18, 18)
        )
        
        self.upload_btn = ctk.CTkButton(self.header, image=upload_icon_loaded, text=" Add a folder to monitor", hover_color="#181818",
                                        fg_color="transparent", text_color="#FF617F", 
                                        command=self.add_folder)
        self.upload_btn.pack(side="right", padx=10)
        
        # Folder List Frame
        self.folders_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.folders_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.folder_widgets = []
        self.update_folder_list_ui()
        
        # Initialize monitoring button as None
        self.monitor_button = None
        # Only create monitoring button if we have folders
        if self.monitored_folders:
            self.create_monitor_button()
        
        # Initialize rules view as None
        self.rules_view = None
        
    
    def update_folder_list_ui(self):
        for widget in self.folder_widgets:
            widget.destroy()
        self.folder_widgets.clear()

        if not self.monitored_folders:
                # Hide the header when no folders
            self.header.pack_forget()

            # Empty state UI
            empty_frame = ctk.CTkFrame(self.folders_frame, fg_color="transparent")
            empty_frame.pack(expand=True, fill="both")

            empty_frame.grid_rowconfigure(0, weight=1)
            empty_frame.grid_columnconfigure(0, weight=1)

            content_frame = ctk.CTkFrame(empty_frame, fg_color="transparent")
            content_frame.grid(row=0, column=0)

            icon_frame = ctk.CTkFrame(content_frame, fg_color="transparent", width=120, height=120, corner_radius=40)
            icon_frame.pack(pady=(0, 20))
            icon_frame.pack_propagate(False)

            icon_label = ctk.CTkLabel(icon_frame, image=self.empty_state_icon, text="")
            icon_label.place(relx=0.5, rely=0.5, anchor="center")

            title_label = ctk.CTkLabel(content_frame, text="Your Files, Organized Effortlessly", font=("Arial", 18, "bold"))
            title_label.pack(pady=(0, 10))

            desc_label = ctk.CTkLabel(
                content_frame,
                text="Click Upload to get started. Once uploaded,\nwe'll automatically sort them based on your\ncustom rules.",
                font=("Arial", 12),
                text_color="gray"
            )
            desc_label.pack(pady=(0, 20))

            upload_icon_loaded = ctk.CTkImage(
                light_image=Image.open(get_resource_path(os.path.join("assets", "folder-add-trans.png"))),
                dark_image=Image.open(get_resource_path(os.path.join("assets", "folder-add-trans.png"))),
                size=(18, 18)
            )

            add_folder_btn = ctk.CTkButton(
                content_frame,
                image=upload_icon_loaded,
                text="Add a folder to monitor",
                fg_color="#FF2D55",
                text_color="white",
                width=200,
                height=56,
                corner_radius=30,
                command=self.add_folder
            )
            add_folder_btn.pack()

            self.folder_widgets.append(empty_frame)
            return

        else:
            # Show the header *above* the folders_frame
            if not self.header.winfo_ismapped():
                self.header.pack_forget()
                self.header.pack(before=self.folders_frame, fill="x", padx=10, pady=10)
                # Load icons
        folder_icon_loaded = ctk.CTkImage(
            light_image=Image.open(get_resource_path(os.path.join("assets", "folder-open.png"))),
            dark_image=Image.open(get_resource_path(os.path.join("assets", "folder-open.png"))),
            size=(24, 24)
        )
        play_icon_loaded = ctk.CTkImage(
            light_image=Image.open(get_resource_path(os.path.join("assets", "play-circle.png"))),
            dark_image=Image.open(get_resource_path(os.path.join("assets", "play-circle.png"))),
            size=(20, 20)
        )
        pause_icon_loaded = ctk.CTkImage(
            light_image=Image.open(get_resource_path(os.path.join("assets", "pause.png"))),
            dark_image=Image.open(get_resource_path(os.path.join("assets", "pause.png"))),
            size=(20, 20)
        )
        settings_icon_loaded = ctk.CTkImage(
            light_image=Image.open(get_resource_path(os.path.join("assets", "settings.png"))),
            dark_image=Image.open(get_resource_path(os.path.join("assets", "settings.png"))),
            size=(20, 20)
        )

        for folder in self.monitored_folders:
            folder_frame = ctk.CTkFrame(self.folders_frame, corner_radius=30, fg_color="transparent", border_width=1, border_color="#434343")
            folder_frame.pack(fill="x", pady=3, padx=5)

            folder_icon = ctk.CTkLabel(folder_frame, image=folder_icon_loaded, text="")
            folder_icon.pack(side="left", pady=14, padx=(14, 0))

            folder_label = ctk.CTkLabel(folder_frame, text=folder, font=("Arial", 12))
            folder_label.pack(side="left", pady=5, padx=5)

            settings_btn = ctk.CTkButton(
                folder_frame, image=settings_icon_loaded, text="",
                width=30, fg_color="transparent", hover_color="#181818",
                command=lambda btn=folder_label, f=folder: self.toggle_popup(btn, f)
            )
            settings_btn.pack(side="right", pady=5, padx=5)

            is_active = self.db.get_folder_status(folder)
            status_btn = ctk.CTkButton(
                folder_frame,
                image=pause_icon_loaded if is_active else play_icon_loaded,
                text=" Pause" if is_active else " Resume",
                width=70, height=32, fg_color="transparent",
                hover_color="#333", border_width=1, border_color="#F5F5F5", corner_radius=20,
                command=lambda f=folder: self.toggle_folder_status(f)
            )
            status_btn.pack(side="right", pady=0, padx=0)

            self.folder_widgets.append(folder_frame)

        
    

    def create_monitor_button(self):
        """Creates and shows the monitoring button"""
        self.monitor_button = ctk.CTkButton(self.main_view, 
                                          text="Stop monitoring folders" if self.monitoring else "Start monitoring folders", 
                                          fg_color="#ff2d55" if self.monitoring else "#28a745", 
                                          text_color="white", width=200, height=50, corner_radius=25, 
                                          font=("Arial", 12), command=self.toggle_monitoring)
        self.monitor_button.pack(pady=10, padx=10)
    
    def add_folder(self):
        folder = filedialog.askdirectory()
        if folder and folder not in self.monitored_folders:
            self.db.add_folder(folder)
            self.monitored_folders.append(folder)
            # Create monitoring button if this is the first folder
            if len(self.monitored_folders) == 1:
                self.create_monitor_button()
            self.update_folder_list_ui()
    
    def toggle_monitoring(self):
        if not self.monitor_button:
            return
        if self.monitoring:
            self.stop_monitoring()
        else:
            self.start_monitoring()
    
    def start_monitoring(self):
        if not self.monitor_button:
            return
        self.stop_monitoring()
        
        # Only include active folders
        active_folders = [folder for folder in self.monitored_folders if self.db.get_folder_status(folder)]
        
        if active_folders:  # Only create handler and organize if there are active folders
            handler = FileHandler(self.rules, active_folders)
            handler.organize_all()
            
            # Start observers for active folders
            for folder in active_folders:
                observer = Observer()
                observer.schedule(handler, folder, recursive=False)
                observer.start()
                self.observers[folder] = observer
        
        pause_icon_loaded = ctk.CTkImage(
            light_image=Image.open(get_resource_path(os.path.join("assets","pause.png"))),
            dark_image=Image.open(get_resource_path(os.path.join("assets","pause.png"))),
            size=(16, 16)
        )
        
        self.monitoring = True
        self.db.toggle_monitoring_status()
        self.monitor_button.configure(image=pause_icon_loaded, text=" Stop Monitoring", fg_color="#ff2d55")
    
    def stop_monitoring(self):
        if not self.monitor_button:
            return
        for observer in self.observers.values():
            observer.stop()
            observer.join()
        self.observers = {}
        
        self.monitoring = False
        self.db.toggle_monitoring_status()
        self.monitor_button.configure(text="Start Monitoring", fg_color="#28a745")

    def remove_folder(self, folder):
        """Removes a folder from monitoring."""
        # Stop monitoring this folder if it's active
        if folder in self.observers:
            self.observers[folder].stop()
            self.observers[folder].join()
            del self.observers[folder]
        
        # Remove from database
        self.db.remove_folder(folder)
        
        # Remove from monitored folders list
        self.monitored_folders.remove(folder)
        
        # Close the popup
        if self.popup:
            self.popup.destroy()
            self.popup = None
        
        # Remove monitoring button if no folders left
        if not self.monitored_folders and self.monitor_button:
            self.monitor_button.destroy()
            self.monitor_button = None
        
        # Update the UI
        self.update_folder_list_ui()

    def setup_rules_view(self):
        """Creates the rules management view"""
        self.rules_view = ctk.CTkFrame(self.root, fg_color="transparent")
        
        # Header with back button and title
        header = ctk.CTkFrame(self.rules_view, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(10, 20))
        
        back_icon = ctk.CTkImage(
            light_image=Image.open(get_resource_path(os.path.join("assets","arrow-left.png"))),
            dark_image=Image.open(get_resource_path(os.path.join("assets","arrow-left.png"))),
            size=(18, 18)
        )
        back_btn = ctk.CTkButton(header, image=back_icon, text=" General settings", width=30,
                                fg_color="transparent", hover_color="#181818",
                                command=self.show_main_view)
        back_btn.pack(side="left")

        # Sort by section
        self.sort_section = ctk.CTkFrame(self.rules_view, fg_color="transparent")
        self.sort_section.pack(fill="x", padx=20, pady=(0, 0))
        
        # Sort header (always visible)
        sort_header = ctk.CTkFrame(self.sort_section, fg_color="transparent")
        sort_header.pack(fill="x")
        
        sort_title = ctk.CTkLabel(sort_header, text="Sort by", font=("Arial", 16))
        sort_title.pack(side="left")
        
        # Initialize chevron icons
        self.chevron_down = ctk.CTkImage(
            light_image=Image.open(get_resource_path(os.path.join("assets","arrow-circle-down.png"))),
            dark_image=Image.open(get_resource_path(os.path.join("assets","arrow-circle-down.png"))),
            size=(16, 16)
        )
        self.chevron_up = ctk.CTkImage(
            light_image=Image.open(get_resource_path(os.path.join("assets","arrow-circle-up.png"))),
            dark_image=Image.open(get_resource_path(os.path.join("assets","arrow-circle-up.png"))),
            size=(16, 16)
        )
        
        # Create expand/collapse button
        self.sort_expand_btn = ctk.CTkButton(sort_header, image=self.chevron_up, text="", width=30,
                                            fg_color="transparent", hover_color="#181818",
                                            command=self.toggle_sort_section)
        self.sort_expand_btn.pack(side="right")
        
        # Description (always visible, left-aligned)
        sort_desc = ctk.CTkLabel(self.sort_section, text="Choose how you want to sort your files",
                                text_color="gray", font=("Arial", 12))
        sort_desc.pack(anchor="w", pady=(5, 0))
        
        # Create collapsible content container
        self.sort_content = ctk.CTkFrame(self.sort_section, fg_color="transparent")
        # Start collapsed
        # self.sort_content.pack(fill="x", pady=(0, 0))
        
        # Sort options
        filetype_option = self.create_sort_option(self.sort_content, os.path.join("assets","folder.png"), "Filetype",
                                                "Group similar filetypes together", True)
        ai_option = self.create_sort_option(self.sort_content, os.path.join("assets","magicpen.png"), "AI",
                                          "Coming soon...", False)
        
        # Separator
        separator = ctk.CTkFrame(self.rules_view, height=1, fg_color="#333")
        separator.pack(fill="x", padx=20, pady=20)
        
        # Extension manager section with database rules
        self.ext_section = ctk.CTkFrame(self.rules_view, fg_color="transparent")
        self.ext_section.pack(fill="x", padx=20, pady=10)
        
        ext_header = ctk.CTkFrame(self.ext_section, fg_color="transparent")
        ext_header.pack(fill="x")
        
        ext_title = ctk.CTkLabel(ext_header, text="Extension manager", font=("Arial", 16))
        ext_title.pack(side="left")
        
        self.ext_expand_btn = ctk.CTkButton(ext_header, image=self.chevron_up, text="", width=30,
                                           fg_color="transparent", hover_color="#181818",
                                           command=self.toggle_ext_section)
        self.ext_expand_btn.pack(side="right")
        
        ext_desc = ctk.CTkLabel(self.ext_section, text="Manage extensions and their corresponding folders",
                               text_color="gray", font=("Arial", 12))
        ext_desc.pack(anchor="w", pady=(5, 15))
        
        # Create scrollable frame for extension categories
        self.ext_content = ctk.CTkScrollableFrame(self.ext_section, fg_color="transparent", 
                                                height=150)
        # Start collapsed
        # self.ext_content.pack(fill="x", pady=(0, 0))
        
        # Organize rules by category
        self.display_categorized_rules()
        
        # Add Extension button
        self.add_ext_btn = ctk.CTkButton(self.ext_section, text="+ Add Extension",
                                   fg_color="transparent", text_color="#FF617F",
                                   hover_color="#282828",
                                   command=self.show_add_extension_dialog)
        self.add_ext_btn.pack(anchor="w", pady=10, padx=(0,0))
        # Start collapsed
        self.add_ext_btn.pack_forget()

    def display_categorized_rules(self):
        """Display rules from database organized by categories"""
        # Clear existing content
        for widget in self.ext_content.winfo_children():
            widget.destroy()
        
        # Group rules by category
        categorized_rules = {}
        
        # self.rules is a dict where key is extension and value is category
        for extension, category in self.rules.items():
            # Add dot to extension if not present
            ext = f".{extension}" if not extension.startswith('.') else extension
            
            # Initialize category list if not exists
            if category not in categorized_rules:
                categorized_rules[category] = []
            
            # Add to category (extension and folder name matches category)
            categorized_rules[category].append((ext, category))
        
        # Display each category
        for category, rules in sorted(categorized_rules.items()):
            if rules:  # Only show categories with rules
                self.create_extension_category(category, rules)

    def create_extension_category(self, category_name, rules):
        """Creates a category section with its rules"""
        # Category header
        category_frame = ctk.CTkFrame(self.ext_content, fg_color="transparent")
        category_frame.pack(fill="x", pady=(0, 10))
        
        folder_icon = ctk.CTkImage(
            light_image=Image.open(get_resource_path(os.path.join("assets","folder.png"))),
            dark_image=Image.open(get_resource_path(os.path.join("assets","folder.png"))),
            size=(20, 20)
        )
        icon_label = ctk.CTkLabel(category_frame, image=folder_icon, text="")
        icon_label.pack(side="left", padx=(0, 10))
        
        title_label = ctk.CTkLabel(category_frame, text=category_name.replace('_', ' '), 
                                  font=("Arial", 14, "bold"))
        title_label.pack(side="left")
        
        # Extensions container
        ext_container = ctk.CTkFrame(self.ext_content, fg_color="transparent")
        ext_container.pack(fill="x", padx=20)
        
        # Create rows for rules
        for extension, folder in sorted(rules):  # Sort extensions within category
            self.create_extension_row(ext_container, extension, folder)

    def create_extension_row(self, parent, extension, folder):
        """Creates a row for a single extension rule"""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=2)
        
        # Extension label
        ext_label = ctk.CTkLabel(row, text=extension, font=("Arial", 12))
        ext_label.pack(side="left")
        
        # Folder name
        folder_entry = ctk.CTkEntry(row, placeholder_text="Folder name",
                                   fg_color="#282828", border_color="#282828")
        folder_entry.insert(0, folder)
        folder_entry.pack(side="left", fill="x", expand=True, padx=10)
        
        # Save changes when folder name is changed
        folder_entry.bind('<FocusOut>', 
                         lambda e, ext=extension: self.update_rule_folder(ext, 
                                                                    folder_entry.get()))
        
        # Delete button
        delete_icon = ctk.CTkImage(
            light_image=Image.open(get_resource_path(os.path.join("assets","minus-circle.png"))),
            dark_image=Image.open(get_resource_path(os.path.join("assets","minus-circle.png"))),
            size=(20, 20)
        )
        delete_btn = ctk.CTkButton(row, image=delete_icon, text="", width=30,
                                  fg_color="transparent", hover_color="#181818",
                                  command=lambda: self.delete_rule(extension, row))
        delete_btn.pack(side="right")

    def show_rules_view(self):
        """Switch to rules management view"""
        if not self.rules_view:
            self.setup_rules_view()
        self.main_view.pack_forget()
        self.rules_view.pack(fill="both", expand=True)
        if self.popup:
            self.popup.destroy()
            self.popup = None

    def show_main_view(self):
        """Switch back to main view"""
        if self.rules_view:
            self.rules_view.pack_forget()
        self.main_view.pack(fill="both", expand=True)

    def toggle_popup(self, button, folder):
        """Shows a small popup menu near the clicked settings button."""
        if self.popup and self.popup.winfo_exists():
            self.popup.destroy()
            self.popup = None
            return
        
        # Create popup
        self.popup = ctk.CTkToplevel(self.root)
        self.popup.overrideredirect(True)
        self.popup.geometry("180x100")
        self.popup.configure(corner_radius=16)
        
        # Position the popup near the clicked button
        x = self.root.winfo_x() + button.winfo_rootx() - self.root.winfo_rootx() + 170
        y = self.root.winfo_y() + button.winfo_rooty() - self.root.winfo_rooty() + 60
        self.popup.geometry(f"+{x}+{y}")

        # Update the profile button to call show_rules_view
        profile_button = ctk.CTkButton(self.popup, text="Manage custom rules", 
                                     corner_radius=15, command=self.show_rules_view,
                                     anchor="w", fg_color="#1F1F1F", text_color="#FFFFFF", hover_color="#1F1F1F", height=35)
        profile_button.pack(pady=10, padx=10, fill="x")

        settings_button = ctk.CTkButton(self.popup, text="Remove folder", 
                                      fg_color="transparent", text_color="#FF3B30",
                                      command=lambda: self.remove_folder(folder),
                                      anchor="w")
        settings_button.pack(pady=10, padx=10, fill="x")

        # Close popup when clicking outside
        self.popup.bind("<FocusOut>", lambda event: self.popup.destroy())
        self.popup.focus_force()

    def toggle_folder_status(self, folder):
        current_status = self.db.get_folder_status(folder)
        new_status = not current_status
        
        if new_status:  # Resuming monitoring
            if self.monitoring:  # Only start observer if global monitoring is active
                handler = FileHandler(self.rules, [folder])
                observer = Observer()
                observer.schedule(handler, folder, recursive=False)
                observer.start()
                self.observers[folder] = observer
        else:  # Pausing monitoring
            if folder in self.observers:
                self.observers[folder].stop()
                self.observers[folder].join()
                del self.observers[folder]
        
        self.db.set_folder_status(folder, new_status)
        self.update_folder_list_ui()
    
    def toggle_sort_section(self):
        """Toggle the visibility of the sort section content"""
        try:
            if self.sort_content.winfo_viewable():
                self.sort_content.pack_forget()
                self.sort_expand_btn.configure(image=self.chevron_down)
            else:
                self.sort_content.pack(fill="x", pady=(5, 0))
                self.sort_expand_btn.configure(image=self.chevron_up)
        except Exception as e:
            print(f"Error toggling sort section: {str(e)}")

    def toggle_ext_section(self):
        """Toggle the visibility of the extension manager section content"""
        try:
            if self.ext_content.winfo_viewable():
                self.ext_content.pack_forget()
                self.add_ext_btn.pack_forget()
                self.ext_expand_btn.configure(image=self.chevron_down)
            else:
                self.ext_content.pack(fill="x", pady=(5, 0))
                self.add_ext_btn.pack(pady=10)
                self.ext_expand_btn.configure(image=self.chevron_up)
        except Exception as e:
            print(f"Error toggling extension section: {str(e)}")

    def show_add_extension_dialog(self):
        """Shows dialog to add new extension"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Add Extension")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        
        # Extension input
        ext_label = ctk.CTkLabel(dialog, text="Extension (e.g., pdf):")
        ext_label.pack(pady=(20, 5))
        ext_entry = ctk.CTkEntry(dialog)
        ext_entry.pack(pady=5, padx=20, fill="x")
        
        # Folder input
        folder_label = ctk.CTkLabel(dialog, text="Folder name:")
        folder_label.pack(pady=(10, 5))
        folder_entry = ctk.CTkEntry(dialog)
        folder_entry.pack(pady=5, padx=20, fill="x")
        
        # Add button
        def add_extension():
            ext = ext_entry.get().strip()
            folder = folder_entry.get().strip()
            if ext and folder:
                if not ext.startswith('.'):
                    ext = '.' + ext
                self.add_new_rule(ext, folder)
                dialog.destroy()
        
        add_btn = ctk.CTkButton(dialog, text="Add", command=add_extension)
        add_btn.pack(pady=20)

    def add_new_rule(self, extension, folder):
        """Adds a new rule to the database and updates UI"""
        # Add to database
        self.db.add_rule(extension, folder)
        
        # Refresh rules from database
        self.rules = self.db.fetch_rules()
        
        # Refresh the display
        self.display_categorized_rules()

    def update_rule_folder(self, extension, new_folder):
        """Updates the folder for an existing rule"""
        self.db.update_rule_folder(extension, new_folder)
        self.rules = self.db.fetch_rules()

    def delete_rule(self, extension, row):
        """Deletes a rule from the database and UI"""
        self.db.delete_rule(extension)
        self.rules = self.db.fetch_rules()
        row.destroy()

    def create_sort_option(self, parent, icon_name, title, description, active=False):
        """Creates a sort option row"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=5)
        
        try:
            icon = ctk.CTkImage(
                light_image=Image.open(get_resource_path(icon_name)),
                dark_image=Image.open(get_resource_path(icon_name)),
                size=(20, 20)
            )
            icon_label = ctk.CTkLabel(frame, image=icon, text="")
            icon_label.pack(side="left", padx=(0, 10))
        except Exception as e:
            print(f"Error loading icon {icon_name}: {str(e)}")
            # Create empty space instead of icon if loading fails
            spacer = ctk.CTkFrame(frame, width=20, fg_color="transparent")
            spacer.pack(side="left", padx=(0, 10))
        
        text_frame = ctk.CTkFrame(frame, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)
        
        title_label = ctk.CTkLabel(text_frame, text=title, font=("Arial", 14))
        title_label.pack(anchor="w")
        
        desc_label = ctk.CTkLabel(text_frame, text=description,
                                 text_color="gray", font=("Arial", 12))
        desc_label.pack(anchor="w")
        
        if active:
            try:
                check_icon = ctk.CTkImage(
                    light_image=Image.open(get_resource_path(os.path.join("assets","tick-circle.png"))),
                    dark_image=Image.open(get_resource_path(os.path.join("assets","tick-circle.png"))),
                    size=(20, 20)
                )
                check_label = ctk.CTkLabel(frame, image=check_icon, text="")
                check_label.pack(side="right")
            except Exception as e:
                print(f"Error loading tick icon: {str(e)}")
        
        return frame


if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()
