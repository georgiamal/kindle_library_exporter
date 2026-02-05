import xml.etree.ElementTree as ET

def parse_kindle_books(path):
    """

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
            "title": meta.findtext("title"),
            "author": author_str,
            "asin": meta.findtext("ASIN"),
            "origin": meta.findtext("origins/origin/type"),
        })
    return books

