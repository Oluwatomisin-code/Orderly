import sqlite3
import os
import platform
from config import DEFAULT_RULES, DEFAULT_FOLDERS
import logging
import sys

def get_resource_path(relative_path):
    """Get the correct resource path for both development and bundled app"""
    if getattr(sys, 'frozen', False):
        # Running in a bundle
        base_path = sys._MEIPASS
    else:
        # Running in development
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class DBHandler:
    def __init__(self, db_name="orderly.db"):
        # Determine appropriate app data directory
        if platform.system() == "Darwin":  # macOS
            app_data_dir = os.path.expanduser("~/Library/Application Support/Orderly")
        elif platform.system() == "Windows":
            app_data_dir = os.path.join(os.getenv("APPDATA"), "Orderly")
        else:  # Linux and others
            app_data_dir = os.path.expanduser("~/.orderly")
            
        # Create app data directory if it doesn't exist
        os.makedirs(app_data_dir, exist_ok=True)
        logging.debug(f"Creating database directory at: {app_data_dir}")
        
        # Set up database path
        self.db_name = os.path.join(app_data_dir, db_name)
        logging.debug(f"Database path: {self.db_name}")
        
        # Initialize database connection
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        # self.reset_database()
        self.insert_default_data()
    
    def reset_database(self):
        """Drop all tables and recreate them."""
        self.cursor.execute("DROP TABLE IF EXISTS rules;")
        self.cursor.execute("DROP TABLE IF EXISTS settings;")
        self.cursor.execute("DROP TABLE IF EXISTS folders;")
        self.conn.commit()
        self.create_tables()


    def create_tables(self):
        """Create tables if they do not exist."""
        
        # Rules Table (for file type categorization)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                extension TEXT UNIQUE,
                category TEXT
            )
        """)

        # Settings Table (for future general settings)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE,
                value TEXT
            )
        """)

        # Folders Table (for monitored directories)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS folders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT UNIQUE,
                status INTEGER DEFAULT 1
            )
        """)

        self.conn.commit()

    def insert_default_data(self):
        """Insert default rules and folders into the database."""
        
        # Insert default rules into rules table
        for ext, category in DEFAULT_RULES.items():
            self.cursor.execute("""
                INSERT OR IGNORE INTO rules (extension, category) VALUES (?, ?)
            """, (ext, category))

        # Insert default folders into folders table
        for folder in DEFAULT_FOLDERS:
            self.cursor.execute("""
                INSERT OR IGNORE INTO folders (path) VALUES (?)
            """, (folder,))

        self.conn.commit()

    def fetch_folders(self):
        """Fetch all monitored folders."""
        self.cursor.execute("SELECT path FROM folders")
        return [row[0] for row in self.cursor.fetchall()]

    def add_folder(self, folder_path):
        """Add a new folder if it doesn't already exist."""
        self.cursor.execute("INSERT OR IGNORE INTO folders (path) VALUES (?)", (folder_path,))
        self.conn.commit()

    def remove_folder(self, folder_path):
        """Remove a folder from the database."""
        self.cursor.execute("DELETE FROM folders WHERE path = ?", (folder_path,))
        self.conn.commit()
    
    def get_folder_status(self, folder_path):
        """Check if a folder is active (1) or paused (0)."""
        self.cursor.execute("SELECT status FROM folders WHERE path = ?", (folder_path,))
        result = self.cursor.fetchone()
        return result[0] == 1 if result else False

    def set_folder_status(self, folder_path, is_active):
        """Update folder monitoring status in the database."""
        status = 1 if is_active else 0
        self.cursor.execute("UPDATE folders SET status = ? WHERE path = ?", (status, folder_path))
        self.conn.commit()


    def fetch_rules(self):
        """Fetch all file extension rules."""
        self.cursor.execute("SELECT extension, category FROM rules")
        return dict(self.cursor.fetchall())  # Returns a dictionary { "jpg": "Images", "pdf": "Documents" }
    
    def fetch_monitoring_status(self):
        """Get the current monitoring status from the database."""
        self.cursor.execute("SELECT value FROM settings WHERE key = 'monitoring_status'")
        result = self.cursor.fetchone()
        print(result,'status from db')
        return result[0] == "true" if result else False  # Convert "true"/"false" to boolean

    
    def toggle_monitoring_status(self):
        """Toggle monitoring status and return new status."""
        current_status = self.fetch_monitoring_status()
        new_status = "true" if not current_status else "false"

        self.cursor.execute("""
            UPDATE settings SET value = ? WHERE key = 'monitoring_status'
        """, (new_status,))
        
        self.conn.commit()
        return new_status == "true"  # Return boolean

    def close(self):
        """Close the database connection."""
        self.conn.close()

    def add_rule(self, extension, folder):
        """Adds a new extension rule"""
        cursor = self.conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO rules (extension, folder) VALUES (?, ?)',
                      (extension.lower(), folder))
        self.conn.commit()

    def update_rule_folder(self, extension, new_folder):
        """Updates the folder for an existing rule"""
        cursor = self.conn.cursor()
        cursor.execute('UPDATE rules SET folder = ? WHERE extension = ?',
                      (new_folder, extension.lower()))
        self.conn.commit()

    def delete_rule(self, extension):
        """Deletes a rule"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM rules WHERE extension = ?', (extension.lower(),))
        self.conn.commit()
