import os
from pathlib import Path
from parser import parse_kindle_books
from export_csv import export_to_csv
from enricher import enrich_books

PROJECT_ROOT = Path(__file__).parent.parent
KINDLE_CACHE = Path.home() / "AppData/Local/Amazon/Kindle/Cache/KindleSyncMetadataCache.xml"
OUTPUT_CSV = PROJECT_ROOT / "data" / "kindle_books.csv"

books = parse_kindle_books(KINDLE_CACHE)
enriched_books = enrich_books(books)
export_to_csv(enriched_books, OUTPUT_CSV)

print(f"{len(books)} books exported to {OUTPUT_CSV}")
print(f"{len(enriched_books)} books enriched.")