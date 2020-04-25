import datetime
import json
import math
import os



MetadataStorageLocation = os.path.join("coronavirus-metadata", "regions")


class MetadataRegion:
    """Object to represent metadata for one region persistently. Behaves mostly
    like a dictionary. Any change is written to disk immediately.

    """

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
        self._d['__last_modified__'] = repr(datetime.datetime.now())

    def _save(self):
        with open(self._storage_path(), 'w') as f_out:
            json.dump(self._d, f_out)

    def __getitem__(self, key):
        return self._d[key]

    def __setitem__(self, key, value):
        self._d[key] = value
        self._save()

