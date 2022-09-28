# %%
"""
# {TITLE}

* Homepage of project: https://oscovida.github.io
* Plots are explained at http://oscovida.github.io/plots.html
* [Execute this Jupyter Notebook using myBinder]({BINDER_URL})
"""

# %%
import datetime
import time

start = datetime.datetime.now()
print(f"Notebook executed on: {{start.strftime('%d/%m/%Y %H:%M:%S%Z')}} {{time.tzname[time.daylight]}}")

# %%
%config InlineBackend.figure_formats = ['svg']
from oscovida import *

# %%
{OVERVIEW_FUNCTION}({OVERVIEW_ARGS}, weeks=5);

# %%
{OVERVIEW_FUNCTION}({OVERVIEW_ARGS});

# %%
{COMPARE_PLOT_FUNCTION}({COMPARE_PLOT_ARGS});


# %%
# load the data
cases, deaths = {DATA_LOAD_FUNCTION}({DATA_LOAD_ARGS})

# get population of the region for future normalisation:
inhabitants = population({OVERVIEW_ARGS})
print(f'Population of {OVERVIEW_ARGS}: {{inhabitants}} people')

# compose into one table
table = compose_dataframe_summary(cases, deaths)

# show tables with up to 1000 rows
pd.set_option("display.max_rows", 1000)

# display the table
table

# %%
"""
# Explore the data in your web browser

- If you want to execute this notebook, [click here to use myBinder]({BINDER_URL})
- and wait (~1 to 2 minutes)
- Then press SHIFT+RETURN to advance code cell to code cell
- See http://jupyter.org for more details on how to use Jupyter Notebook
"""

# %%
"""
# Acknowledgements:

- Johns Hopkins University provides data for countries
- Robert Koch Institute provides data for within Germany
- Atlo Team for gathering and providing data from Hungary (https://atlo.team/koronamonitor/)
- Open source and scientific computing community for the data tools
- Github for hosting repository and html files
- Project Jupyter for the Notebook and binder service
- The H2020 project Photon and Neutron Open Science Cloud ([PaNOSC](https://www.panosc.eu/))

--------------------
"""

# %%
print(f"Download of data from Johns Hopkins university: cases at {{fetch_cases_last_execution()}} and "
      f"deaths at {{fetch_deaths_last_execution()}}.")

# %%
# to force a fresh download of data, run "clear_cache()"

# %%
print(f"Notebook execution took: {{datetime.datetime.now()-start}}")
