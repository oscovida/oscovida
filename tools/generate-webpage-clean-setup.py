import oscovida as osc

# force download of new data
osc.clear_cache()

# clear all metadata entries (cache used to compose markdown after html notebooks have been created)
osc.MetadataRegion.clear_all()

