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
          # List of dependencies as of 27 March. Replace with frozen set
          # to keep system more stable towards changes in dependencies.
          #
          # See https://github.com/oscovida/oscovida/issues/301
          # 'joblib',
          # 'pandas',
          # 'seaborn',
          # 'matplotlib',
          # 'markdown',
          # 'openpyxl',
          # 'numpy',
          # 'scipy',
          # 'pelican',
          # 'pelican-jupyter',
          # 'seaborn',
          # 'tabulate<0.8.8',  # Pinned until release with https://github.com/astanin/python-tabulate/pull/111 is made
          # 'tqdm',
          # 'ipywidgets',
          # 'ipynb_py_convert',
          # 'Jinja2==3.0.3',   # Pinned to address https://github.com/oscovida/oscovida/issues/300
          # 'click',
          # 'pytest_tornasync',
          # 'nbconvert>=6.0.0',
          # 'plotly',
          #
          # Frozen set:
          'appnope==0.1.2',
          'argon2-cffi==21.1.0',
          'attrs==21.2.0',
          'backcall==0.2.0',
          'bleach==4.1.0',
          'blinker==1.4',
          'cffi==1.15.0',
          'click==8.0.3',
          'colorama==0.4.4',
          'commonmark==0.9.1',
          'coverage==6.1.2',
          'cycler==0.11.0',
          'debugpy==1.5.1',
          'decorator==5.1.0',
          'defusedxml==0.7.1',
          'docutils==0.18',
          'entrypoints==0.3',
          'et-xmlfile==1.1.0',
          'feedgenerator==2.0.0',
          'iniconfig==1.1.1',
          'ipykernel==6.5.0',
          'ipynb-py-convert==0.4.6',
          'ipython==7.29.0',
          'ipython-genutils==0.2.0',
          'ipywidgets==7.6.5',
          'jedi==0.18.0',
          'Jinja2==3.0.3',
          'joblib==1.1.0',
          'jsonschema==4.2.1',
          'jupyter-client==7.0.6',
          'jupyter-core==4.9.1',
          'jupyterlab-pygments==0.1.2',
          'jupyterlab-widgets==1.0.2',
          'kiwisolver==1.3.2',
          'Markdown==3.3.4',
          'MarkupSafe==2.0.1',
          'matplotlib==3.4.3',
          'matplotlib-inline==0.1.3',
          'mistune==0.8.4',
          'nbclient==0.5.5',
          'nbconvert==5.6.1',
          'nbformat==5.1.3',
          'nbval==0.9.6',
          'nest-asyncio==1.5.1',
          'notebook==6.4.5',
          'numpy==1.21.4',
          'openpyxl==3.0.9',
          'packaging==21.2',
          'pandas==1.3.4',
          'pandocfilters==1.5.0',
          'parso==0.8.2',
          'pelican==4.7.1',
          'pelican-jupyter==0.10.1',
          'pexpect==4.8.0',
          'pickleshare==0.7.5',
          'Pillow==8.4.0',
          'plotly==5.3.1',
          'pluggy==1.0.0',
          'prometheus-client==0.12.0',
          'prompt-toolkit==3.0.22',
          'ptyprocess==0.7.0',
          'py==1.11.0',
          'pycodestyle==2.8.0',
          'pycparser==2.21',
          'Pygments==2.10.0',
          'pyparsing==2.4.7',
          'pyrsistent==0.18.0',
          'pytest==6.2.5',
          'pytest-cov==3.0.0',
          'pytest-tornasync==0.6.0.post2',
          'python-dateutil==2.8.2',
          'pytz==2021.3',
          'pyzmq==22.3.0',
          'rich==10.13.0',
          'scipy==1.7.2',
          'seaborn==0.11.2',
          'Send2Trash==1.8.0',
          'six==1.16.0',
          'tabulate==0.8.7',
          'tenacity==8.0.1',
          'terminado==0.12.1',
          'testpath==0.5.0',
          'toml==0.10.2',
          'tornado==6.1',
          'tqdm==4.62.3',
          'traitlets==5.1.1',
          'Unidecode==1.3.2',
          'wcwidth==0.2.5',
          'webencodings==0.5.1',
          'widgetsnbextension==3.5.2'
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
