from bs4 import BeautifulSoup
from markdown import markdown
from pathlib import Path


def read_and_soupify(filepath):
    """
    Read markdown file from `filepath` and convert to a BeautifulSoup object in HTML format.

    Args:
        filepath: Path of the Markdown file to be read in.

    Returns:
        soup: a BeautifulSoup object in HTML format.
    """
    # Check file to be read in is Markdown.
    if Path(filepath).suffix != ".md":
        raise FileNotFoundError("The file is not Markdown.")

    # Convert to HTML and soupify.
    f = open(filepath, "r")
    html = markdown(f.read(), output_format="html5")
    soup = BeautifulSoup(html, "html.parser")

    return soup


def find_h2_by_keyword(soup, keyword):
    """
    Find within BeautifulSoup object the first header of level 2
    that contains a given keyword.

    Args:
        soup: BeautifulSoup object within which to perform a search.
        keyword: String representation of the keyword to be found.

    Returns:
        h2: bs4.element.Tag
    """
    for h2 in soup.find_all("h2"):
        if keyword.lower() in h2.text.lower():
            print(type(h2))
            return h2


def get_h2_and_bullets(soup, keyword, stop_early=None):
    """
    Extract the first h2 containing the keyword, and the
    first subsequent set of bullet points, with an option to
    skip some list items at the end.

    Args:
        soup: BeautifulSoup object within which to perform a search.
        keyword: String representation of the keyword to be found.

    Returns:
        h2: bs4.element.Tag that contains the keyword.
        bullets: List of items appearing just after h2.
        stop_early (Optional): How many bullets to skip at the end.
    """
    h2 = find_h2_by_keyword(soup, keyword)
    ul = h2.find_next_sibling("ul")
    bullets = ul.findChildren("li")
    if stop_early is not None:
        bullets = bullets[:-stop_early]
    return h2, bullets


def read_and_parse_sources(config_dict):
    sources = []
    for source in config_dict["sources"]:
        soup = read_and_soupify(source["filepath"])
        h2, bullets = get_h2_and_bullets(
            soup, source["keyword"], stop_early=source["stop_early"]
        )
        source["h2_title"] = h2.text
        source["bullets"] = [x.text for x in bullets]
        sources.append(source)
    return sources
