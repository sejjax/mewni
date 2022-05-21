from setuptools import setup

setup(
    name='muni',
    version='0.1.3',
    packages=['muni'],
    install_requires=[
        'click >= 8.1.3',
        'aiogram >= 2.2.0',
        'aioredis >= 2.0.1',
        'environs >= 9.5.0',
        'peewee >= 3.14.10'
    ],
    scripts=[
        'bin/ni',
        'bin/muni'
    ],
    include_package_data=True
)