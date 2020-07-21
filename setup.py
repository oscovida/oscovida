#!/usr/bin/env python
import os.path as osp
import re
from setuptools import setup, find_packages
import sys


def get_script_path():
    return osp.dirname(osp.realpath(sys.argv[0]))


def read(*parts):
    return open(osp.join(get_script_path(), *parts)).read()


def find_version(*parts):
    vers_file = read(*parts)
    match = re.search(r'^__version__ = "(\d+\.\d+\.\d+)"', vers_file, re.M)
    if match is not None:
        return match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="oscovida",
    version=find_version("oscovida", "__init__.py"),
    author="European XFEL GmbH",
    author_email="da-support@xfel.eu",
    maintainer="Hans Fangohr",
    url="https://github.com/oscovida/oscovida",
    description="Coronavirus-2020",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    license="BSD-3-Clause",
    packages=find_packages(),
    install_requires=[
        "click==7.*,>=7.1.2",
        "ipynb-py-convert==0.*,>=0.4.5",
        "ipywidgets==7.*,>=7.5.1",
        "joblib==0.*,>=0.16.0",
        "markdown==3.*,>=3.2.2",
        "matplotlib<3.3",
        "numpy==1.*,>=1.19.0",
        "pandas==1.*,>=1.0.5",
        "pelican==4.*,>=4.2.0",
        "pelican-jupyter==0.*,>=0.10.0",
        "scipy==1.*,>=1.5.1",
        "seaborn==0.*,>=0.10.1",
        "tabulate==0.*,>=0.8.7",
        "tqdm==4.*,>=4.48.0",
        "voila==0.*,>=0.1.21",
    ],
    extras_require={
        "test": [
            "black==19.*,>=19.10.0.b0",
            "coverage==5.*,>=5.2.0",
            "mypy==0.*,>=0.782.0",
            "nbval==0.*,>=0.9.5",
            "pycodestyle==2.*,>=2.6.0",
            "pytest==5.*,>=5.4.3",
            "pytest-cov==2.*,>=2.10.0",
            "testpath==0.*,>=0.4.4",
        ]
    },
    python_requires=">=3.6.7",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
)
