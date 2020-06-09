import datetime
import json
import math
import os
import time
import pytest
import numpy as np
import pandas as pd


from oscovida import MetadataRegion


def test_MetadataRegion_basics():
    m = MetadataRegion("Germany", "w")
    # assert os.path.exists(MetadataStorageLocation)

    m['html'] = "html-pfad"
    m['ipynb'] = "ipynb-pfad"

    m = MetadataRegion("UK", "w")
    m['html'] = "html-path"

    m = MetadataRegion("Germany")
    assert m['html'] == "html-pfad"
    assert m['ipynb'] == "ipynb-pfad"
    assert sorted(m.keys()) == sorted(["html", "ipynb"])

    assert m.as_dict() == {'html': 'html-pfad', 'ipynb': 'ipynb-pfad'}

    m = MetadataRegion("UK")
    assert m['html'] == "html-path"
    with pytest.raises(KeyError):
        m['missing-key'] 


def test_MetadataRegion_updated():
    m = MetadataRegion("Test", "w")
    assert m.last_updated_hours_ago() == math.inf

    m.mark_as_updated()
    # should be faster than a second
    assert m.last_updated_hours_ago()*3600 < 1
    assert m.last_updated_hours_ago() > 0

    time.sleep(1)
    assert m.last_updated_hours_ago()*3600 > 0.5

    m2 = MetadataRegion("Test")
    assert m.last_updated_hours_ago()*3600 > 0.5
    assert m.last_updated_hours_ago()*3600 < 2.0

    # calling last_updated adds this key
    assert list(m.keys()) == ["__last_modified__"]


def test_MetadataRegion_get_regions():
    MetadataRegion.clear_all()

    m = MetadataRegion("Germany", "w")
    # assert os.path.exists(MetadataStorageLocation)

    m['html'] = "html-pfad"
    m['ipynb'] = "ipynb-pfad"

    m = MetadataRegion("UK", "w")
    m['html'] = "html-path"

    assert sorted(MetadataRegion.get_all()) == ["Germany", "UK"]

    MetadataRegion.clear_all()

    assert sorted(MetadataRegion.get_all()) == []



def test_MetadataRegion_get_all_as_dataframe():
    MetadataRegion.clear_all()
    m = MetadataRegion("Germany", "w")
    # assert os.path.exists(MetadataStorageLocation)

    m['html'] = "html-pfad"
    m['ipynb'] = "ipynb-pfad"

    m = MetadataRegion("UK", "w")
    m['html'] = "html-path"
    m['ipynb'] = "ipynb-path"

    ref = pd.DataFrame({'html' : {'UK' : 'html-path', "Germany" : 'html-pfad'},
                        'ipynb' : {'UK' : 'ipynb-path', "Germany" : 'ipynb-pfad'}})
    actual = MetadataRegion.get_all_as_dataframe()

    # We want to run this line:
    # assert ref.equals(actual)
    # but need to sort the table to be sure rows are in the
    # same order:
    assert ref.sort_index().equals(actual.sort_index())
