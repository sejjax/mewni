from setuptools import setup

setup(
    name='mewni',
    version='0.1.7',
    packages=['mewni'],
    install_requires=[
        'click >= 8.1.3',
        'aiogram >= 2.2.0',
        'aioredis >= 2.0.1',
        'environs >= 9.5.0',
        'peewee >= 3.14.10',
        'werkzeug >= 2.1.2',
        'aioschedule >= 0.5.2'
    ],
    scripts=[
        'bin/ni',
        'bin/mewni'
    ],
    include_package_data=True
)