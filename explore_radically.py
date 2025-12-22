"""
Example script to explore and use radically's generated data in Python.

This script demonstrates how to:
1. Load the JSON data files that radically generates
2. Search for characters by components
3. Understand character decompositions
4. Find character variants

Prerequisites:
- The radically ETL process should have been run (npm run etl)
- JSON files should exist in radically/public/json/
"""

import json
import os
from pathlib import Path

# Path to the radically submodule
RADICALLY_PATH = Path(__file__).parent / "radically" / "public" / "json"


def load_json_file(filename):
    """Load a JSON file from the radically public/json directory."""
    filepath = RADICALLY_PATH / filename
    if not filepath.exists():
        print(f"Warning: {filename} not found at {filepath}")
        print("You may need to run 'npm run etl' in the radically directory first.")
        return None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def find_characters_by_component(forward_map, component):
    """
    Find all characters that contain a specific component.
    
    Args:
        forward_map: The forwardMap.json data (component -> list of characters)
        component: A single character/radical to search for
    
    Returns:
        List of characters containing the component
    """
    return forward_map.get(component, [])


def get_character_components(reverse_map, character):
    """
    Get the component frequencies for a character.
    
    Args:
        reverse_map: The reverseMapCharFreqsOnly.json data
        character: The character to analyze
    
    Returns:
        Dictionary mapping components to their frequencies
    """
    return reverse_map.get(character, {})


def find_characters_with_multiple_components(forward_map, components):
    """
    Find characters that contain ALL of the specified components.
    
    This is a simple implementation - the actual radically algorithm
    is more sophisticated and handles frequencies.
    
    Args:
        forward_map: The forwardMap.json data
        components: List of components to search for
    
    Returns:
        Set of characters containing all components
    """
    if not components:
        return set()
    
    # Start with characters containing the first component
    result = set(find_characters_by_component(forward_map, components[0]))
    
    # Intersect with characters containing each subsequent component
    for component in components[1:]:
        chars_with_component = set(find_characters_by_component(forward_map, component))
        result = result.intersection(chars_with_component)
    
    return result


def main():
    print("=" * 60)
    print("Exploring Radically Data with Python")
    print("=" * 60)
    print()
    
    # Load the data files
    print("Loading data files...")
    forward_map = load_json_file("forwardMap.json")
    reverse_map = load_json_file("reverseMapCharFreqsOnly.json")
    base_radicals = load_json_file("baseRadicals.json")
    variants_map = load_json_file("variantsMap.json")
    
    if not forward_map:
        print("\nCannot proceed without forwardMap.json")
        print("Please run 'npm run etl' in the radically directory first.")
        return
    
    print("✓ Data loaded successfully!")
    print()
    
    # Example 1: Find characters containing a specific radical
    print("Example 1: Finding characters containing '人' (person)")
    print("-" * 60)
    characters_with_ren = find_characters_by_component(forward_map, "人")
    print(f"Found {len(characters_with_ren)} characters containing '人'")
    print(f"First 10: {characters_with_ren[:10]}")
    print()
    
    # Example 2: Analyze a specific character
    print("Example 2: Analyzing the character '蓮' (lotus)")
    print("-" * 60)
    if reverse_map:
        lian_components = get_character_components(reverse_map, "蓮")
        print(f"Components in '蓮': {lian_components}")
        print(f"Total unique components: {len(lian_components)}")
    else:
        print("reverseMapCharFreqsOnly.json not available")
    print()
    
    # Example 3: Find characters with multiple components
    print("Example 3: Finding characters containing both '人' and '車'")
    print("-" * 60)
    chars_with_both = find_characters_with_multiple_components(
        forward_map, 
        ["人", "車"]
    )
    print(f"Found {len(chars_with_both)} characters containing both '人' and '車'")
    if chars_with_both:
        print(f"Examples: {list(chars_with_both)[:10]}")
    print()
    
    # Example 4: Show base radicals
    if base_radicals:
        print("Example 4: Base radicals (cannot be further decomposed)")
        print("-" * 60)
        print(f"Total base radicals: {len(base_radicals)}")
        print(f"First 20: {base_radicals[:20]}")
        print()
    
    # Example 5: Character variants
    if variants_map:
        print("Example 5: Character variants")
        print("-" * 60)
        # Find a character with variants
        for char, variants in list(variants_map.items())[:5]:
            print(f"'{char}' has variant types: {variants}")
        print()
    
    print("=" * 60)
    print("Try modifying this script to explore more!")
    print("=" * 60)


if __name__ == "__main__":
    main()

