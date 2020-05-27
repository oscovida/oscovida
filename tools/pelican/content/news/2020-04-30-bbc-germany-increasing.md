title: BBC news reports "Germany's daily cases increasing"
tags: Data, Germany, Numbers-in-news, News, Analysis
date: 2020/04/30 10:00
slug: 2020-04-30-news-report-germanys-daily-cases-increasing


## The news article

Today, a report from [BBC live news
coverage](https://www.bbc.com/news/live/world-52481788/page/2) of COVID19 was
featuring the headline: "*Germany's daily cases keep rising*" and then explained that

> Germany has recorded 1,478 new cases for the past 24 hours, marking the fourth
> day that new infections have gone up.

And ends with:

> Germany last week began easing some of its lockdown measures. It's not clear
> whether officials attribute the rise in cases to that easing - but polls show
> the majority of Germans are against a rushed lifting of the lock down.

This seems to imply an unexpected increase in daily new cases. 

## Putting these numbers in context

The daily new cases computed from the data from the Johns Hopkins university for the last 4 days are:

```
|            |   total cases |   daily new cases |
|:-----------|--------------:|------------------:|
| 2020-04-26 |        157770 |              1257 |
| 2020-04-27 |        158758 |               988 |
| 2020-04-28 |        159912 |              1154 |
| 2020-04-29 |        161539 |              1627 |
```

The [data for cases for 30 April is not yet made available from Johns
Hopkins](https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv)
- the numbers are always updated at the beginning of the next day to be able to
include the data from the previous day.

For at least the last three days, the trend reported is correct: the daily new cases increase from 988 to 1154 to 1627.

```
|            |   daily new cases |
|:-----------|------------------:|
| 2020-04-27 |               988 |
| 2020-04-28 |              1154 |
| 2020-04-29 |              1627 |
```

We visualise this by plotting a bar for each day and the number of new infections:

![image]({attach}2020-04-30-bbc-germany-increasing1.svg)

We put these numbers into the context of the development of the daily new cases
over an extended period of time, and show the corresponding visualisation:

![image]({attach}2020-04-30-bbc-germany-increasing2.svg)

## Conclusion

We can see that the increase of daily new cases over 3 days is somewhat
meaningless: the reported new cases have been oscillating for all data points,
so that increasing numbers for a few days are not necessarily alarming (or
re-assuring). One could speculate that during the weekend and just after fewer
cases are reported, and thus there could be a modulation in the reported data
with a frequency of weeks.

The important data is that averaged over a longer period of time. The blue line
shows data averaged over a week and provides more useful guidance than the daily
numbers which are subjected to noise and - probably - to systematic periodic
oscillations due to the working week.

The main lesson is that individual numbers need to be to put the data in context
to be interpreted.

## Further reading

1. The [Jupyter Notebook to create the plots and table above is
available](https://github.com/oscovida/binder/blob/master/ipynb/2020-04-30-bbc-germany-increasing.ipynb) or [here](2020-04-30-bbc-germany-increasing-notebook.html)
and can be [re-executed in your
browser](https://mybinder.org/v2/gh/oscovida/binder/master?filepath=ipynb/2020-04-30-bbc-germany-increasing.ipynb) 

2. Updated plots and tables of the type shown above [are available for many countries and regions](https://oscovida.github.io)
 and for Germany at [https://oscovida.github.io/html/Germany.html](https://oscovida.github.io/html/Germany.html).


3. Original article
   ([https://www.bbc.com/news/live/world-52481788/page/2](https://www.bbc.com/news/live/world-52481788/page/2),
   7:19am)

4. More data from Germany (see also [at bottom of this page](https://oscovida.github.io/html/Germany.html)):
```
|            |   total cases |   daily new cases |   total deaths |   daily new deaths |
|:-----------|--------------:|------------------:|---------------:|-------------------:|
| 2020-04-29 |        161539 |              1627 |           6467 |                153 |
| 2020-04-28 |        159912 |              1154 |           6314 |                188 |
| 2020-04-27 |        158758 |               988 |           6126 |                150 |
| 2020-04-26 |        157770 |              1257 |           5976 |                 99 |
| 2020-04-25 |        156513 |              1514 |           5877 |                117 |
| 2020-04-24 |        154999 |              1870 |           5760 |                185 |
| 2020-04-23 |        153129 |              2481 |           5575 |                296 |
| 2020-04-22 |        150648 |              2357 |           5279 |                246 |
| 2020-04-21 |        148291 |              1226 |           5033 |                171 |
| 2020-04-20 |        147065 |              1881 |           4862 |                276 |
```
