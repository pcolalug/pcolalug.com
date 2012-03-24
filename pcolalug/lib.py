import os

def get_data_dir():
    local_path = os.path.join(os.path.dirname(__file__), 'data')

    path = os.path.abspath(os.environ.get("EPIO_DATA_DIRECTORY", local_path))

    path = os.path.abspath(os.environ.get("OPENSHIFT_DATA_DIR", local_path))

    return path
