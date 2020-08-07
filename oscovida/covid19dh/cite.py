from io import StringIO
import math
import re
import warnings

import pandas as pd
import requests


def cite(x: pd.DataFrame, raw: bool = False):
    # get sources
    url = 'https://storage.covid19datahub.io/src.csv'
    response = requests.get(url)  # headers={'User-Agent': 'Mozilla/5.0'}
    sources: pd.DataFrame = pd.read_csv(StringIO(response.text))

    # transform data
    isos = set(x["iso_alpha_3"].unique())
    params = set(x.columns)
    # add universal
    isos.add(math.nan)

    # collect used references
    sources = sources[
        sources["iso_alpha_3"].isin(isos) & sources["data_type"].isin(params)
    ]
    unique_sources = sources.fillna("").groupby(
        ["title", "author", "year", "institution", "url", "textVersion", "bibtype"]
    )

    if raw:
        return unique_sources.count().reset_index()

    # turn references into citations
    citations = []
    for n, g in unique_sources:
        (title, author, year, institution, url, textVersion, bibtype) = n

        if not author and not title:
            warnings.warn("reference does not specify author nor title, omitting")
            continue
        if not year:
            warnings.warn("reference does not specify year, omitting")
            continue

        if textVersion:
            citation = textVersion
        else:
            # pre,post
            if author:
                pre = author
                if title:
                    post = f"{title}"
            elif title:
                pre = title
                post = ""
            # post
            if institution:
                if post:
                    post += ", "
                post += f"{institution}"
            if url:
                if post:
                    post += ", "
                url = re.sub(r"(http://|https://|www\\.)([^/]+)(.*)", r"\1\2/", url)
                post += f"{url}"
            else:
                post += "."
            citation = f"{pre} ({year}), {post}"

        citations.append(citation)

    citations.append(
        "Guidotti, E., Ardia, D., (2020), \"COVID-19 Data Hub\", Working paper, doi: 10.13140/RG.2.2.11649.81763."
    )
    return citations


__all__ = ["cite"]
