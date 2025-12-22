"""
Example script showing how to use the extracted Unihan data.

This demonstrates how to extract:
- Stroke counts
- Readings (pronunciations, definitions)
- Variants
"""

import json
from pathlib import Path

# Path to JSON files
JSON_DIR = Path("radically/public/json")


def load_json(filename):
    """Load a JSON file."""
    filepath = JSON_DIR / filename
    if not filepath.exists():
        print(f"Error: {filename} not found at {filepath}")
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_character_info(char):
    """Get comprehensive information about a character."""
    # Load all data
    stroke_counts = load_json("strokeCount.json")
    readings = load_json("readings.json")
    variants = load_json("variants.json")
    
    if not all([stroke_counts, readings]):
        return None
    
    info = {
        "character": char,
        "stroke_count": stroke_counts.get(char),
        "readings": readings.get(char, {}),
    }
    
    # Get variants if available
    if variants:
        variant_list = variants.get(char, [])
        info["variants"] = variant_list
    
    return info


def main():
    """Example usage."""
    print("=" * 60)
    print("Using Extracted Unihan Data")
    print("=" * 60)
    print()
    
    # Example 1: Get stroke count
    print("Example 1: Stroke Counts")
    print("-" * 60)
    stroke_counts = load_json("strokeCount.json")
    if stroke_counts:
        for char in ["一", "人", "蓮", "車"]:
            count = stroke_counts.get(char)
            if count:
                print(f"  {char}: {count} strokes")
    print()
    
    # Example 2: Get readings
    print("Example 2: Readings")
    print("-" * 60)
    readings = load_json("readings.json")
    if readings:
        char = "蓮"
        char_readings = readings.get(char, {})
        print(f"  Character: {char}")
        print(f"  Pinyin (Mandarin): {char_readings.get('kMandarin', 'N/A')}")
        print(f"  Cantonese: {char_readings.get('kCantonese', 'N/A')}")
        print(f"  Japanese On: {char_readings.get('kJapaneseOn', 'N/A')}")
        print(f"  Japanese Kun: {char_readings.get('kJapaneseKun', 'N/A')}")
        print(f"  Korean: {char_readings.get('kKorean', 'N/A')}")
        print(f"  Definition: {char_readings.get('kDefinition', 'N/A')}")
    print()
    
    # Example 3: Get variants
    print("Example 3: Variants")
    print("-" * 60)
    variants = load_json("variants.json")
    if variants:
        char = "发"
        variant_list = variants.get(char, [])
        if variant_list:
            print(f"  Variants of {char}: {', '.join(variant_list)}")
        else:
            print(f"  No variants found for {char}")
    print()
    
    # Example 4: Comprehensive info
    print("Example 4: Complete Character Info")
    print("-" * 60)
    info = get_character_info("蓮")
    if info:
        print(f"  Character: {info['character']}")
        print(f"  Strokes: {info['stroke_count']}")
        print(f"  Pinyin: {info['readings'].get('kMandarin', 'N/A')}")
        print(f"  Definition: {info['readings'].get('kDefinition', 'N/A')}")
        if 'variants' in info and info['variants']:
            print(f"  Variants: {', '.join(info['variants'])}")
    print()
    
    print("=" * 60)
    print("All data files are in:", JSON_DIR)
    print("=" * 60)


if __name__ == "__main__":
    main()

