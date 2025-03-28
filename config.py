import os

DEFAULT_RULES = {
    # Images
    "jpg": "Images",
    "jpeg": "Images",
    "png": "Images",
    "gif": "Images",
    "bmp": "Images",
    "tiff": "Images",
    "webp": "Images",
    "svg": "Images",
    "raw": "Images",
    "heic": "Images",
    
    # Documents
    "pdf": "Documents",
    "doc": "Documents",
    "docx": "Documents",
    "xls": "Documents",
    "xlsx": "Documents",
    "ppt": "Documents",
    "pptx": "Documents",
    "txt": "Documents",
    "rtf": "Documents",
    "odt": "Documents",
    "epub": "Documents",
    
    # Videos
    "mp4": "Videos",
    "avi": "Videos",
    "mkv": "Videos",
    "mov": "Videos",
    "flv": "Videos",
    "wmv": "Videos",
    "webm": "Videos",
    
    # Audios
    "mp3": "Audios",
    "wav": "Audios",
    "aac": "Audios",
    "ogg": "Audios",
    "flac": "Audios",
    "wma": "Audios",
    "m4a": "Audios",
    
    # Compressed/Archives
    "zip": "Archives",
    "rar": "Archives",
    "7z": "Archives",
    "tar": "Archives",
    "gz": "Archives",
    "bz2": "Archives",
    "xz": "Archives",
    
    # Code/Executables
    "exe": "Executables",
    "msi": "Executables",
    "sh": "Scripts",
    "py": "Scripts",
    "js": "Scripts",
    "html": "Web_Files",
    "css": "Web_Files",
    "php": "Web_Files",
    "java": "Code_Files",
    "cpp": "Code_Files",
    "c": "Code_Files",
    "cs": "Code_Files",
    "rb": "Code_Files",
    "go": "Code_Files",
    "ts": "Code_Files",
    
    # Miscellaneous
    "iso": "Disk_Images",
    "dmg": "Disk_Images",
    "apk": "Apps",
    "ipa": "Apps",
    "torrent": "Torrents",
}

DEFAULT_FOLDERS = [
    os.path.join(os.path.expanduser("~"), "Downloads"),
    os.path.join(os.path.expanduser("~"), "Documents"),
]

# Default extension categories and their extensions
DEFAULT_CATEGORIES = {
    "Audio": {
        "extensions": [".mp3", ".wav", ".flac", ".m4a", ".aac"],
        "folder": "Audio"
    },
    "Video": {
        "extensions": [".mp4", ".mov", ".avi", ".mkv", ".wmv"],
        "folder": "Video"
    },
    "Images": {
        "extensions": [".jpg", ".png", ".gif", ".bmp", ".webp"],
        "folder": "Images"
    },
    "Documents": {
        "extensions": [".pdf", ".doc", ".docx", ".txt", ".rtf"],
        "folder": "Documents"
    },
    "Archives": {
        "extensions": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "folder": "Archives"
    }
}

# Function to get extension category
def get_category_for_extension(extension):
    """Returns the category name for a given extension"""
    for category, data in DEFAULT_CATEGORIES.items():
        if extension.lower() in data["extensions"]:
            return category
    return "Other"

# Function to get default folder name for extension
def get_default_folder(extension):
    """Returns the default folder name for a given extension"""
    category = get_category_for_extension(extension)
    return DEFAULT_CATEGORIES.get(category, {}).get("folder", "Other")
