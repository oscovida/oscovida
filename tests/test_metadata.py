import datetime
import json
import math
import os
import time
import pytest


from coronavirus import MetadataRegion


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

