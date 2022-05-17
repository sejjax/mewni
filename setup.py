from setuptools import setup
import shutil
import pathlib

setup(
    name='muni',
    version='0.1.0',
    packages=['muni'],
    install_requires=[
        'click >= 8.1.3',
    ],
)

shutil.copy(pathlib.Path().parent.joinpath('muni/cli/ni.py'), '/usr/local/bin/ni')