
# Also delete data in place where notebooks are executed
rm -rf wwwroot/ipynb/cachedir

# copy requirements into base directory of repository for binder
cp ../binder/requirements.txt wwwroot
cp ../binder/apt.txt wwwroot
cp ../binder/requirements.txt binder
cp ../binder/apt.txt binder

# copy oscovida package so the notebooks can import it when executing on binder
rm -rf wwwroot/ipynb/oscovida
cp -av ../oscovida wwwroot/ipynb
rm -rf binder/ipynb/oscovida
cp -av ../oscovida binder/ipynb
