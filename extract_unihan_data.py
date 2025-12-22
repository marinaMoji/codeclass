"""
Extract dictionary data from Unihan files.

This script processes the Unihan text files in radically/public/ to extract:
- Stroke counts
- Readings (pronunciations, definitions)
- Variants

Similar to what radically's ETL process does, but in Python.
"""

import json
from pathlib import Path
from collections import defaultdict

# Paths
RADICALLY_DIR = Path("radically")
PUBLIC_DIR = RADICALLY_DIR / "public"
JSON_DIR = PUBLIC_DIR / "json"

# Create JSON directory if it doesn't exist
JSON_DIR.mkdir(parents=True, exist_ok=True)


def unicode_to_char(code_str):
    """Convert Unicode code point string (e.g., 'U+3400') to character."""
    code_point = int(code_str[2:], 16)  # Remove 'U+' and convert hex to int
    return chr(code_point)


def extract_stroke_counts(input_file, output_file):
    """
    Extract stroke counts from Unihan_IRGSources.txt.
    
    Format: U+3400	kTotalStrokes	5
    Output: { "一": 1, "人": 2, ... }
    """
    print(f"Extracting stroke counts from {input_file.name}...")
    stroke_counts = {}
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split('\t')
            if len(parts) >= 3 and parts[1] == 'kTotalStrokes':
                char = unicode_to_char(parts[0])
                # Some entries have multiple stroke counts (e.g., "8 9")
                # Take the first one, or average if needed
                stroke_value = parts[2].strip()
                if ' ' in stroke_value:
                    # Multiple values - take the first one
                    stroke_value = stroke_value.split()[0]
                stroke_counts[char] = int(stroke_value)
    
    # Write to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(stroke_counts, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Extracted {len(stroke_counts)} stroke counts")
    return stroke_counts


def extract_readings(input_file, output_file):
    """
    Extract readings from Unihan_Readings.txt.
    
    Format: U+3400	kMandarin	qiū
    Output: { "一": { "kMandarin": "yī", "kDefinition": "...", ... }, ... }
    """
    print(f"Extracting readings from {input_file.name}...")
    readings = defaultdict(dict)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split('\t')
            if len(parts) >= 3:
                char = unicode_to_char(parts[0])
                field = parts[1]
                value = parts[2]
                readings[char][field] = value
    
    # Convert defaultdict to regular dict
    readings = dict(readings)
    
    # Write to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(readings, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Extracted readings for {len(readings)} characters")
    return readings


def extract_variants(input_file, output_file):
    """
    Extract variants from Unihan_Variants.txt.
    
    Format: U+3400	kSemanticVariant	U+4E18
    Output: { "一": ["variant1", "variant2", ...], ... }
    """
    print(f"Extracting variants from {input_file.name}...")
    variants = defaultdict(set)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split('\t')
            if len(parts) >= 3:
                char = unicode_to_char(parts[0])
                variant_type = parts[1]
                variant_code = parts[2]
                
                # Handle variants - may have multiple codes or additional info
                # Split by space to handle multiple codes (e.g., "U+9DC8 U+9DC9")
                for code_part in variant_code.split():
                    # Handle codes with additional info (e.g., "U+4E18<kMatthews")
                    if code_part.startswith('U+'):
                        try:
                            clean_code = code_part.split('<')[0]
                            variant_char = unicode_to_char(clean_code)
                            variants[char].add(variant_char)
                            # Also add reverse mapping
                            variants[variant_char].add(char)
                        except (ValueError, IndexError):
                            # Skip invalid codes
                            continue
    
    # Convert sets to lists for JSON serialization
    variants_dict = {char: list(variant_set) for char, variant_set in variants.items()}
    
    # Write to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(variants_dict, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Extracted variants for {len(variants_dict)} characters")
    return variants_dict


def main():
    """Main function to extract all data."""
    print("=" * 60)
    print("Extracting Unihan Data")
    print("=" * 60)
    print()
    
    # Check if input files exist
    irg_sources = PUBLIC_DIR / "Unihan_IRGSources.txt"
    readings_file = PUBLIC_DIR / "Unihan_Readings.txt"
    variants_file = PUBLIC_DIR / "Unihan_Variants.txt"
    
    if not irg_sources.exists():
        print(f"Error: {irg_sources} not found!")
        return
    
    # Extract stroke counts
    stroke_counts = extract_stroke_counts(
        irg_sources,
        JSON_DIR / "strokeCount.json"
    )
    
    # Extract readings
    if readings_file.exists():
        readings = extract_readings(
            readings_file,
            JSON_DIR / "readings.json"
        )
    else:
        print(f"Warning: {readings_file} not found, skipping readings extraction")
    
    # Extract variants
    if variants_file.exists():
        variants = extract_variants(
            variants_file,
            JSON_DIR / "variants.json"
        )
    else:
        print(f"Warning: {variants_file} not found, skipping variants extraction")
    
    print()
    print("=" * 60)
    print("Extraction complete!")
    print(f"JSON files written to: {JSON_DIR}")
    print("=" * 60)
    
    # Show some examples
    if stroke_counts:
        print("\nExample stroke counts:")
        for char in list(stroke_counts.keys())[:5]:
            print(f"  {char}: {stroke_counts[char]} strokes")


if __name__ == "__main__":
    main()

