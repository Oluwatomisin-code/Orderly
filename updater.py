import requests
import os
import zipfile
import shutil
from tkinter import messagebox

class Updater:
    def __init__(self, repo_owner, repo_name, current_version):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = current_version
        self.releases_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    def check_for_update(self):
        try:
            response = requests.get(self.releases_url)
            response.raise_for_status()
            latest_release = response.json()
            latest_version = latest_release["tag_name"]
            if self.is_newer_version(latest_version):
                return {
                    "update_available": True,
                    "latest_version": latest_version,
                    "download_url": latest_release["assets"][0]["browser_download_url"]
                }
            return {"update_available": False}
        except requests.RequestException as e:
            print(f"Error checking for updates: {e}")
            return {"update_available": False}

    def is_newer_version(self, latest_version):
        def version_tuple(version):
            return tuple(map(int, version.split(".")))

        return version_tuple(latest_version) > version_tuple(self.current_version)

    def download_and_apply_update(self, download_url, target_dir):
        try:
            response = requests.get(download_url, stream=True)
            response.raise_for_status()

            zip_path = os.path.join(target_dir, "update.zip")
            with open(zip_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(target_dir)

            os.remove(zip_path)
            messagebox.showinfo("Update Complete", "The app has been updated. Please restart.")
        except Exception as e:
            print(f"Error applying update: {e}")
            messagebox.showerror("Update Failed", "Could not update the application.")
