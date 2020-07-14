import IPython.display

base_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"


def compute_binder_link(notebook_name):
    """Given a string """
    root_url = "https://mybinder.org/v2/gh/oscovida/binder/master?filepath=ipynb/"
    return root_url + notebook_name


def display_binder_link(notebook_name):
    url = compute_binder_link(notebook_name)
    # print(f"url is {url}")
    IPython.display.display(
        IPython.display.Markdown(f'[Execute this notebook with Binder]({url})'))
