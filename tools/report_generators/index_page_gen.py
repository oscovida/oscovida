import datetime
import os
import subprocess

from coronavirus import MetadataRegion


def create_markdown_index_list(category):
    """Assemble a markdown table like this:

    | Country/Region                       | Total cases   | Total deaths   |
    |:-------------------------------------|:--------------|:---------------|
    | [Afghanistan](html/Afghanistan.html) | 1,351         | 43             |
    | [Albania](html/Albania.html)         | 678           | 27             |
    | [Algeria](html/Algeria.html)         | 3,127         | 415            |
    | [Andorra](html/Andorra.html)         | 731           | 40             |

    and return as string.
    """

    known_categories = ["world", "Germany", "US"]

    # gather data
    regions_all = MetadataRegion.get_all_as_dataframe()
    if category in known_categories:
        # select those we are interested in
        regions = regions_all[regions_all['category'] == category]
    elif category in ["all-regions"]:
        regions = regions_all
    else:

        raise NotImplementedError(
            f"category {category} is unknown."+
            f" Known values are {known_categories + ['all-regions']}")

    # change index to contain URLs and one-line summary in markdown syntax
    def compose_md_url(x):
        one_line_summary, html = x
        if isinstance(html, str):
            return "[" + one_line_summary + "](" + os.path.join('html', html) +")"
        elif repr(html) == 'nan':   # if html was not produced, then variable html is np.nan
            print(f"Missing html for {one_line_summary} - will not add link to html: \n{x}")
            return one_line_summary
        else:
            raise NotImplementedError("Don't know how to proceed: ", one_line_summary, html, x)

    new_index = regions[['one-line-summary', 'html-file']].apply(compose_md_url, axis=1)
    regions2 = regions.set_index(new_index)
    regions2.index.name = "Location"

    # select columns
    regions3 = regions2[['max-cases', 'max-deaths', 'cases-last-week']]
    regions4 = regions3.applymap(lambda v: '{:,}'.format(v))  # Thousands comma separator

    # rename columns
    rename_dict = {
        'max-cases' : 'Total cases',
        'max-deaths' : 'Total deaths',
        'cases-last-week' : 'New cases last week'
    }
    regions5 = regions4.rename(columns=rename_dict)

    return regions5.to_markdown()

def create_markdown_index_page(
    md_content, title, pelican_file_path,
    save_as, wwwroot, slug=None
):
    """Create pelican markdown file, like this:

    title: Germany
    tags: Data, Plots, Germany
    save-as: germany
    date: 2020-04-11 08:00
    """

    if slug is None:
        slug = save_as

    with open(os.path.join(pelican_file_path), "tw") as f:
        f.write(f"title: {title}\n")
        # f.write(f"category: Data\n")  - have stopped using categories (22 April 2020)
        f.write(f"tags: Data, Plots, {title}\n")
        f.write(f"save-as: {save_as}\n")
        f.write(f"slug: {slug}\n")
        date_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
        f.write(f"date: {date_time}\n")
        f.write("\n")
        f.write("\n")
        f.write(md_content)
        f.write("\n")

def create_index_page(sections, rootname, wwwroot):
    """Sections is dictionary: key is title, value is markdown text"""
    md_file = rootname + ".md"

    with open(os.path.join(wwwroot, md_file), "tw") as f:
        for section in sections:
            f.write(f"# {section}\n\n")
            f.write(sections[section])
    print(f"Written overview to {md_file}.")
    html_file = rootname + ".html"
    subprocess.check_call(
        f"pandoc -t html -o {os.path.join(wwwroot, html_file)} " +
        f"{os.path.join(wwwroot, md_file)}", shell=True
    )
    return html_file
