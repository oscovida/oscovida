import pytest

from oscovida import regions


@pytest.mark.parametrize(
    'test_input,expected_output',
    [
        (('GB',), ('United Kingdom', 'GBR', None, None, 1)),
        (('GBR', 'England'), ('United Kingdom', 'GBR', 'England', None, 2)),
        (('GB', None, None, 3), ('United Kingdom', 'GBR', '*', '*', 3)),
        (
            ('United Kingdom', 'England', 'Westminster'),
            ('United Kingdom', 'GBR', 'England', 'Westminster', 3),
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


def test_region_ambiguity_error():
    with pytest.raises(LookupError):
        regions.Region('UK')


@pytest.mark.parametrize('level', [0, 4])
def test_level_error(level):
    with pytest.raises(ValueError):
        regions.Region('GBR', level=level)


def test_repr():
    region = regions.Region('United Kingdom', 'England', 'Westminster')

    assert (
        region.__repr__()
        == "Region(country='United Kingdom', admin_1='GBR', admin_2='England', admin_3='Westminster', level=3)"
    )


def test_str():
    region = regions.Region('United Kingdom', 'England', 'Westminster')

    assert region.__str__() == "United Kingdom (GBR): England, Westminster"
