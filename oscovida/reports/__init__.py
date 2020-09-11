import datetime
from typing import Optional

from .. import covid19dh, statistics


def create_index(
    level: int,
    start: Optional[datetime.datetime] = None,
    end: Optional[datetime.datetime] = None,
):
    columns = ['confirmed', 'deaths', 'population']
    columns_delta = ['confirmed', 'deaths']

    if end is None:
        end = datetime.datetime.now()

    if start is None:
        start = datetime.datetime.today() - datetime.timedelta(7)

    data = covid19dh.get(level=level)

    aa = f'administrative_area_level_{level}'

    data_start = data.loc[start.strftime("%Y%m%d")].set_index(aa)[columns]
    data_end = data.loc[end.strftime("%Y%m%d")].set_index(aa)[columns]

    data_delta = data_end[columns_delta] - data_start[columns_delta]
    data_delta = data_delta.rename(
        columns={
            'confirmed': f'confirmed-past-{(end-start).days + 1}-days',
            'deaths': f'deaths-past-{(end-start).days + 1}-days',
        }
        # {
        #     'confirmed': f'New cases last {(end-start).days + 1} days',
        #     'deaths': f'New deaths last {(end-start).days + 1} days',
        # }
    )

    return data_end.join(data_delta)
