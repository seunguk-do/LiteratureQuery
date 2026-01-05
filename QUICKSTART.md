# Quick Start Guide

## Installation

```bash
# Install dependencies
uv add pdfplumber tyro ollama

# Install Ollama (https://ollama.ai)
# Pull the default model
ollama pull ministral-3
```

## Folder Structure

```
PDF_to_Text/
├── inputs/          # Place your PDFs here
├── outputs/         # Extracted references (LLM results)
└── tmp/
    ├── txts/                   # Converted text (temporary)
    └── extraction_templates/   # Manual templates (temporary)
```

## Basic Usage

### 1. Full Workflow (Convert + Extract with LLM)

```bash
# Place PDF in inputs/
cp your_paper.pdf inputs/

# Extract with default model (ministral-3)
uv run python main.py "Extract all references from the Introduction section"

# Check results
cat outputs/your_paper_references.txt
```

### 2. Use Different Model

```bash
uv run python main.py "Extract references from Related Work" --model llama3.2
```

### 3. Skip Conversion (Use Existing Text Files)

```bash
# If you already have text files in tmp/txts/
uv run python main.py "Extract from Methodology" --no-convert
```

### 4. Generate Manual Template Only

```bash
# Generate Python template without LLM
uv run python main.py "Extract from Results" --no-extract

# Template saved to: tmp/extraction_templates/
```

### 5. Clear Temporary Files

```bash
# Clear tmp/ before processing
uv run python main.py "Extract all references" --clear
```

## Command Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--model` | `ministral-3` | Ollama model to use |
| `--convert` | `True` | Convert PDFs to text |
| `--no-convert` | - | Skip PDF conversion |
| `--extract` | `True` | Extract with LLM |
| `--no-extract` | - | Generate manual template only |
| `--clear` | `True` | Clear tmp/ before processing |
| `--no-clear` | - | Skip clearing tmp/ files |

## Example Commands

```bash
# Show help
uv run python main.py --help

# Basic extraction
uv run python main.py "Extract references from Introduction"

# Custom model
uv run python main.py "Extract all references" --model llama3.2

# Skip conversion
uv run python main.py "Extract from Methods" --no-convert

# Manual template
uv run python main.py "Extract from Results" --no-extract

# Skip clearing tmp/ files
uv run python main.py "Extract all references" --no-clear

# Combined flags
uv run python main.py "Extract from Introduction" --model llama3.2 --no-convert
```

## Typical Workflows

### First Time Use

```bash
# 1. Add PDF
cp research.pdf inputs/

# 2. Extract (converts + extracts)
uv run python main.py "Extract all references from Related Work"

# 3. View results
cat outputs/research_references.txt
```

### Process Multiple Papers

```bash
# Add all PDFs
cp paper1.pdf paper2.pdf paper3.pdf inputs/

# Process with same query
uv run python main.py "Extract all references from Introduction"

# Check outputs/
ls outputs/
```

### Use Existing Text Files

```bash
# If you already have tmp/txts/ from previous run
uv run python main.py "Extract from Methodology" --no-convert
```

### Skip Clearing (Keep Existing Files)

```bash
# Skip clearing tmp/ to reuse existing files
uv run python main.py "Extract all references" --no-clear
```

### Manual Template Workflow

```bash
# 1. Generate template
uv run python main.py "Extract from Introduction" --no-extract

# 2. Edit template
vim tmp/extraction_templates/paper_template.py

# 3. Run template
python tmp/extraction_templates/paper_template.py
```

## Available Ollama Models

| Model | Description |
|-------|-------------|
| `ministral-3` | Fast and efficient (default) |
| `llama3.2` | Balanced performance |
| `mistral` | High quality |
| `codellama` | Code-focused tasks |

Install a model:
```bash
ollama pull MODEL_NAME
```

List installed models:
```bash
ollama list
```

## Troubleshooting

**No PDFs found?**
- Make sure PDFs are in `inputs/` folder

**Ollama not running?**
```bash
ollama serve
```

**Model not found?**
```bash
ollama pull ministral-3
```

**Keep existing files?**
```bash
# Temporary files are cleared by default; use --no-clear to keep them
uv run python main.py "Extract all references" --no-clear
```
