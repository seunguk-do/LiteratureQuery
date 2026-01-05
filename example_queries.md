# Example Queries for Reference Extraction

This document provides example queries you can use to extract references from academic papers.

## Basic Queries

### Extract from Specific Sections

```bash
# Extract all references from the Introduction
python main.py --extract "Extract all references cited in the Introduction section"

# Extract from Related Work
python main.py --extract "Extract all references from the Related Work section"

# Extract from Methodology
python main.py --extract "Extract references from the Methodology section"

# Extract from Results and Discussion
python main.py --extract "List all references in Results and Discussion"
```

### Extract from Specific Paragraphs

```bash
# Extract from a specific paragraph
python main.py --extract "Extract references from the paragraph titled 'Dynamic scene reconstruction' in Section 2"

# Extract from multiple paragraphs
python main.py --extract "Extract references from paragraphs about 'neural networks' and 'deep learning'"
```

### Extract by Topic

```bash
# Extract references about a specific topic
python main.py --extract "Extract all references related to '3D reconstruction'"

# Extract methodological references
python main.py --extract "Find all references about datasets and evaluation metrics"

# Extract technique-specific references
python main.py --extract "List references about Gaussian Splatting and NeRF"
```

## Advanced Queries

### Categorical Extraction

```bash
# Extract classical work
python main.py --extract "Extract all references to classical or foundational work mentioned in the paper"

# Extract recent work
python main.py --extract "List all references from 2023 and 2024"

# Extract survey papers
python main.py --extract "Find all survey papers and review articles cited"
```

### Comparative Analysis

```bash
# Extract baseline comparisons
python main.py --extract "Extract all references to methods that are compared as baselines"

# Extract prior art
python main.py --extract "List all references cited as prior art or previous work"
```

### Domain-Specific Queries

#### Computer Vision
```bash
python main.py --extract "Extract references about image processing and computer vision"
python main.py --extract "Find papers about object detection and segmentation"
```

#### Machine Learning
```bash
python main.py --extract "Extract all deep learning and neural network references"
python main.py --extract "List papers about transformer architectures"
```

#### Robotics
```bash
python main.py --extract "Extract references related to robotic manipulation"
python main.py --extract "Find papers about SLAM and 3D mapping"
```

## Using with Ollama LLM

For automatic extraction with a local LLM:

```bash
# Basic extraction with Ollama
python main.py --extract "Extract all references from Introduction" --llm ollama

# Complex query with Ollama
python main.py --extract "Categorize and extract references by: classical methods, neural approaches, and recent advances" --llm ollama
```

## Query Templates

### Template 1: Section-Based
```
Extract all references cited in the [SECTION_NAME] section
```

### Template 2: Paragraph-Based
```
Extract references from the paragraph about [TOPIC] in Section [NUMBER]
```

### Template 3: Topic-Based
```
List all references related to [TOPIC_1], [TOPIC_2], and [TOPIC_3]
```

### Template 4: Chronological
```
Extract all references published [before/after/during] [YEAR]
```

### Template 5: Type-Based
```
Find all [journal/conference/arxiv/survey] papers cited in the paper
```

## Tips for Effective Queries

1. **Be Specific**: Mention exact section names as they appear in the paper
   - Good: "Extract from 'Related Work' section"
   - Better: "Extract from Section 2.1 'Dynamic Scene Reconstruction'"

2. **Use Keywords**: Include specific technical terms
   - "Extract references about '3D Gaussian Splatting'"

3. **Combine Criteria**: You can combine multiple conditions
   - "Extract all NeRF-related references from the Introduction and Related Work sections"

4. **Specify Output Format**: If using LLM, you can request specific formatting
   - "Extract and categorize references from Related Work into: classical methods, neural approaches, and hybrid techniques"

## Common Use Cases

### Literature Review
```bash
python main.py --extract "Extract all references and categorize them by research area"
```

### Baseline Identification
```bash
python main.py --extract "List all methods mentioned as baselines or comparison points"
```

### Dataset Discovery
```bash
python main.py --extract "Find all datasets and benchmarks cited in the paper"
```

### Method Genealogy
```bash
python main.py --extract "Extract references that this work builds upon or extends"
```
