"""
merge_pdfs.py - Merge all PDFs in a folder into a single output file.

Usage:
    python merge_pdfs.py                        # merges PDFs in current folder
    python merge_pdfs.py /path/to/folder        # merges PDFs in specified folder
    python merge_pdfs.py /path/to/folder -o my_output.pdf  # custom output name

Install dependency first:
    pip install pypdf
"""

import sys
import argparse
from pathlib import Path
from pypdf import PdfWriter, PdfReader


def merge_pdfs(folder: Path, output_path: Path) -> None:
    # Collect all PDFs in the folder, sorted alphabetically
    pdf_files = sorted(folder.glob("*.pdf"))

    # Exclude the output file itself if it's in the same folder
    pdf_files = [f for f in pdf_files if f.resolve() != output_path.resolve()]

    if not pdf_files:
        print(f"No PDF files found in: {folder}")
        return

    print(f"Found {len(pdf_files)} PDF(s) to merge:")
    for f in pdf_files:
        print(f"  - {f.name}")

    writer = PdfWriter()

    for pdf_file in pdf_files:
        try:
            reader = PdfReader(pdf_file)
            for page in reader.pages:
                writer.add_page(page)
            print(f"  ✓ Added {pdf_file.name} ({len(reader.pages)} page(s))")
        except Exception as e:
            print(f"  ✗ Skipped {pdf_file.name}: {e}")

    with open(output_path, "wb") as out:
        writer.write(out)

    print(f"\nDone! Merged file saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Merge all PDFs in a folder.")
    parser.add_argument(
        "folder",
        nargs="?",
        default=".",
        help="Folder containing PDFs to merge (default: current directory)",
    )
    parser.add_argument(
        "-o", "--output",
        default="merged.pdf",
        help="Output filename (default: merged.pdf)",
    )
    args = parser.parse_args()

    folder = Path(args.folder).resolve()

    if not folder.is_dir():
        print(f"Error: '{folder}' is not a valid directory.")
        sys.exit(1)

    output_path = folder / args.output

    merge_pdfs(folder, output_path)


if __name__ == "__main__":
    main()