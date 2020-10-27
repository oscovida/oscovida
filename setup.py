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


setup(name="oscovida",
      version=find_version("oscovida", "__init__.py"),
      author="European XFEL GmbH",
      author_email="da-support@xfel.eu",
      maintainer="Hans Fangohr",
      url="https://github.com/oscovida/oscovida",
      description="Coronavirus-2020",
      long_description=read("README.md"),
      long_description_content_type='text/markdown',
      license="BSD-3-Clause",
      packages=find_packages(),
      install_requires=[
          'joblib',
          'pandas',
          'seaborn',
          'matplotlib<3.3',
          'markdown',
          'openpyxl',
          'numpy',
          'scipy',
          'voila',
          'pelican',
          'pelican-jupyter',
          'seaborn',
          'tabulate',
          'tqdm',
          'ipywidgets',
          'ipynb_py_convert',
          'click',
          'nbconvert==5.*,<6',
      ],
      extras_require={
          'test': [
              'pytest',
              'pytest-cov',
              'coverage',
              'nbval',
              'testpath',
              'pycodestyle',
          ]
      },
      python_requires='>=3.6',
      classifiers=[
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering :: Information Analysis',
      ]
)
