import os


def create_folder(folder_path: str) -> None:
    """Создает папку проекта. Если папка существует взводит исключение"""
    folder_path = folder_path
    try:
        os.mkdir(folder_path)
    except FileExistsError:
        print(f'WARNING! Folder {folder_path} already exists')
