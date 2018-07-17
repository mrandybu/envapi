import os


def get_root_path(file):
    path_to_file = os.path.join(os.path.dirname(__file__), file)
    return path_to_file
