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

    # data cleaning: on 13 April, we had a Landkreis "LK Göttingen (alt)"
    # with only one data point. This causes plots to fail, because there
    # is nothing to plot, and then the legend() command failed.
    # We assume that the RKI labels unusual data with '(alt)', and remove those.

    alt_data_sets = [x for x in subregions if "(alt)" in x.lower()]
    if len(alt_data_sets) > 0:
        print(f"Removing datasets label with '(alt)': {alt_data_sets}")
        for alt in alt_data_sets:
            c, d = germany_get_region(landkreis=alt)
            print(f"  removed: {alt} : len(cases)={len(c)}, len(deaths)={len(d)}")
            # subregions = [x for x in subregions if not "(alt)" in x.lower()]

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



def main():
    test_world_overview(n=300)  # test all
    test_germany_overview(n=500) # test all


if __name__ == "__main__":
    main()
