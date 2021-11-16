Home
####

:URL: index.html
:save_as: index.html

OSCOVIDA provides an `open science <open-science.html>`__ portal to see and
investigate the COVID19 infections and deaths as a function of time for the
`US states <us.html>`__, the `districts in Germany <germany.html>`__,
and most `other countries <countries.html>`__ in the world.

Use OSCOVIDA to monitor the pandemic, second waves, local outbreaks and motivate
social distancing and support for other containment measures.

European XFEL follows the RKI recommendations for access restrictions to the
campus after travel abroad or in Germany, we provide tables showing these
incidence rates for `Germany here <germany-incidence-rate.html>`__, and for
`countries worldwide here <countries-incidence-rate.html>`__.

Read more about our `motivation <motivation.html>`__, `data sources
<data-sources.html>`__, `team <team.html>`__, watch a
`video interview <https://youtu.be/1_oDc_vptBQ>`__, or join our
`Zulip chat instance here <https://oscovida.zulipchat.com>`__.

We provide a standard a set of analysis plots (`explained here <plots.html>`__) for different regions:

-  `List of all regions, countries and US states <all-regions.html>`__

-  `Overview for each country in the world <countries.html>`__ (Johns Hopkins data)

-  `States in the US <us.html>`__ (Johns Hopkins data)

-  `Counties (Landkreise) in Germany <germany.html>`__ (Robert Koch Institute data)

Occasionally, we try to provide `additional discussion COVID19 related news and numbers <tag-analysis.html>`__.

You can `fire up your own analysis environment in the cloud, select the relevant analysis notebook yourself, re-execute or extend the analysis <https://mybinder.org/v2/gh/oscovida/binder/master?filepath=ipynb>`__. See also our (growing) `set of tutorials <tag-tutorial.html>`__.

--------------

.. raw:: html
   :file: index-included-for-interactive-map

The map shows `7-day incidence rates per 100,000 people
<https://oscovida.github.io/countries-incidence-rate.html>`__ based on data
reported by the `Johns-Hopkins University
<https://oscovida.github.io/data-sources.html>`__. The colour scale for the
this world map goes up to the 90th quantile (where 90% of the countries have
less than that number of cases): any country with a 7 day incidence rate over
the 90th quantile is set to the darkest red colour.

--------------

.. raw:: html
   :file: index-included-for-figure1-html

This plot shows a randomly picked country as an example of what data is
available in the `detailed reports <all-regions.html>`__.

--------------

If you want to `contribute <contribute.html>`__, please either join our `Zulip
chat instance here <https://oscovida.zulipchat.com>`__ or `get in
touch <mailto:oscovidaproject@gmail.com>`__. Ideas, suggestions and
error reports, are welcome at our
`issue tracker <https://github.com/oscovida/oscovida/issues>`__.

History and authors
===================

This project was started by `Hans Fangohr <https://fangohr.github.io>`__ early in 2020, and later developed further with the
`Photon and Neutron Open Science Cloud (PaNOSC) <https://www.panosc.eu/>`__ and
`other volunteers <https://oscovida.github.io/team.html>`__ as an open science demonstrator.
Currently, the project is maintained by Hans Fangohr from the
`Max Planck Institute for Structure and Dynamics of Matter <https://www.mpsd.mpg.de/research/ssus/comput-science>`__,
`Yuri Kirienko <https://github.com/kirienko>`__, and
`Robert Rosca <https://github.com/RobertRosca>`__ 
from `European XFEL <http://xfel.eu>`__. European XFEL kindly provides the hardware to compute the daily
updates of all plots.


Disclaimer
==========

The plots and code here has been put together by volunteers who have no
training in epidemiology. There are likely to be errors in the
processing. You are welcome to use the material at your own risk. See
`license <license.html>`__ for details.

Acknowledgements
================

-  `Max Planck Institute for the Structure and Dynamics of Matter <https://www.mpsd.mpg.de/en>`__
-  `European XFEL <http://www.xfel.eu>`__
-  The H2020 project `Photon and Neutron Open Science Cloud (PaNOSC) <https://www.panosc.eu/>`__
-  `University of Southampton <https://www.soton.ac.uk>`__
-  `Biological Research Centre <http://www.brc.hu/>`__, Szeged
-  `Dept. of Software Engineering, University of Szeged <https://u-szeged.hu/>`__, Hungary
-  Johns Hopkins University provides data for countries
-  Robert Koch Institute provides data for within Germany
-  Open source and scientific computing community for the data tools, in particular numpy, scipy, pandas, matplotlib
-  Github for hosting repository and html files
-  Project Jupyter for the Notebook and Binder service

--------------

.. raw:: html

   <img src="{attach}europe-flag.svg" alt="European flag" width="40"> This project has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No. 823852.

.. raw:: html

   <!--![Plot]({attach}belgium7.png)

   -------------------------

   ![Plot]({attach}germany-doubling-time.png)

   -->
