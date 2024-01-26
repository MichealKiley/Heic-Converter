from pathlib import Path


# sends absolute path to heic route in order to send converted files
def temp_file_path():
    file_path = str(Path(__file__).parent).replace("\\", "/")
    return file_path