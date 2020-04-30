"""Package Configuration for AIbbeyRoad."""

from setuptools import setup

setup(
    name='ai_road',
    version='0.0.0',
    packages=['ai_road'],
    include_package_data=True,
    install_requires=[
        'numpy==1.18.1',
        'matplotlib',
        'torch',
        'tqdm',
        'bs4',
        'pandas',
        'selenium',
        'flask',
        'rauth'
    ],
)
