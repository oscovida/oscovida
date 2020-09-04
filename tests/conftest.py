import os
from unittest import mock

import pytest

import oscovida.covid19dh


@pytest.fixture()
def fresh_cache(tmp_path):
    cache_dir = os.path.join(tmp_path, "cache_dir")
    with mock.patch('oscovida.covid19dh.CACHE_DIR', cache_dir):
        return oscovida.covid19dh.Cache()


@pytest.fixture(scope="session")
def reused_cache(tmp_path_factory):
    cache_dir = tmp_path_factory.mktemp("cache_dir")
    with mock.patch('oscovida.covid19dh.CACHE_DIR', cache_dir):
        return oscovida.covid19dh.Cache()
