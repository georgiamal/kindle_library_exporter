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
        if origin_type != "Purchase" and origin_type != "KindleUnlimited":
            continue

        books.append({
            "title": meta.findtext("title"),
            "author": meta.findtext("authors/author"),
            "asin": meta.findtext("ASIN"),
            "origin": meta.findtext("origins/origin/type"),
        })
    return books

