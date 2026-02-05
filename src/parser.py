import xml.etree.ElementTree as ET
# TODO: remove asin
def parse_kindle_books(path):
    """
    Parses Kindle for PC app's metadata XML file
    and extracts user's purchased or borrowed (Kindle Unlimited)
    ebook information excluding any default books like dictionaries.

    Args:
        path: path to the KindleSyncMetadataCache.xml file.

    Returns:
        list[dict]: a list of dictionaries, each representing a Kindle ebook
        with the following keys:
            - title (str): Book title excluding anything in "()" or after ":"
            - author (str): Author name(s) in [First] [Last] format
            - asin (str): Amazon Standard Identification Number
            - origin (str): Ebook's origin (e.g. "Purchase", "KindleUnlimited").
    """

    tree = ET.parse(path)
    root = tree.getroot()
    books = []

    for meta in root.findall(".//meta_data"):
        if meta.findtext("cde_contenttype") != "EBOK":
            continue

        origin_type = meta.findtext("origins/origin/type")
        # Skip default books, dictionaries etc
        if origin_type != "Purchase" and origin_type != "KindleUnlimited":
            continue

        # Exclude anything from ":" and after from title
        title_raw = meta.findtext("title")
        if ":" in title_raw:
            title = title_raw[:title_raw.index(":")]
        else:
            title = title_raw
        # Exclude anything from "(" and after from title
        if "(" in title:
            title = title[:title.index("(")]

        # Format authors in [First] [Last] name before appending
        authors_raw = [a.text.strip() for a in meta.findall("authors/author") if a.text]

        authors = []
        for a in authors_raw:
            if "," in a:
                last, first = [x.strip() for x in a.split(",", 1)]
                authors.append(f"{first} {last}")
            else:
                authors.append(a)  # already in correct order

        # Join multiple authors with comma
        author_str = ", ".join(authors)

        books.append({
            "title": title,
            "author": author_str,
            "asin": meta.findtext("ASIN"),
            "origin": meta.findtext("origins/origin/type"),
        })
    return books

