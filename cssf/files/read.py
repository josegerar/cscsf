import os
import sys
from pathlib import Path
from app.settings import BASE_DIR

BASE_REPOSITORY = '\\static\\repository\\'

def get_content_folder(path):
    return os.listdir(str(BASE_DIR) + path)

# def get_path_root_repository():
#     return os.path.join(get_path_root(), 'static/repository')
