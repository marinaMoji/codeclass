# Jisho.org Character Radicals Data

This directory contains Japanese character radicals organized by stroke number, sourced from jisho.org.

## Files Available

1. **jisho_radicals.json** - JSON format (easy to use with Python's `json` module)
2. **jisho_radicals.csv** - CSV format (easy to import into databases or spreadsheets)
3. **jisho_radicals.py** - Python module (import directly into your Python code)
4. **jisho_radicals.xml** - XML format (useful for XML processing)

## Quick Start Examples

### Using the Python Module (Easiest)

```python
from data.jisho_radicals import RADICALS_BY_STROKE, ALL_RADICALS, is_radical

# Get all radicals with 3 strokes
three_stroke = RADICALS_BY_STROKE[3]
print(f"Radicals with 3 strokes: {three_stroke}")

# Check if a character is a radical
if is_radical('心'):
    print("心 is a radical!")

# Get all radicals as a flat list
print(f"Total radicals: {len(ALL_RADICALS)}")
```

### Using JSON

```python
import json

with open('data/jisho_radicals.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Access radicals by stroke count
radicals_4_strokes = data['radicals']['4']
print(radicals_4_strokes)
```

### Using CSV

```python
import csv

with open('data/jisho_radicals.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"Stroke {row['stroke_count']}: {row['radical']}")
```

### Using XML

```python
import xml.etree.ElementTree as ET

tree = ET.parse('data/jisho_radicals.xml')
root = tree.getroot()

# Find all radicals with 5 strokes
for stroke_group in root.findall("stroke_count[@value='5']"):
    for radical in stroke_group.findall('radical'):
        print(radical.text)
```

## Data Structure

The data is organized by stroke count (1-17 strokes). Each stroke count has a list of radical characters associated with it.

**Note:** Not all stroke counts are present (e.g., there are no radicals with 15 or 16 strokes in this dataset).

## Total Count

There are 214 radicals total in this dataset.

