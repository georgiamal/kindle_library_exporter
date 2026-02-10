import requests
# TODO: implement clean cancellation of enrichment

VALID_GENRES = {
    "fantasy": ["fantasy", "epic fantasy", "romantic fantasy", "urban fantasy", "dark fantasy"],
    "science fiction": ["science fiction", "sci-fi", "scifi", "cyberpunk"],
    "mystery": ["mystery", "detective"],
    "thriller": ["thriller", "suspense", "murder", "psychological thriller"],
    "horror": ["horror", "gothic", "supernatural", "paranormal"],
    "romance": ["romance", "romantic", "love story"],
    "historical fiction": ["historical fiction", "historical"],
    "literary fiction": ["literary fiction", "literary", "contemporary"],
    "young adult": ["young adult", "ya", "teen"],
    "biography": ["autobiography", "memoir"],
    "self-help": ["self-help", "self help", "personal development"],
    "non-fiction": ["non-fiction", "non fiction"],
}

def extract_genres(subjects, max_genres=2):
    """
    Iterates through VALID GENRES dictionary and subjects found in openlibrary
    and finds valid genres; separated by a comma for up to [max_genres].

    Args:
        subjects: a list of subjects/ genres
        max_genres(int): maximum number of genres to return

    Returns:
        A string of all the valid found genres separated by a comma.
    """
    if not subjects:
        return ""

    found_genres = []

    for subject in subjects:

        for valid_genre, synonyms in VALID_GENRES.items():
            for synonym in synonyms:
                if synonym in subject.lower():
                    genre = valid_genre.title()

                    if genre not in found_genres:
                        found_genres.append(genre)

                        if len(found_genres) >= max_genres:
                            return ", ".join(found_genres)
                    break
    return ", ".join(found_genres) if found_genres else ""


def fetch_metadata(title, author):
    """
    Using the response from a query to openlibrary, extracts valid genre
    from metadata and page count if available.

    Args:
        title(str): title of the book
        author(str): author of the book

    Returns:
        A dictionary of the books page count and genre if found, else an empty dictionary.
    """
    query = f"title:{title} author:{author} language:eng".replace(" ", "+")
    url = f"https://openlibrary.org/search.json?q={query}&fields=key,title,subject,number_of_pages_median"
    headers = {
        "User-Agent": "KindleLibraryExporter/1.0 (https://github.com/georgiamal/kindle_library_exporter)"
    }
    try:
        response = requests.get(url, timeout=5, headers=headers)
        data = response.json()

        if data.get("numFound", 0) == 0:
            return {"Genre": "", "Page count": ""}

        doc = data["docs"][0]

        subjects = doc.get("subject", [])
        genre = extract_genres(subjects, max_genres=2)
        page_count = doc.get("number_of_pages_median", "")
        return {
            "Genre": genre,
            "Page count": page_count,
        }

    except Exception as e:
        print(f"  ERROR: {e}")
        return {"Genre": "", "Page count": ""}