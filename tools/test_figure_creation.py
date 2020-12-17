import time
import matplotlib
matplotlib.use("Agg")


from oscovida import overview, fetch_data_germany, fetch_deaths, fetch_cases


def get_germany_subregion_list():
    """returns list of subregions (Kreise),
    ordered according to (i) Land, then (ii) Kreis
    """
    x = fetch_data_germany()
    land_kreis = x[['Bundesland', 'Landkreis']]
    ordered = land_kreis.sort_values(['Bundesland', 'Landkreis'])
    return list(ordered['Landkreis'].drop_duplicates())


def get_country_list():
    d, c = fetch_deaths(), fetch_cases()

    countries = d.index
    countries2 = c.index
    assert (countries2 == countries).all()

    # Here we should identify regions in countries, and process those.
    # Instead, as a quick hack to get started, we'll just take one country
    # and the current "get_country" method will sum over all regions of one country if only
    # the country name is given.

    return sorted(countries.drop_duplicates())


def test_germany_overview(n=10):
    """Test n countries """

    subregions = get_germany_subregion_list()[0:n]

    start_time = time.time()
    for i, subregion in enumerate(subregions):
        print(f"Processing {i+1:3}/{len(subregions)} [{time.time()-start_time:4.0f}s] {subregion}")
        overview(country="Germany", subregion=subregion)
        matplotlib.pyplot.close('all')


def test_world_overview(n=10):
    countries = get_country_list()

    start_time = time.time()
    for i, country in enumerate(countries[0:n]):
        print(f"Processing {i+1:3}/{len(countries)} [{time.time()-start_time:4.0f}s] {country}")
        overview(country=country)
        matplotlib.pyplot.close('all')


if __name__ == "__main__":
    test_world_overview(n=300)      # test all
    test_germany_overview(n=500)    # test all
