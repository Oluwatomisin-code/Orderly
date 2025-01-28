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
    ".raw": "Images",
    
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
