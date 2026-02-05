import csv
from pathlib import Path
from typing import List, Dict


def export_to_csv(books: List[Dict], output_path: Path):
    """
    Export parsed books to a csv file.

    Args:
        books: list[dict] of parsed books
        output_path: path to output csv file

    Returns:
        None
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not books:
        print("No books found")
        return

    fieldnames = books[0].keys()

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)

    print(f"Wrote {len(books)} books to {output_path}")