import re

# Read the extracted text file
with open('outputs/Wang 등 - 2025 - MonoFusion Sparse-View 4D Reconstruction via Monocular Fusion.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Reference numbers we're looking for
ref_numbers = [2, 4, 7, 9, 18, 26, 30, 33, 35, 38, 40, 41, 50, 52, 54, 58, 64]

print("=" * 80)
print("LITERATURES CITED IN 'DYNAMICS SCENE RECONSTRUCTION' PARAGRAPH")
print("Section 2. Related Works")
print("=" * 80)
print()

# Find References section
references_start = text.find('References')
if references_start == -1:
    references_start = text.find('[1]')

references_text = text[references_start:]

# Extract each reference
for ref_num in ref_numbers:
    # Pattern to match reference number and its content
    # Match from [N] to the next [N+1] or end
    pattern = rf'\[{ref_num}\]\s+(.*?)(?=\n\[|\nAppendix|\n\d+\n|$)'

    match = re.search(pattern, references_text, re.DOTALL)

    if match:
        ref_text = match.group(1).strip()
        # Clean up the reference text - remove extra whitespace and line breaks
        ref_text = re.sub(r'\s+', ' ', ref_text)

        print(f"[{ref_num}] {ref_text}")
        print()
    else:
        print(f"[{ref_num}] NOT FOUND")
        print()

print("=" * 80)
print(f"Total: {len(ref_numbers)} references")
print("=" * 80)
