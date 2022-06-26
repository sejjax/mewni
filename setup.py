from setuptools import setup, find_packages

setup(
    name='mewni',
    version='0.1.7',
    packages=find_packages(),
    install_requires=[
        'click >= 8.1.3',
        'aiogram >= 2.2.0',
        'aioredis >= 2.0.1',
        'environs >= 9.5.0',
        'peewee >= 3.14.10',
        'werkzeug >= 2.1.2',
        'aioschedule >= 0.5.2'
    ],
    entry_points={
        'console_scripts': [
            'mewni = mewni.cli.cli:main',
            'ni = mewni.cli.cli:main',
        ],
    },
    include_package_data=True
)