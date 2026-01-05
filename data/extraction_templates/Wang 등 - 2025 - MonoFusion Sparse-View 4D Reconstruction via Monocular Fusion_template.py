
# ============================================================================
# MANUAL REFERENCE EXTRACTION TEMPLATE
# Paper: Wang 등 - 2025 - MonoFusion Sparse-View 4D Reconstruction via Monocular Fusion.txt
# Query: Extract references from 'Dynamics scene reconstruction' in Section 2
# ============================================================================

import re

# Step 1: Find and paste the relevant section text here
section_text = '''
# TODO: Locate the section mentioned in your query from the text file
# and paste it here between the triple quotes
'''

# Step 2: Extract citation numbers
citation_pattern = r'\[(\d+(?:,\s*\d+)*)\]'
citations = re.findall(citation_pattern, section_text)

# Step 3: Parse and collect all reference numbers
all_refs = []
for citation in citations:
    refs = [int(ref.strip()) for ref in citation.split(',')]
    all_refs.extend(refs)

# Step 4: Get unique reference numbers
unique_refs = sorted(set(all_refs))
print(f"Total unique references: {len(unique_refs)}")
print(f"Reference numbers: {unique_refs}")

# Step 5: Find each reference in the References section and add it here
references = {
    # TODO: For each number in unique_refs, find the full reference
    # from the References section of the paper and add it like this:
    # 1: "Author Name. Paper Title. Conference/Journal, Year.",
    # 2: "Author Name. Paper Title. Conference/Journal, Year.",
}

# Step 6: Display results
print("\n" + "="*80)
print("EXTRACTED REFERENCES")
print("="*80 + "\n")

for ref_num in unique_refs:
    if ref_num in references:
        print(f"[{ref_num}] {references[ref_num]}")
        print()

# ============================================================================
# INSTRUCTIONS:
# 1. Copy this template to a new Python file
# 2. Fill in the section_text with the relevant paragraph
# 3. Fill in the references dictionary with the full reference details
# 4. Run the script to see the extracted references
# ============================================================================
