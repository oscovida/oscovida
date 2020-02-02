[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fangohr/coronavirus-2020/master?filepath=model.ipynb)

# coronavirus-2020
Predict increase in infections and deaths based on extrapolation of fit

- [Static view of notebook, rendered by github](model.ipynb)
- [Static view of notebook, rendered by nbviewer](https://nbviewer.jupyter.org/github/fangohr/coronavirus-2020/blob/master/model.ipynb)
- [Interactive session (allows execution and modification of notebook with Binder)](https://mybinder.org/v2/gh/fangohr/coronavirus-2020/master?filepath=model.ipynb)


## What is this?

- an exploration of the data on infection and deaths related to the Coronavirus outbreak early 2020
- maybe this opens up the data and situation to more people (citizen science?)
- disclaimer: this is not done by epidemiology experts, [don't trust anything here](https://github.com/fangohr/coronavirus-2020/blob/master/LICENSE)
- contributions welcome
- The "predictions" below are based on a very simple model of growth, where we
  assume the same growth rate over the duration of the outbreak. We want to see
  these predictions to start to be wrong (and in particular to overestimate
  actual numbers; this would indicate the outbreak starts to be constrained).
- see also discussion in notebook
- raw data is available from this URL https://raw.githubusercontent.com/fangohr/coronavirus-2020/master/data.txt
- it may not be possible to update this daily/ 


## Predictions

In the tables below: "Prediction date" 31 January means that the prediction was
made with data available on the 31 Jan 2020. At that point, infections and
deaths were reported up to 30 January. The "1-day ahead prediction" is thus
predicting the numbers for 31 Jan (which typically become available the day
after, i.e. 1 Feb 2020 in this example).

As the basis for the data, we use the numbers from
https://www.worldometers.info/coronavirus/, which are shown when hovering with
the mouse over the data points in the two graphs. These are updated (according
to the graph) at at GMT+8h every day. (Other numbers on that webpage update more
frequently during the day.)

See [notebook](https://nbviewer.jupyter.org/github/fangohr/coronavirus-2020/blob/master/model.ipynb) for more details.

### Deaths

| Prediction date |  1-day ahead predicted |  actual |   10 days ahead predicted | actual          |
| --------------- | ---------------------: | ------: | ------------------------: | --------------: |
| 31 Jan 2020     |                    262 |     258 |                      1072 | ?               |
| 1 Feb 2020      |                    312 |     304 |                      1120 | ?               |
| 2 Feb 2020      |                    361 |       ? |                      1104 | ?               |  


### Infections

| Prediction date |  1-day ahead predicted |  actual |   10 days ahead predicted | actual      |
| --------------- | ---------------------: | ------: | ------------------------: | ----------: |
| 31 Jan 2020     |                  12358 |   11948 |                     48558 | ?           |
| 1 Feb 2020      |                  14687 |   14551 |                     50738 | ?           |
| 2 Feb 2020      |                  17436 |       ? |                     55286 | ?           |





