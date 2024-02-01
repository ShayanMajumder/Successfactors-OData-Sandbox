# setup.py
from setuptools import setup, find_packages

setup(
    name='odata_metadata_sandbox',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'xmltodict',  # Include any other dependencies
    ],
)
