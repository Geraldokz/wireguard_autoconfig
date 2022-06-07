import os

from config import WORK_DIR


def create_project_folder(project_name: str) -> None:
    """Создает папку проекта. Если папка существует взводит исключение"""
    folder_path = f'{WORK_DIR}/{project_name}'
    try:
        os.mkdir(folder_path)
    except FileExistsError:
        print(f'WARNING! Folder {folder_path} already exists')
