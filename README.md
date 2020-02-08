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
- and some processed data is available at https://raw.githubusercontent.com/fangohr/coronavirus-2020/master/figures/table-1.md
- it may not be possible to update this daily

## News 7 February

It looks like the spread starts to slow down now - this is promising. 

This is best seen in the bar chart showing "New infections per day".

The predictions should here should now fail and overestimate actual numbers
(because the fitted model assumes constant growth during the whole outbreak, 
and actual data points of infection seem to start to deviate from this.
Would be interesting to check this quantitatively).


## Infections

![Infection data](figures/infections-with-model-fit.svg)

![Infections daily change](figures/new-infections.svg)

## Deaths

![Infection data](figures/deaths-with-model-fit.svg)

![Deaths daily change](figures/new-deaths.svg)


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
| 2 Feb 2020      |                    361 |     362 |                      1104 | ?               |
| 3 Feb 2020      |                    423 |     426 |                      1230 | ?               |
| 4 Feb 2020      |                    493 |     492 |                      1393 | ?               |
| 5 Feb 2020      |                    566 |     565 |                      1518 | ?               |
| 6 Feb 2020      |                    645 |     638 |                      1650 | ?               |
| 7 Feb 2020      |                    724 |     724 |                      1746 | ?               |
| 8 Feb 2020      |                    813 |       ? |                      1891 | ?               |


### Infections

| Prediction date |  1-day ahead predicted |  actual |   10 days ahead predicted | actual      |
| --------------- | ---------------------: | ------: | ------------------------: | ----------: |
| 31 Jan 2020     |                  12358 |   11948 |                     48558 | ?           |
| 1 Feb 2020      |                  14687 |   14551 |                     50738 | ?           |
| 2 Feb 2020      |                  17436 |   17387 |                     55286 | ?           |
| 3 Feb 2020      |                  20498 |   20626 |                     60621 | ?           |
| 4 Feb 2020      |                  23956 |   24553 |                     67084 | ?           |
| 5 Feb 2020      |                  28137 |   28276 |                     77138 | ?           |
| 6 Feb 2020      |                  32417 |   31439 |                     85451 | ?           |
| 7 Feb 2020      |                  36170 |   34875 |                     88039 | ?           |
| 8 Feb 2020      |                  39987 |       ? |                     91704 | ?           |

