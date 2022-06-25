import os
import pathlib
import shutil

def get_root():
    return pathlib.Path(os.getcwd()).parent.parent.resolve()

def get_tmp():
    TMP_FOLDER = '.tmp'
    return pathlib.Path(get_root()).joinpath(TMP_FOLDER).resolve()

def go_tmp():
    return os.chdir(get_tmp())

def go_root():
    os.chdir(get_root())

def prepare():
    try:
        os.mkdir(get_tmp())
    except FileExistsError:
        pass


def clean():
    try:
        shutil.rmtree(get_tmp())
    except FileExistsError:
        pass

def prepare_workspace():
    def wrapper():
        pass

    return wrapper