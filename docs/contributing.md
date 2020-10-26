# Contributing

If you'd like to make a contribution to the project you may or may not have to
read through this document. For small contributions/bugfixes, reading through
these guidelines is probably not needed as we can suggest any required changes
during the review process, but if you plan on contributing a large amount then
please read through this in detail.

## Local Development Setup

We strongly recommend using a virtual environment for python project
development, the rough workflow to set up a local environment would be:

```sh
git clone git@github.com:oscovida/oscovida.git
cd oscovida
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

This will create a new virtual environment `.venv`, which is then activated and
used to install all of the development dependencies for oscovida.

Oscovida has relatively strict dependency management and code style guidelines,
you can execute these manually by running `black` and `isort` on any relevant
files, and if you have added or removed dependencies you should run
`dephell convert` to update the `setup.py` file.

To avoid running this manually, you can enable some hooks with `pre-commit` by
running:

```sh
pre-commit install
```

This will install some pre-commit hooks, so that `black`, `isort`, `dephell`,
and some other formatters/checks run before every commit is made. If a change
needs to be made then git will stop during the commit, and you must add the
changes in before the commit will be allowed.

If you do not want to install the hooks then you can run the scripts manually:

```sh
pre-commit run --all-files
```

## Dependency Management

As mentioned above, oscovida uses [Poetry](https://python-poetry.org/) and
[Dephell](https://github.com/dephell/dephell) for its dependency management. If
you need to add, update, or remove a dependency then make sure to do it via
poetry, as the `setup.py` file is automatically generated and should not be
modified by hand.

Once you have made your changes via poetry you can either run `pre-commit run
--all-files` to update and format `setup.py`, or manually run the commands:

```sh
dephell deps convert
black setup.py
```

And then commit your changes. Alternatively if you have enabled the pre-commit
hooks then simply add the `pyproject.toml` and `poetry.lock` files with git and
make a commit, at which point `setup.py` will be updated and formatted
automatically.

## Code Style

Oscovida follows the [Black](https://github.com/psf/black) code style, you can
manually run the formatter with `black $FILE_YOU_MODIFIED`, or you can set up
the pre-commit hooks so that it runs automatically for you each commit.

## Testing and Coverage

We use pytest for unit tests, and nbval for some additional testing for the
plots. Before sending off your PR we recommend running the test locally first,
this can be done by:

```sh
#  To run standard tests:
pytest --verbose
#  To run the notebook plot tests:
pytest --verbose --cov=oscovida --nbval ./tests/plots/
#  To run tests against the documentation notebooks:
pytest --verbose --cov=oscovida --nbval ./docs/
```

We aim for high coverage with our tests, so if you add in additional features
please add in tests for them as well.
