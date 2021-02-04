import os
from app.settings import BASE_DIR
from django.core.files.storage import default_storage, FileSystemStorage


def create_folder(name_folder, folder_parent):
    os.makedirs(str(BASE_DIR) + folder_parent + name_folder)

def create_file(file, folder_parent):
    path = default_storage.save(str(BASE_DIR) + folder_parent + file.name, file)
    return path