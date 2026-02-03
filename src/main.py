from pathlib import Path
from parser import parse_kindle_books
from export_csv import export_to_csv

KINDLE_CACHE = Path.home() / "AppData/Local/Amazon/Kindle/Cache/KindleSyncMetadataCache.xml"

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_CSV = PROJECT_ROOT / "data" / "kindle_books.csv"

books = parse_kindle_books(KINDLE_CACHE)
export_to_csv(books, OUTPUT_CSV)

print(f"{len(books)} books exported to {OUTPUT_CSV}")