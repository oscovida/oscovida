# %%
"""
# {TITLE}

* Homepage of project: https://oscovida.github.io
* [Execute this Jupyter Notebook using myBinder]({BINDER_URL})
"""

# %%
import datetime
import time

start = datetime.datetime.now()
print(f"Notebook executed on: {{start.strftime('%d/%m/%Y %H:%M:%S%Z')}} {{time.tzname[time.daylight]}}")

# %%
from oscovida.regions import Region
import oscovida.plots as plots

plots.set_backend('plotly')

# %%
region = Region({{REGION_ARGS}})
region

# %%
plots.plot_summary(region, label_prepend="")

# %%
region.data

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

- Open source and scientific computing community for the data tools
- Github for hosting repository and html files
- Project Jupyter for the Notebook and binder service
- The H2020 project Photon and Neutron Open Science Cloud ([PaNOSC](https://www.panosc.eu/))

"""

# %%
#  Data sources:
region.cite

# %%
print(f"Notebook execution took: {{datetime.datetime.now()-start}}")
