import time
from pathlib import Path
from rich.console import Console
from rich import box
from rich.panel import Panel
from rich.progress import track
from rich.table import Table

from parser import parse_kindle_books
from export_csv import export_to_csv
from enricher import fetch_metadata

console = Console()
table = Table(box=box.ASCII_DOUBLE_HEAD)

PROJECT_ROOT = Path(__file__).parent.parent
KINDLE_CACHE = Path.home() / "AppData/Local/Amazon/Kindle/Cache/KindleSyncMetadataCache.xml"
OUTPUT_CSV = PROJECT_ROOT / "data" / "kindle_books.csv"

def main():
    try:
        # Title
        console.print(Panel.fit("[bold medium_purple3]📚 Kindle Library Exporter[/bold medium_purple3]\n"
            "Export your Kindle books to CSV with enriched metadata.",
            border_style="medium_purple3"))

        # Parse step
        console.print("[pink3]Parsing[/pink3] kindle cache..")
        with console.status("[spinner] Processing XML.."):
            books = parse_kindle_books(KINDLE_CACHE)
        console.print(f"> Found {len(books)} kindle books.\n")

        # Enrich step
        console.print("[pink3]Enriching[/pink3] books with metadata from OpenLibrary..")
        enriched_books = []
        total = len(books)

        for book in track(books, description="Processing..", total=len(books)):
            metadata = fetch_metadata(book["Title"], book["Author"])
            enriched_books.append({**book, **metadata})
            time.sleep(0.5)
        console.print("[bold orchid]✓[/bold orchid] Kindle books have been enriched.\n")

        # Export step
        console.print("[pink3]Exporting[/pink3] to CSV..")
        export_to_csv(enriched_books, OUTPUT_CSV)
        console.print(f"[bold orchid]✓[/bold orchid] Exported to [italic pink3]{OUTPUT_CSV}[/italic pink3]\n")

        # Summary
        summary = Table(title="Export Summary", show_header=False, border_style="pink3")
        summary.add_row("Total Books", str(len(enriched_books)))
        summary.add_row("Output File", str(OUTPUT_CSV))
        console.print(summary)

    except KeyboardInterrupt:
        console.print("\nKindle Library Exporter [italic red]interrupted[/italic red].\n")
        return
    except FileNotFoundError as e:
        console.print(f"\nKindle cache file not found: {e}")
        console.print("[dim] Ensure that the Kindle for PC app is installed and your books are synced.[/dim]\n")
        return
    except Exception as e:
        console.print(f"\n[dim] Error: {e}")
        return

if __name__ == "__main__":
    main()