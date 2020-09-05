import os
from unittest import mock

import pytest

import oscovida.covid19dh


def pytest_addoption(parser):
    #  This tells the `mock_cache_dir` fixture to set the cache directory
    #  to a static location instead of a temporary one. With this enabled
    #  the data files can be reused and do not have to be downloaded, this
    #  means that the download tests are no longer performed but that the
    #  tests can run much faster. Useful for mutation testing
    parser.addoption("--static-cache", action="store_true", default=False)
    parser.addoption("--disable-level-3", action="store_true", default=False)


@pytest.fixture()
def mock_cache_dir_fresh(tmp_path):
    cache_dir = os.path.join(tmp_path, "cache_dir")
    with mock.patch('oscovida.covid19dh.CACHE_DIR', cache_dir):
        #  The default `cache` argument for `oscovida.covid19dh.get` is the
        #  function call `Cache()`. This is usually desired as it means that
        #  the cache is initialised once when the module is loaded, and then
        #  reused for any calls of `get`. However this makes testing more
        #  difficult, as we have to mock the cache object in get's __defaults__
        #  when we mock the `CACHE_DIR` constant as well. I'd rather have
        #  the test be a bit odd than change the functionality of `get`
        defaults = list(oscovida.covid19dh.get.__defaults__)
        defaults[4] = oscovida.covid19dh.Cache()
        defaults = tuple(defaults)
        with mock.patch.object(oscovida.covid19dh.get, '__defaults__', defaults):
            yield


@pytest.fixture(scope="session")
def mock_cache_dir(tmp_path_factory, request):
    static_cache = request.config.getoption("--static-cache")

    if static_cache:
        test_dir = os.path.dirname(os.path.abspath(__file__))
        cache_dir = os.path.join(test_dir, "test_data", ".cache")
    else:
        cache_dir = tmp_path_factory.mktemp("cache_dir")

    with mock.patch('oscovida.covid19dh.CACHE_DIR', cache_dir):
        #  See comments for `mock_cache_new` fixture
        defaults = list(oscovida.covid19dh.get.__defaults__)
        defaults[4] = oscovida.covid19dh.Cache()
        defaults = tuple(defaults)
        with mock.patch.object(oscovida.covid19dh.get, '__defaults__', defaults):
            yield
