#!/usr/bin/env fish

conda activate oscovida-production

python -c "import oscovida as osc; print(osc.__file__)"

# capture exit code
if test $status -eq 0
    #echo "no error when importing"
else
    echo "SCHTOPP - wrong conda environment??"
    exit 1
end

echo "About to clean cache and metadata cache [in 5 sec]"
sleep 5
# This script is meant to be usable as a cron job. 

# first delete cached data etc
make clean


# then re-compute. Sometimes, some process times out, and we need to restart. It
# is safe to call the 'make all' command as often as desired: it will skip the
# work being done already, and only commit and push the webpages once the
# updating has completed. (Or at least until each step in the chain of makefile
# targets completes without an error code.)
for i in (seq 1 10);
    echo (date) " attempt $i running make all"
    make all;
    # if we have a fail, give the system some time
    # to sort itself out. 
    sleep 10
end
