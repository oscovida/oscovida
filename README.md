[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fangohr/coronavirus-2020/master?filepath=model.ipynb)

# coronavirus-2020
Predict increase in infections and deaths based on extrapolation of fit

- [Static view of notebook, rendered by github](model.ipynb)
- [Static view of notebook, rendered by nbviewer](https://nbviewer.jupyter.org/github/fangohr/coronavirus-2020/blob/master/model.ipynb)
- [Interactive session (allows execution and modification of notebook with Binder)](https://mybinder.org/v2/gh/fangohr/coronavirus-2020/master?filepath=model.ipynb)

## Predictions

In the tables below: "Prediction date" 31 January means that the prediction was made with data available on the 31 Jan 2020. At that point, infections and deaths were reported up to 30 January. The "1-day ahead prediction" is thus predicting 
the numbers for 31 Jan (which typically become available the day after, i.e. 1 Feb 2020 in this example). 

As the bases for the data, we use the numbers from https://www.worldometers.info/coronavirus/, which are shown when hovering with the mouse over the data points in the two graphs. These are updated (according to the graph) at at GMT+8h every day. (Other numbers on that webpage update more frequently during the day.)

See [notebook](https://nbviewer.jupyter.org/github/fangohr/coronavirus-2020/blob/master/model.ipynb) for more details.

### Deaths

| Prediction date | 1-day ahead predicted | actual | 10 days ahead predicted | actual        |
| --------------- | ---------------------:| ------:|------------------------:|--------------:|
| 31 Jan 2020     | 262                   | 258    | 1072                    |  ?            |

### Infections

| Prediction date | 1-day ahead predicted | actual | 10 days ahead predicted | actual        |
| --------------- | ---------------------:| ------:|------------------------:|--------------:|
| 31 Jan 2020     | 12358                 | 11948  | 48558                   |   ?           |





