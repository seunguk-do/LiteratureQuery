"""
PDF to Text Conversion Module
Converts all PDF files in inputs folder to text files in tmp/txts
"""
import pdfplumber
import os
from pathlib import Path

def convert_pdf_to_text(pdf_path, output_path):
    """Convert a single PDF file to text."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)

        print(f"✓ Converted: {pdf_path.name} -> {output_path.name}")
        return True
    except Exception as e:
        print(f"✗ Error converting {pdf_path.name}: {str(e)}")
        return False

def convert_all_pdfs():
    """Convert all PDFs in inputs folder to text files in tmp/txts."""
    # Define input and output directories
    input_dir = Path("inputs")
    output_dir = Path("tmp/txts")

    # Create directories if they don't exist
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get all PDF files
    pdf_files = list(input_dir.glob("*.pdf"))

    if not pdf_files:
        print("⚠ No PDF files found in 'inputs' folder.")
        print(f"  Please add PDF files to: {input_dir.absolute()}")
        return 0

    print(f"\n{'='*70}")
    print(f"PDF to Text Conversion")
    print(f"{'='*70}")
    print(f"Found {len(pdf_files)} PDF file(s) to convert.\n")

    # Convert each PDF file
    successful = 0
    for pdf_file in pdf_files:
        # Create output filename (replace .pdf with .txt)
        output_file = output_dir / f"{pdf_file.stem}.txt"

        if convert_pdf_to_text(pdf_file, output_file):
            successful += 1

    print(f"\n{'='*70}")
    print(f"Conversion complete: {successful}/{len(pdf_files)} files converted successfully.")
    print(f"{'='*70}\n")

    return successful

if __name__ == "__main__":
    convert_all_pdfs()
