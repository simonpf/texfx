from setuptools import setup, find_packages
from os import path

setup(
    name='texfx',  # Required
    version='0.0',  # Required
    description='Extract and rename image files from .tex documents.',
    author='Simon Pfreundschuh',  # Optional
    packages=["texfx"],
    python_requires='>=3.6',
    scripts=['bin/texfx'],
    project_urls={'Source': 'https://github.com/simonpf/texxf/'}
)
