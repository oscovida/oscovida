import pytest

from oscovida import regions


def test_region_check_admin_level(mock_cache_dir):
    pass


def test_region_top_level_parser(mock_cache_dir):
    pass


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
def test_region_data_levels(test_input, expected_output):
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


def test_region_raises():
    #  Invalid admin 1
    with pytest.raises(LookupError):
        regions.Region('UK')

    #  Invalid admin 2
    with pytest.raises(LookupError):
        regions.Region('GBR', 'Hamburg')

    # Invalid level
    with pytest.raises(ValueError):
        regions.Region('GBR', level=0)
    with pytest.raises(ValueError):
        regions.Region('GBR', level=4)


def test_display():
    region = regions.Region('USA', 'California', 'San Francisco')

    assert (
        region.__repr__()
        == "Region(country='United States', admin_1='USA', admin_2='California', admin_3='San Francisco', level=3)"
    )

    assert region.__str__() == "United States (USA): California, San Francisco"
