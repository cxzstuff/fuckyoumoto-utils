import os
import subprocess

PRELOADER = "preloader_penangf.bin"
LOADER = "MT6768_USER.bin"

PATH = "./sources"
ALTERNATIVE_PATH = "./scripts/sources"

def get_file_path(file_name):
    """
    Ищет файл сначала в основной директории, затем в альтернативной.
    Если файл найден, возвращает его путь. В противном случае возвращает None.
    """
    path = os.path.join(PATH, file_name)
    if os.path.isfile(path):
        return path

    # Если файл не найден в основной директории, ищем в альтернативной
    alternative_path = os.path.join(ALTERNATIVE_PATH, file_name)
    if os.path.isfile(alternative_path):
        print(f"File {file_name} not found in main path, using alternative path: {alternative_path}")
        return alternative_path

    print(f"Error: {file_name} not found in both source and alternative paths.")
    return None

def print_gpt():
    preloader_path = get_file_path(PRELOADER)
    loader_path = get_file_path(LOADER)

    if not preloader_path or not loader_path:
        print("Error: Required files not found")
        return

    try:
        subprocess.run(
            ["mtk", "printgpt",
             "--preloader", preloader_path, "--loader", loader_path],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to print gpt partitions")
        print(f"Error details: {e.stderr.decode()}")