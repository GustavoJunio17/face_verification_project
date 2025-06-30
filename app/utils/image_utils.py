import os
import shutil

def save_uploaded_image(upload_file, path: str):
    with open(path, "wb") as f:
        shutil.copyfileobj(upload_file.file, f)

def remove_file_if_exists(path: str):
    if os.path.exists(path):
        os.remove(path)