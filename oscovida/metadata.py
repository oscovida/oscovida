import datetime
import json
import math
import os
import pandas as pd


MetadataStorageLocation = os.path.join("oscovida-metadata", "regions")


class MetadataRegion:
    """Object to represent metadata for one region persistently. Behaves mostly
    like a dictionary. Any change is written to disk immediately.

    Intended use:
    - each MetadataRegion object represents one country.
    - store for each the location of html and ipynb files
    - store current deaths and cases
    - store when last updated

    Use cases:

    - create markdown/html based on this metadata information, not
      on building a list of files while computing the html
    - this is good for testing things
    - and allows to create the html files in different functions/sessions, and to later
      composed the markdwon/html from the metadata
    - also useful for more aggressive parallelisation

    """
    @staticmethod
    def get_all():
        """ Return list of names that are stored on disk.
        """
        regions = []
        for fname in os.listdir(MetadataStorageLocation):
            # check this is a valid file:
            assert fname.endswith("-meta.json")

            region_name = fname.split("-meta.json")[0]
            # attempt reading for good measure
            m = MetadataRegion(region_name)
            regions.append(region_name)
        return regions

    @staticmethod
    def get_all_as_dataframe():
        """ Return a Dataframe with all data stored on disk.
        """
        regions = MetadataRegion.get_all()
        d = {}
        for region in regions:
            index = region
            m = MetadataRegion(region)
            d[region] = m.as_dict()
        df = pd.DataFrame(d).T
        return df

    @staticmethod
    def clear_all():
        """ Clear all entries from disk, and create storage directory if it doesn't exist yet.
        """
        if os.path.exists(MetadataStorageLocation):
            for fname in os.listdir(MetadataStorageLocation):
                # check this is a valid file:
                assert fname.endswith("-meta.json")
                os.remove(os.path.join(MetadataStorageLocation, fname))
        else:
            # presumably we run the code in a new place

            # create path
            os.makedirs(MetadataStorageLocation)
            # not creating the path here, can lead to a race condition when
            # multiple processed try to create it when running in parallel

    def __init__(self, country, mode="r"):
        """Expects country string and mode

        mode:
        - "r" to read back and update record (default)
        - "w" to delete any existing data
        """
        self.country = country

        # check path exists
        if not os.path.exists(MetadataStorageLocation):
            os.makedirs(MetadataStorageLocation)

        if mode == "r":
            # have we got an existing record?
            if os.path.exists(self._storage_path()):
                self._load()
            else:
                self._clear()

        elif mode == "w":
            self._clear()
        else:
            raise NotImplementedError(f"Unknown mode {mode}")

    def last_updated_hours_ago(self):
        """returns hours since last modification, i.e. number of hours since last time
        something was changed in the object.
        """
        last_modified = self._d.get('__last_modified__', None)
        if last_modified:
            time_delta = datetime.datetime.now() - eval(last_modified)
            hours_ago = time_delta.total_seconds() / 3600
        else:
            hours_ago = math.inf

        return hours_ago

    def _storage_path(self):
        return os.path.join(MetadataStorageLocation,
                            self.country + "-meta.json")

    def _clear(self):
        self._d = {}
        self._save()

    def _load(self):
        with open(self._storage_path()) as f_in:
            self._d = json.load(f_in)

    def mark_as_updated(self):
        self['__last_modified__'] = repr(datetime.datetime.now())

    def _save(self):
        with open(self._storage_path(), 'w') as f_out:
            json.dump(self._d, f_out, sort_keys=True, indent=4)

    def keys(self):
        return self._d.keys()

    def as_dict(self):
        return self._d

    def __getitem__(self, key):
        return self._d[key]

    def __setitem__(self, key, value):
        self._d[key] = value
        self._save()




# Stuff to track:

"""
object-identifier: country name

values:
- html-name (file)
- ipynb-name (file)  
- deaths (current values)
- cases (current values)




"""
