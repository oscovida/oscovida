import pytest

from oscovida import regions
from tests.conftest import mock_cache_dir


def test_top_level_parser(mock_cache_dir):
    region_parser = regions.Region._top_level_region_parser

    assert region_parser('Germany').alpha_3 == 'DEU'
    assert region_parser('DEU').name == 'Germany'

    assert region_parser('United Kingdom').alpha_3 == 'GBR'
    assert region_parser('GBR').name == 'United Kingdom'

    assert region_parser('great britain').alpha_3 == 'GBR'


def test_top_level_parser_raises():
    with pytest.raises(LookupError):
        regions.Region._top_level_region_parser('UK')


def test_check_admin_level_2(mock_cache_dir):
    assert regions.Region('DEU', level=2)._check_admin_level('Hamburg', level=2)
    assert regions.Region('USA', level=2)._check_admin_level('California', level=2)


def test_check_admin_level_3(mock_cache_dir):
    assert regions.Region('USA', 'California', level=3)._check_admin_level(
        'San Francisco', level=3
    )


def test_cite(mock_cache_dir):
    cite = regions.Region('DEU').cite

    assert all([isinstance(line, str) for line in cite])


def test_display_level_1():
    region = regions.Region('USA')

    assert (
        region.__repr__()
        == "Region(country='United States', admin_1='USA', admin_2=None, admin_3=None, level=1)"
    )

    assert region.__str__() == "United States (USA)"


def test_display_level_2():
    region = regions.Region('USA', 'California')

    assert (
        region.__repr__()
        == "Region(country='United States', admin_1='USA', admin_2='California', admin_3=None, level=2)"
    )

    assert region.__str__() == "United States (USA): California"


def test_display_level_3():
    region = regions.Region('USA', 'California', 'San Francisco')

    assert (
        region.__repr__()
        == "Region(country='United States', admin_1='USA', admin_2='California', admin_3='San Francisco', level=3)"
    )

    assert region.__str__() == "United States (USA): California, San Francisco"


@pytest.mark.parametrize(
    'test_input,expected_output',
    [
        (('USA',), ('United States', 'USA', None, None, 1)),
        (('USA', 'California'), ('United States', 'USA', 'California', None, 2)),
        (
            ('USA', 'California', 'San Francisco'),
            ('United States', 'USA', 'California', 'San Francisco', 3),
        ),
    ],
)
def test_data_levels(test_input, expected_output):
    country, admin_1, admin_2, admin_3, level = expected_output

    region = regions.Region(*test_input)

    assert region.level == level

    assert region.country == country

    assert region.admin_1 == admin_1
    assert region.admin_2 == admin_2
    assert region.admin_3 == admin_3

    if level == 2 and admin_2 != '*' and admin_2:
        assert region.data['administrative_area_level_2'].unique() == [admin_2]
    if level == 3 and admin_3 != '*' and admin_3:
        assert region.data['administrative_area_level_3'].unique() == [admin_3]


def test_raises_invalid_admin_name(mock_cache_dir):
    with pytest.raises(LookupError):
        regions.Region('UK')

    with pytest.raises(LookupError):
        regions.Region('GBR', 'Hamburg')


def test_raises_invalid_level(mock_cache_dir):
    with pytest.raises(ValueError):
        regions.Region('GBR', level=0)

    with pytest.raises(ValueError):
        regions.Region('GBR', level=4)

    with pytest.raises(ValueError):
        regions.Region('DEU', 'Hamburg', level=2)

    with pytest.raises(ValueError):
        regions.Region('DEU', 'Hamburg', 'SK Hamburg', level=3)
