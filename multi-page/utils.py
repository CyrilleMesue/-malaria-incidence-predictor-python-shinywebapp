import pickle

def load_object(file_path):
    """
    load sklearn model obejct
    """
    with open(file_path, "rb") as file_obj:
        return pickle.load(file_obj)