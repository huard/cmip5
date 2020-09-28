#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup

NAME = "cmip5"
DESCRIPTION = "CMIP5 utility functions."
URL = "https://github.com/huard/cmip5"
AUTHOR = "David Huard"
AUTHOR_EMAIL = "huard.david@ouranos.ca"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.3"
LICENSE = "Apache Software License 2.0"

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "numpy>=1.16",
    "netCDF4>=1.4",
]

KEYWORDS = "ESM CMIP5"

setup(
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
    ],
    description=DESCRIPTION,
    python_requires=REQUIRES_PYTHON,
    install_requires=requirements,
    license=LICENSE,
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    keywords=KEYWORDS,
    name=NAME,
    packages=find_packages(),
    url=URL,
    version=VERSION,
    zip_safe=False,
)


