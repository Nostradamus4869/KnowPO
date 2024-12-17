import os
BASE_DIR = os.getcwd()
LOG_DIR = os.join(BASE_DIR,"logs")
DATA_DIR = os.join(BASE_DIR,"data")

def get_path(dataset, path_type):
    allowed_paths = ['raw', 'tmp', 'processed', 'sft', 'dpo']
    
    if path_type not in allowed_paths:
        raise ValueError(f"Invalid path_type. Choose from: {', '.join(allowed_paths)}")
    
    return os.path.join(DATA_DIR, dataset, path_type)