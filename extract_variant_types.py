"""
Extract variant type information (simplified/traditional, shinjitai/kyujitai, etc.)

This script processes the available data sources to create variantsMap.json
similar to what radically's genVariants.ts does.

Variant type codes (from CharacterVariant enum):
  1 = gukja
  2 = korean_standard
  3 = kokuji
  4 = japanese_shinjitai
  5 = japanese_kyujitai
  6 = joyo_kanji
  7 = kakikae
  8 = other_japanese
  9 = chinese_simplified
  10 = chinese_traditional
  11 = other_simplified
  12 = sawndip_simplified
  13 = sawndip
  14 = radical
  15 = unicode_pua
"""

import json
from pathlib import Path
from collections import defaultdict

# Paths
RADICALLY_DIR = Path("radically")
ETL_DIR = RADICALLY_DIR / "etl"
PUBLIC_DIR = RADICALLY_DIR / "public"
JSON_DIR = PUBLIC_DIR / "json"

# Variant type codes (matching CharacterVariant enum)
CHINESE_SIMPLIFIED = 9
CHINESE_TRADITIONAL = 10
JAPANESE_SHINJITAI = 4
JAPANESE_KYUJITAI = 5
KOREAN_STANDARD = 2
KOKUJI = 3
JOYO_KANJI = 6
KAKIKAE = 7
OTHER_JAPANESE = 8
OTHER_SIMPLIFIED = 11
SAWNDIP = 13
SAWNDIP_SIMPLIFIED = 12
RADICAL = 14
UNICODE_PUA = 15
GUKJA = 1


def get_common_traditional_characters():
    """Extract common traditional Chinese characters from cj5-tc-sourced.txt."""
    file_path = ETL_DIR / "cj5-tc-sourced.txt"
    if not file_path.exists():
        return set()
    
    chars = set()
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # Format: "a      日" - character is the last element
            parts = line.split()
            if parts:
                char = parts[-1]
                if len(char) == 1:  # Single character
                    chars.add(char)
    return chars


def get_common_simplified_characters():
    """Extract common simplified Chinese characters from cj5-sc-sourced.txt."""
    file_path = ETL_DIR / "cj5-sc-sourced.txt"
    if not file_path.exists():
        return set()
    
    chars = set()
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # Format: "a      日" - character is the last element
            parts = line.split()
            if parts:
                char = parts[-1]
                if len(char) == 1:  # Single character
                    chars.add(char)
    return chars


def get_radical_variants():
    """Extract radical variants from manual-cjkvi-variants/radical-variants.txt."""
    file_path = ETL_DIR / "manual-cjkvi-variants" / "radical-variants.txt"
    if not file_path.exists():
        return set()
    
    chars = set()
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # Format: "variant,type,target" - get target character
            parts = line.split(',')
            if len(parts) >= 3:
                target = parts[2].strip()
                if len(target) == 1:
                    chars.add(target)
    return chars


def create_variants_map():
    """
    Create variantsMap.json from available data sources.
    
    Output format: { [character: string]: number[] }
    """
    print("Creating variantsMap.json...")
    print("=" * 60)
    
    # Dictionary to store variant types for each character
    variants_map = defaultdict(set)
    
    # 1. Add Chinese Traditional characters
    print("1. Processing Traditional Chinese characters...")
    traditional_chars = get_common_traditional_characters()
    for char in traditional_chars:
        variants_map[char].add(CHINESE_TRADITIONAL)
    print(f"   Found {len(traditional_chars)} traditional characters")
    
    # 2. Add Chinese Simplified characters
    print("2. Processing Simplified Chinese characters...")
    simplified_chars = get_common_simplified_characters()
    for char in simplified_chars:
        variants_map[char].add(CHINESE_SIMPLIFIED)
    print(f"   Found {len(simplified_chars)} simplified characters")
    
    # 3. Add Radical variants
    print("3. Processing Radical variants...")
    radical_chars = get_radical_variants()
    for char in radical_chars:
        variants_map[char].add(RADICAL)
    print(f"   Found {len(radical_chars)} radical variants")
    
    # Convert sets to sorted lists for JSON serialization
    variants_map_dict = {
        char: sorted(list(variant_set))
        for char, variant_set in variants_map.items()
    }
    
    # Write to JSON
    output_file = JSON_DIR / "variantsMap.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(variants_map_dict, f, ensure_ascii=False, indent=2)
    
    print()
    print(f"✓ Created {output_file}")
    print(f"  Total characters with variant types: {len(variants_map_dict)}")
    
    # Show some examples
    print()
    print("Examples:")
    variant_names = {
        CHINESE_SIMPLIFIED: "Simplified Chinese",
        CHINESE_TRADITIONAL: "Traditional Chinese",
        JAPANESE_SHINJITAI: "Japanese Shinjitai",
        JAPANESE_KYUJITAI: "Japanese Kyujitai",
        KOREAN_STANDARD: "Korean Standard",
        RADICAL: "Radical",
    }
    
    for char in list(variants_map_dict.keys())[:10]:
        codes = variants_map_dict[char]
        names = [variant_names.get(c, f"Type {c}") for c in codes]
        print(f"  {char}: {codes} ({', '.join(names)})")
    
    return variants_map_dict


def main():
    """Main function."""
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    
    variants_map = create_variants_map()
    
    print()
    print("=" * 60)
    print("Note: This is a simplified version.")
    print("The full radically ETL process uses additional data sources:")
    print("  - CJKVI variant files")
    print("  - Japanese old style variants (jp-old-style.txt)")
    print("  - Jōyō kanji lists")
    print("  - Korean standard characters")
    print("  - Babelstone PUA data")
    print("  - And more...")
    print()
    print("For complete variant data, you would need to run:")
    print("  cd radically && npm run etl")
    print("=" * 60)


if __name__ == "__main__":
    main()

