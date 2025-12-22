# Guide: Handling TSV Tokenizing Errors in Pandas

## The Problem

When loading TSV (Tab-Separated Values) files with `pd.read_csv()`, you might encounter errors like:

```
pandas.errors.ParserError: Error tokenizing data. C error: Expected 5 fields in line 3, saw 6
```

This happens when:
- Some lines have **more tab-separated fields** than expected
- The file format is **inconsistent** (some rows have extra columns)
- There are **header lines** or **comment lines** that need to be skipped

## Solutions

### Solution 1: Use `usecols` to Read Only Specific Columns (Recommended)

If you only need the first N columns, tell pandas to ignore extra columns:

```python
df = pd.read_csv(
    'file.tsv',
    sep='\t',
    usecols=[0, 1, 2],  # Only read first 3 columns
    names=['col1', 'col2', 'col3'],
    encoding='utf-8'
)
```

**Why this works**: Even if line 3 has 6 fields, pandas will only read the first 3 and ignore the rest.

### Solution 2: Skip Bad Lines

If you want to skip lines that can't be parsed:

```python
# For pandas 1.3+ (including pandas 2.0+)
df = pd.read_csv(
    'file.tsv',
    sep='\t',
    on_bad_lines='skip',  # Skip problematic lines
    encoding='utf-8'
)

# For older pandas (< 1.3)
df = pd.read_csv(
    'file.tsv',
    sep='\t',
    error_bad_lines=False,  # Deprecated but works in older versions
    encoding='utf-8'
)
```

**Warning**: This will silently skip data! Use only if you're okay losing those rows.

### Solution 3: Skip Header/Comment Lines

If the file has header lines or comments at the top:

```python
df = pd.read_csv(
    'file.tsv',
    sep='\t',
    skiprows=2,  # Skip first 2 lines
    comment='#',  # Skip lines starting with #
    encoding='utf-8'
)
```

### Solution 4: Diagnose the Problem First

Before fixing, check what's wrong:

```python
# Check how many fields each line has
with open('file.tsv', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i < 10:  # Check first 10 lines
            fields = line.split('\t')
            print(f"Line {i+1}: {len(fields)} fields")
            if len(fields) > 3:
                print(f"  Extra fields: {fields[3:]}")
```

### Solution 5: Combine Multiple Solutions

For complex files, combine approaches:

```python
df = pd.read_csv(
    'file.tsv',
    sep='\t',
    skiprows=2,  # Skip header
    comment='#',  # Skip comments
    usecols=[0, 1, 2],  # Only first 3 columns
    names=['code_point', 'character', 'components'],
    encoding='utf-8',
    on_bad_lines='skip'  # Skip any remaining problematic lines
)
```

## Example: Loading IDS Data

For the IDS files in `cjkvi-ids-unicode`, use:

```python
df = pd.read_csv(
    'cjkvi-ids-unicode/rawdata/cjkvi-ids/ids.txt',
    sep='\t',
    skiprows=2,  # Skip copyright header
    usecols=[0, 1, 2],  # Only read: unicode, character, first IDS
    names=['unicode', 'character', 'ids'],
    encoding='utf-8',
    on_bad_lines='skip'
)
```

**Why**: Some characters have multiple IDS decompositions in the same line (extra tab-separated fields), but we only need the first one.

## Quick Reference

| Problem | Solution |
|---------|----------|
| Too many fields in some lines | Use `usecols=[0, 1, 2]` |
| Want to skip bad lines | Use `on_bad_lines='skip'` |
| Header lines at top | Use `skiprows=N` |
| Comment lines | Use `comment='#'` |
| Need to diagnose | Check line field counts manually |

## Best Practice

**Always use `usecols` when you know which columns you need!** This is the safest and most efficient solution.

