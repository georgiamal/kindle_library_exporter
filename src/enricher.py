import requests
import time
# TODO: implement clean cancellation of enrichment
# TODO: what else for mystery one?
# TODO: maybe add api header for identification - user input in TUI??
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
    query = f"title:{title} author:{author} language:eng".replace(" ", "+")
    url = f"https://openlibrary.org/search.json?q={query}&fields=key,title,subject,number_of_pages_median"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("numFound", 0) == 0:
            return {"page_count": "", "genre": ""}

        doc = data["docs"][0]

        subjects = doc.get("subject", [])
        genre = extract_genres(subjects, max_genres=2)
        page_count = doc.get("number_of_pages_median", "")
        return {
            "page_count": page_count,
            "genre": genre,
        }

    except Exception as e:
        print(f"  ERROR: {e}")
        return {"page_count": "", "genre": ""}


def enrich_books(books):
    enriched_books = []
    total = len(books)

    for i, book in enumerate(books, 1):
        print(f"Processing book {i}/{total}")

        metadata = fetch_metadata(book["title"], book["author"])
        enriched_book = {**book, **metadata}
        enriched_books.append(enriched_book)

        time.sleep(0.5)

    return enriched_books
