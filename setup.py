# Always prefer setuptools over distutils
from pathlib import Path

from setuptools import setup, find_packages

here = Path(__file__).parent.absolute()

# Get the long description from the README file
with open(here / Path('requirements.txt')) as f:
    requirements = f.read().split("\n")

setup(
    name='projet_shazam',
    version='1.0',
    description='Audio fingerprinting and recognition algorithm implemented in Python',
    url='https://github.com/charlesbacq/Shazam.git',
    author='Team Shazam TDLOG',
    license="MIT",
    packages=find_packages(exclude=['docs', 'tests']),
    setup_requires=['setuptools>=38.6.0'],  # >38.6.0 needed for markdown README.md
    install_requires=requirements,
    extras_require={
        "tests": [
            "pytest",
        ],
    }
)