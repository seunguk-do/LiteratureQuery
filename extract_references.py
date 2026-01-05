"""
Reference Extraction Module
Uses a local LLM to extract references from academic papers based on user prompts.
"""

import os
from pathlib import Path
from typing import Dict, Optional


def load_text_file(txt_path: Path) -> str:
    """Load text content from a file."""
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"✗ Error loading {txt_path.name}: {str(e)}")
        return ""


def create_extraction_prompt(paper_text: str, user_query: str) -> str:
    """
    Create a prompt for the LLM to extract references.

    Template instructions for the LLM:
    1. Identify the section/paragraph mentioned in the user query
    2. Extract all citation numbers from that section
    3. Find the full reference details from the References section
    4. Return structured output
    """
    prompt = f"""You are an expert at extracting references from academic papers.

TASK: {user_query}

PAPER TEXT:
{paper_text}

INSTRUCTIONS:
1. Locate the section or paragraph mentioned in the task
2. Extract ALL citation numbers (e.g., [1], [2, 3], etc.) from that section
3. Parse and collect all unique reference numbers
4. Find the complete reference details from the References section
5. Output the results in the following Python code format

REQUIRED OUTPUT FORMAT - Copy this template and fill it in:

```python
# Step 1: Section text found
section_text = '''
[Paste the relevant section text here]
'''

# Step 2: Citation numbers extracted
citation_pattern = r'\\[(\\d+(?:,\\s*\\d+)*)\\]'
citations = re.findall(citation_pattern, section_text)

# Step 3: Parse citation numbers
all_refs = []
for citation in citations:
    refs = [int(ref.strip()) for ref in citation.split(',')]
    all_refs.extend(refs)

# Step 4: Unique reference numbers (sorted)
unique_refs = sorted(set(all_refs))
print(f"Total unique references: {{len(unique_refs)}}")
print(f"Reference numbers: {{unique_refs}}")

# Step 5: Full reference details
references = {{
    # Fill in the reference details like this:
    # 1: "Author Name. Title. Journal/Conference, Year.",
    # 2: "Author Name. Title. Journal/Conference, Year.",
}}

# Step 6: Display results
print("\\n" + "="*80)
print("EXTRACTED REFERENCES")
print("="*80 + "\\n")

for ref_num in unique_refs:
    if ref_num in references:
        print(f"[{{ref_num}}] {{references[ref_num]}}")
        print()
```

Now execute this analysis for the given task.
"""
    return prompt


def extract_references_with_llm(
    txt_path: Path,
    user_query: str,
    model: Optional[str] = None,
    provider: str = "claude",
) -> Dict:
    """
    Extract references from a text file using an LLM.

    Args:
        txt_path: Path to the converted text file
        user_query: User's query about which references to extract
        model: LLM model name (e.g., 'ministral-3', 'claude-haiku-4-5').
               If None, generates manual template instead.
        provider: LLM provider to use ('ollama' or 'claude')

    Returns:
        Dictionary containing extracted references
    """
    print(f"\n{'=' * 70}")
    print(f"Processing: {txt_path.name}")
    print(f"Query: {user_query}")
    print(f"{'=' * 70}\n")

    # Load the paper text
    paper_text = load_text_file(txt_path)
    if not paper_text:
        return {"error": "Failed to load text file"}

    # Create the extraction prompt
    prompt = create_extraction_prompt(paper_text, user_query)

    # Manual extraction template mode (no LLM)
    if model is None:
        return manual_extraction_template(paper_text, user_query, txt_path)

    # Validate provider
    if provider not in ["ollama", "claude"]:
        print(f"✗ Invalid provider '{provider}'. Must be 'ollama' or 'claude'\n")
        return {"error": f"Invalid provider: {provider}"}

    # Route to appropriate LLM provider
    if provider == "claude":
        return extract_with_claude(prompt, txt_path, model)
    else:  # provider == "ollama"
        return extract_with_ollama(prompt, txt_path, model)


def extract_with_ollama(prompt: str, txt_path: Path, model: str) -> Dict:
    """
    Extract references using Ollama local LLM.

    Args:
        prompt: The extraction prompt
        txt_path: Path to the text file being processed
        model: Ollama model name (e.g., 'ministral-3', 'llama3.2')

    Returns:
        Dictionary with extraction results
    """
    try:
        import ollama

        print("🤖 Using Ollama local LLM for extraction...")
        print(f"   Model: {model}")
        print("   (This may take a few moments)\n")

        # Call Ollama API
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )

        result = response["message"]["content"]

        # Save the LLM output to outputs folder
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / f"{txt_path.stem}_references.txt"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)

        print(f"✓ Results saved to: {output_file}\n")

        return {"status": "success", "output": result, "output_file": str(output_file)}

    except ImportError:
        print("⚠ Ollama not installed. Install with: uv add ollama")
        print("  Or install Ollama from: https://ollama.ai\n")
        return {"error": "Ollama not installed"}
    except Exception as e:
        print(f"✗ Error with Ollama: {str(e)}\n")
        print(f"  Make sure the model '{model}' is available.")
        print(f"  Pull it with: ollama pull {model}\n")
        return {"error": str(e)}


