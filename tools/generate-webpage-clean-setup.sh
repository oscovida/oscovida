
# Also delete data in place where notebooks are executed
rm -rf wwwroot/ipynb/cachedir

# copy requirements into base directory of repository for binder
cp ../binder/requirements.txt wwwroot
cp ../binder/apt.txt wwwroot
cp ../binder/requirements.txt binder
cp ../binder/apt.txt binder

# copy coronavirus package so the notebooks can import it when executing on binder
rm -rf wwwroot/ipynb/coronavirus 
cp -av ../coronavirus wwwroot/ipynb
rm -rf binder/ipynb/coronavirus 
cp -av ../coronavirus binder/ipynb


