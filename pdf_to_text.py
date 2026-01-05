import pdfplumber
import os
from pathlib import Path

def convert_pdf_to_text(pdf_path, output_path):
    """Convert a single PDF file to text."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)

        print(f"Successfully converted: {pdf_path.name} -> {output_path.name}")
        return True
    except Exception as e:
        print(f"Error converting {pdf_path.name}: {str(e)}")
        return False

def main():
    # Define input and output directories
    input_dir = Path("inputs")
    output_dir = Path("outputs")

    # Create directories if they don't exist
    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)

    # Get all PDF files in the inputs folder
    pdf_files = list(input_dir.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in the 'inputs' folder.")
        return

    print(f"Found {len(pdf_files)} PDF file(s) to convert.\n")

    # Convert each PDF file
    successful = 0
    for pdf_file in pdf_files:
        # Create output filename (replace .pdf with .txt)
        output_file = output_dir / f"{pdf_file.stem}.txt"

        if convert_pdf_to_text(pdf_file, output_file):
            successful += 1

    print(f"\nConversion complete: {successful}/{len(pdf_files)} files converted successfully.")

if __name__ == "__main__":
    main()
