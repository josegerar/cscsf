import os
import sys
from pathlib import Path
from app.settings import BASE_DIR

BASE_REPOSITORY = '\\static\\repository\\'


def get_content_folder(path):
    return os.listdir(str(BASE_DIR) + path)


# def get_path_root_repository():
#     return os.path.join(get_path_root(), 'static/repository')

def rearm_url(array, exclude_quant):
    url = "\\"
    for idx, val in enumerate(array):
        if idx < (len(array) - exclude_quant):
            if len(val) > 0:
                url += val + "\\"
    return url
