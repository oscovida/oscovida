Currently this is a bit of a code-spaghetti. The
[oscovida/oscovida.github.io](github.com/oscovida/oscovida.github.io) repository
has a CI which automatically updates the web-page twice a day. This pulls in the
master branch of `oscovida/oscovida`, and then calls some of the functions it
provides to generate the pages.

Generating the reports is handled by the `oscovida/tools/report_generators`
module, however this **only** creates the ipynb/html summary reports, so the
individual notebooks (e.g. those in `oscovida/tools/pelican/content/ipynb`) are
not re-generated.

To get around this, we define `pre-generate.sh` and `post-generate.sh` files
here, the `pre-generate.sh` script is executed by the
`oscovida/oscovida.github.io` CI at the start after all the dependencies are
installed and **before** the automatic report generation runs, and the
`post-generate.sh` script is executed **after** the reports are generated but
before the `make html` stage is executed.

For example, if you create a new analysis notebook and put it into
`pelican/content/ipynb/cool-nb.ipynb` then you would add this line to the
`post-generate.sh` file:

```
jupyter nbconvert --ExecutePreprocessor.timeout=600 --inplace --to notebook --execute ../pelican/content/ipynb/cool-nb.ipynb
```

Which means that the notebook will be re-executed in place (overwriting the
original), and after that is done `make html` runs so that pelican uses the
updated python notebook to generate the pages.

These hooks are also called by the PR CI.
