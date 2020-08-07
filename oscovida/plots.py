import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.ticker import FuncFormatter, ScalarFormatter


# choose font - can be deactivated
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Inconsolata']

# need many figures for index.ipynb and germany.ipynb
rcParams['figure.max_open_warning'] = 50

plt.style.use('ggplot')

