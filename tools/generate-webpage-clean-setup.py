import coronavirus as cv

# force download of new data
cv.clear_cache()

# clear all metadata entries (cache used to compose markdown after html notebooks have been created)
cv.MetadataRegion.clear_all()

