#!/usr/bin/env bash

# This script is meant to be usable as a cron job. 

# first delete cached data etc
make clean


# then re-compute. Sometimes, some process times out, and we need to restart. It
# is safe to call the 'make all' command as often as desired: it will skip the
# work being done already, and only commit and push the webpages once the
# updating has completed. (Or at least until each step in the chain of makefile
# targets completes without an error code.)
for i in `seq 1 10`; do
    echo "`date` attempt $i running make all"
    make all;
done
