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


def read_and_parse_methodology_sources(config_dict):
    """
    Read and parse the Markdown sources detailed in the configuration
    dictionary, which explain the methodology followed on the away day.

    Args:
        config_dict: Dictionary configuring the Journalist.

    Returns:
        sources: List of dictionaries containing parsed information
        from the methodology sources.
    """
    sources = []
    for source in config_dict["methodology_sources"]:
        soup = read_and_soupify(source["filepath"])
        h2, bullets = get_h2_and_bullets(
            soup, source["keyword"], stop_early=source["stop_early"]
        )
        source["h2_title"] = h2.text
        source["bullets"] = [x.text for x in bullets]
        sources.append(source)
    return sources


def read_and_parse_transcript_sources(directory_path):
    """
    Read the transcript sources contained in the
    appropriate directory, and parse them.

    Args:
        directory_path: Path of the directory containing
        the transcript sources.
    
    Returns:
        transcript_sources: List of parsed transcript sources,
        where each source is a string (encoded in Markdown).
    """
    paths = Path(directory_path).iterdir()
    paths = [
        x for x in paths if "group" in x.name.lower()
    ]
    transcript_sources = []
    for path in paths:
        with open(path, "r") as f:
            source = path.name + "  " + f.read() + "  "
        transcript_sources.append(source)
    return transcript_sources