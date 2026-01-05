"""
Academic Paper Reference Extraction Tool
Main orchestration script for the complete workflow
"""

from dataclasses import dataclass
from pathlib import Path
import shutil
import tyro
from convert_pdfs import convert_all_pdfs
from extract_references import extract_from_all_papers


def print_banner():
    """Print welcome banner."""
    print("\n" + "=" * 70)
    print(" " * 15 + "📚 ACADEMIC REFERENCE EXTRACTION TOOL")
    print("=" * 70)


def clear_tmp_folders():
    """Clear all files in tmp/txts and tmp/extraction_templates."""
    folders_to_clear = [
        Path("tmp/txts"),
        Path("tmp/extraction_templates")
    ]

    for folder in folders_to_clear:
        if folder.exists():
            # Remove all files in the folder
            for item in folder.glob("*"):
                if item.is_file():
                    item.unlink()
                    print(f"  Removed: {item}")
            print(f"✓ Cleared: {folder}/")
        else:
            print(f"  Skipped (not found): {folder}/")


@dataclass
class Args:
    """Academic Paper Reference Extraction Tool

    Extract and analyze references from academic papers using PDF to text conversion
    and optional LLM-powered extraction.

    Examples:
        # Full workflow with Claude API (default)
        python main.py "Extract references from Introduction"

        # Use Ollama instead
        python main.py "Extract all references" --provider ollama

        # With specific model
        python main.py "Extract all references" --model llama3.2

        # Skip conversion step
        python main.py "Extract from Related Work" --no-convert

        # Manual template (no LLM)
        python main.py "Extract from Methods" --no-extract

        # Clear temporary files
        python main.py "Extract from Introduction" --clear
    """

    query: str
    """The extraction query (e.g., 'Extract references from the Introduction section')"""

    provider: str = "claude"
    """LLM provider to use: 'ollama' or 'claude' (default: claude)"""

    model: str = ""
    """LLM model to use. If not specified, uses default for provider (claude-haiku-4-5 for claude, ministral-3 for ollama)"""

    convert: bool = True
    """Convert PDFs to text (default: True). Use --no-convert to skip."""

    extract: bool = True
    """Extract references with LLM (default: True). Use --no-extract for manual template only."""

    clear: bool = True
    """Clear temporary files in tmp/ before processing (default: True)"""


def main():
    """Main entry point."""
    print_banner()

    args = tyro.cli(Args, description=Args.__doc__)

    # Set default model based on provider if not specified
    if not args.model:
        if args.provider == "claude":
            args.model = "claude-haiku-4-5"
        else:  # ollama
            args.model = "ministral-3"

    # Step 0: Clear temporary files if requested
    if args.clear:
        print("\n🗑️  Clearing temporary files...\n")
        clear_tmp_folders()
        print()

    # Step 1: Convert PDFs (if enabled)
    if args.convert:
        print("\n📄 Step 1: Converting PDFs to text...\n")
        num_converted = convert_all_pdfs()

        if num_converted == 0:
            print("\n❌ No PDFs to process. Please add PDF files to inputs/")
            return
    else:
        print("\n⏭️  Skipping PDF conversion (--no-convert)\n")

    # Step 2: Extract references (if enabled)
    if args.extract:
        print("\n🔍 Step 2: Extracting references...\n")
        print(f"Query: {args.query}")
        print(f"Provider: {args.provider}")
        print(f"Model: {args.model}\n")
        extract_from_all_papers(args.query, model=args.model, provider=args.provider)
    else:
        print("\n📝 Step 2: Generating manual template...\n")
        print(f"Query: {args.query}")
        print("Mode: Manual template generation\n")
        extract_from_all_papers(args.query, model=None, provider=args.provider)

    print("\n✅ Process complete!\n")


if __name__ == "__main__":
    main()
