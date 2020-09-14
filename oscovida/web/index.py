import datetime
from typing import Optional

from .. import covid19dh, statistics


def create_index(
    level: int,
    start: Optional[datetime.datetime] = None,
    end: Optional[datetime.datetime] = None,
    groupby: Optional[str] = None,
):
    #  This excludes the current administrative area as that one becomes the index
    #  later on
    available_aa = [f'administrative_area_level_{level}' for level in range(1, level)]

    columns = ['confirmed', 'deaths', 'population'] + available_aa
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
            'confirmed': 'confirmed-delta',
            'deaths': 'deaths-delta',
        }
    )

    data_index = data_end.join(data_delta)

    if groupby:
        data_index_groups = data_index.groupby(groupby)
        return {
            group: data_index_groups.get_group(group)
            for group in data_index_groups.groups
        }

    return data_index