def extract_with_claude(prompt: str, txt_path: Path, model: str) -> Dict:
    """
    Extract references using Claude API.

    Args:
        prompt: The extraction prompt
        txt_path: Path to the text file being processed
        model: Claude model name (e.g., 'claude-haiku-4-5')

    Returns:
        Dictionary with extraction results
    """
    try:
        import anthropic

        # Get API key from environment
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("✗ ANTHROPIC_API_KEY environment variable not set")
            print("  Please set your API key:")
            print("  export ANTHROPIC_API_KEY=your_key_here\n")
            return {"error": "ANTHROPIC_API_KEY not set"}

        print("🤖 Using Claude API for extraction...")
        print(f"   Model: {model}")
        print("   (This may take a few moments)\n")

        # Call Claude API
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model=model,
            max_tokens=8192,
            messages=[{"role": "user", "content": prompt}],
        )

        result = message.content[0].text

        # Save the Claude output to outputs folder
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / f"{txt_path.stem}_references.txt"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)

        print(f"✓ Results saved to: {output_file}\n")

        return {"status": "success", "output": result, "output_file": str(output_file)}

    except ImportError:
        print("⚠ Anthropic SDK not installed. Install with: uv add anthropic\n")
        return {"error": "Anthropic SDK not installed"}
    except Exception as e:
        print(f"✗ Error with Claude API: {str(e)}\n")
        print(
            f"  Make sure your API key is valid and the model '{model}' is accessible.\n"
        )
        return {"error": str(e)}


def manual_extraction_template(
    paper_text: str, user_query: str, txt_path: Path
) -> Dict:
    """
    Provide a manual extraction template and instructions.
    This is the default method when no LLM is configured.
    """
    print("📋 Manual Extraction Template Mode\n")
    print(
        "Since no LLM is configured, here's a template to manually extract references:\n"
    )

    template = f"""
# ============================================================================
# MANUAL REFERENCE EXTRACTION TEMPLATE
# Paper: {txt_path.name}
# Query: {user_query}
# ============================================================================

import re

# Step 1: Find and paste the relevant section text here
section_text = '''
# TODO: Locate the section mentioned in your query from the text file
# and paste it here between the triple quotes
'''

# Step 2: Extract citation numbers
citation_pattern = r'\\[(\\d+(?:,\\s*\\d+)*)\\]'
citations = re.findall(citation_pattern, section_text)

# Step 3: Parse and collect all reference numbers
all_refs = []
for citation in citations:
    refs = [int(ref.strip()) for ref in citation.split(',')]
    all_refs.extend(refs)

# Step 4: Get unique reference numbers
unique_refs = sorted(set(all_refs))
print(f"Total unique references: {{len(unique_refs)}}")
print(f"Reference numbers: {{unique_refs}}")

# Step 5: Find each reference in the References section and add it here
references = {{
    # TODO: For each number in unique_refs, find the full reference
    # from the References section of the paper and add it like this:
    # 1: "Author Name. Paper Title. Conference/Journal, Year.",
    # 2: "Author Name. Paper Title. Conference/Journal, Year.",
}}

# Step 6: Display results
print("\\n" + "="*80)
print("EXTRACTED REFERENCES")
print("="*80 + "\\n")

for ref_num in unique_refs:
    if ref_num in references:
        print(f"[{{ref_num}}] {{references[ref_num]}}")
        print()

# ============================================================================
# INSTRUCTIONS:
# 1. Copy this template to a new Python file
# 2. Fill in the section_text with the relevant paragraph
# 3. Fill in the references dictionary with the full reference details
# 4. Run the script to see the extracted references
# ============================================================================
"""

    # Save template
    output_dir = Path("tmp/extraction_templates")
    output_dir.mkdir(exist_ok=True)
    template_file = output_dir / f"{txt_path.stem}_template.py"

    with open(template_file, "w", encoding="utf-8") as f:
        f.write(template)

    print(f"✓ Template saved to: {template_file}")
    print(f"✓ Text file location: {txt_path}\n")
    print("Instructions:")
    print("1. Open the template file")
    print("2. Fill in the section_text and references")
    print("3. Run it to extract references\n")

    return {
        "status": "template_created",
        "template_file": str(template_file),
        "text_file": str(txt_path),
    }


def extract_from_all_papers(
    user_query: str, model: Optional[str] = None, provider: str = "claude"
):
    """Extract references from all converted papers.

    Args:
        user_query: The extraction query
        model: LLM model name. If None, generates manual templates.
        provider: LLM provider to use ('ollama' or 'claude')
    """
    txt_dir = Path("tmp/txts")
    txt_files = list(txt_dir.glob("*.txt"))

    if not txt_files:
        print("⚠ No text files found in 'tmp/txts' folder.")
        print("  Please run PDF conversion first.\n")
        return

    print(f"\n{'=' * 70}")
    print(f"Reference Extraction from {len(txt_files)} paper(s)")
    print(f"{'=' * 70}\n")

    results = []
    for txt_file in txt_files:
        result = extract_references_with_llm(txt_file, user_query, model, provider)
        results.append({"paper": txt_file.name, "result": result})

    return results


if __name__ == "__main__":
    # Example usage
    example_query = "Extract all references cited in the 'Related Work' section"

    print("Example: Reference Extraction")
    print(f"Query: {example_query}\n")

    extract_from_all_papers(example_query, model=None)
