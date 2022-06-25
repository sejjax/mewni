import glob
import pathlib
import shutil
import hashlib


def check_tree_identity(path_a, path_b) -> bool:
    path_a = pathlib.Path(path_a)
    path_b = pathlib.Path(path_b)
    # If paths is not absolute then make it absolute
    if not path_a.is_absolute():
        path_a = path_a.resolve()
    if not path_b.is_absolute():
        path_b = path_b.resolve()

    # Get all nodes in subtrees
    items_a = glob.glob('**', root_dir=path_a, recursive=True)
    items_b = glob.glob('**', root_dir=path_b, recursive=True)
    # Compare number of nodes in subtree
    if len(items_a) != len(items_b):
        return False
    for item_a, item_b in zip(items_a, items_b):
        # Compare names of node
        if item_a != item_b:
            return False
        item_a = pathlib.Path(path_a).joinpath(item_a).resolve()
        item_b = pathlib.Path(path_b).joinpath(item_b).resolve()
        # If nodes is a dirrectory the skip data reading
        if item_a.is_dir() and item_b.is_dir():
            continue
        with open(item_a, 'rb') as f_a:
            data_a = f_a.read()
        with open(item_b, 'rb') as f_b:
            data_b = f_b.read()
        hash_a = hashlib.md5(data_a).digest()
        hash_b = hashlib.md5(data_b).digest()
        if hash_a != hash_b:
            return False
    return True
