# 📚 Academic Paper Reference Extraction Tool

A Python tool to automatically extract and analyze references from academic papers. Converts PDFs to text and uses Ollama LLM for intelligent reference extraction.

## 🚀 Quick Start

```bash
# 1. Add your PDFs
cp your_paper.pdf inputs/

# 2. Extract references with LLM (default: ministral-3)
uv run python main.py "Extract references from the Introduction section"

# 3. Check results
ls outputs/
```

## ✨ Features

- **PDF to Text Conversion**: Batch convert academic papers using pdfplumber
- **Ollama LLM Integration**: Automatic extraction using local language models
- **Flexible Model Selection**: Choose from any Ollama model (ministral-3, llama3.2, etc.)
- **Manual Template Mode**: Generate Python templates for manual extraction
- **Tyro CLI**: Modern, type-safe command-line interface with boolean flags

## 📁 Project Structure

```
PDF_to_Text/
├── inputs/                      # Place your PDF files here
├── outputs/                     # Extracted references (LLM results)
├── tmp/
│   ├── txts/                    # Converted text files (temporary)
│   └── extraction_templates/    # Manual extraction templates (--no-extract)
├── convert_pdfs.py              # PDF to text conversion
├── extract_references.py        # Reference extraction engine
├── main.py                      # Main CLI interface (tyro)
└── README.md                    # This file
```

## 📖 Usage

### Installation

```bash
# Install dependencies
uv add pdfplumber tyro ollama

# Install Ollama: https://ollama.ai
# Pull a model
ollama pull ministral-3
```

### Command Reference

```bash
# Show help
uv run python main.py --help

# Basic extraction with LLM
uv run python main.py "Extract all references from the Related Work section"

# Use specific model
uv run python main.py "Extract references from Introduction" --model llama3.2

# Skip PDF conversion (use existing tmp/txts/)
uv run python main.py "Extract from Methodology" --no-convert

# Generate manual template only (no LLM)
uv run python main.py "Extract from Results" --no-extract

# Skip clearing temporary files (keep existing)
uv run python main.py "Extract all references" --no-clear
```

### Flags

- `--model MODEL` - Ollama model to use (default: ministral-3)
- `--convert` / `--no-convert` - Enable/disable PDF conversion (default: True)
- `--extract` / `--no-extract` - Enable/disable LLM extraction (default: True)
- `--clear` / `--no-clear` - Clear tmp/ files before processing (default: True)

### Example Queries

```bash
# Extract from specific section
uv run python main.py "Extract all references from the Related Work section"

# Extract from specific paragraph  
uv run python main.py "Extract references from 'Dynamics scene reconstruction' in Section 2"

# Extract by topic
uv run python main.py "Extract all references about neural radiance fields"

# Use different model
uv run python main.py "Extract all references" --model llama3.2

# Keep existing temp files
uv run python main.py "Extract from Introduction" --no-clear
```

## 🤖 Ollama Models

The tool uses Ollama for LLM-powered extraction. Default model: `ministral-3`

**Recommended models:**
- `ministral-3` - Fast and efficient (default)
- `llama3.2` - Balanced performance
- `mistral` - High quality
- `codellama` - Code-focused tasks

**Pull a model:**
```bash
ollama pull ministral-3
```

**List available models:**
```bash
ollama list
```

## 📝 How It Works

### Workflow

1. **Convert**: PDFs (inputs/) → Text (tmp/txts/) using pdfplumber
2. **Prompt**: Generate structured extraction prompt
3. **LLM**: Ollama processes the paper and extracts references
4. **Output**: Structured list of references saved to outputs/

### Two Modes

**1. LLM Mode (Default - `--extract`)**
- Uses Ollama for automatic extraction
- Configurable model selection
- Results saved to `outputs/`

**2. Manual Template Mode (`--no-extract`)**
- Generates Python template with TODOs
- Saved to `tmp/extraction_templates/`
- You fill in section text and references
- Run template to see results

### Flags Explained

**`--convert` (default: True)**
- Converts PDFs in `inputs/` to text in `tmp/txts/`
- Use `--no-convert` to skip if you already have text files

**`--extract` (default: True)**
- Uses LLM to extract references, saves to `outputs/`
- Use `--no-extract` to generate manual template instead

**`--clear` (default: True)**
- Removes all files in `tmp/txts/` and `tmp/extraction_templates/`
- Use `--no-clear` to skip clearing temporary files

## 🎯 Real-World Example

From our demonstration with the MonoFusion paper:

**Command**: 
```bash
uv run python main.py "Extract all references from 'Dynamics scene reconstruction' paragraph in Section 2"
```

**Result**: Successfully extracted 17 unique references saved to `outputs/`

## 🛠️ Advanced Usage

### Batch Processing
Process multiple papers - add them all to `inputs/`

### Skip Conversion
If you already converted PDFs:
```bash
uv run python main.py "Extract from Introduction" --no-convert
```

### Manual Template Workflow
```bash
# Generate template
uv run python main.py "Extract from Methods" --no-extract

# Fill in the template at tmp/extraction_templates/
# Then run it
python tmp/extraction_templates/paper_template.py
```

### Keep Existing Files
```bash
# Temporary files are cleared by default; use --no-clear to keep them
uv run python main.py "Extract all references" --no-clear
```

## 🐛 Troubleshooting

**PDF conversion fails?**
- Check PDF isn't encrypted
- Ensure PDF has extractable text (not scanned images)

**Ollama errors?**
```bash
# Verify Ollama is running
ollama list

# Pull the model
ollama pull ministral-3

# Check model availability
ollama list | grep ministral
```

**Model not found?**
- Pull the model: `ollama pull <model-name>`
- Check spelling of model name
- Use `ollama list` to see available models

**No PDFs found?**
- Make sure PDFs are in `inputs/` folder (not `data/pdfs/`)

## 📚 Dependencies

- **Python 3.8+**
- **pdfplumber** - PDF text extraction
- **tyro** - CLI argument parsing
- **ollama** - LLM integration
- **Ollama** - Local LLM server (separate installation)

## 🎓 Example Workflows

### Full Workflow
```bash
# Place PDF
cp research.pdf inputs/

# Extract with LLM
uv run python main.py "Extract all references from Related Work"

# Check results
cat outputs/research_references.txt
```

### Use Different Model
```bash
uv run python main.py "Categorize references by topic" --model llama3.2
```

### Manual Template
```bash
# Generate template
uv run python main.py "Extract from Introduction" --no-extract

# Edit template
vim tmp/extraction_templates/paper_template.py

# Run it
python tmp/extraction_templates/paper_template.py
```

### Default Behavior (Fresh Start)
```bash
# Temporary files are cleared automatically by default
uv run python main.py "Extract all references"
```

## 🙏 Acknowledgments

Built to streamline literature review and reference analysis. The LLM-powered approach provides accurate, automated extraction while the manual template mode ensures transparency.

## 📄 License

Open source - see LICENSE for details.
