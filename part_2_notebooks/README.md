# Pandas DataFrames Tutorial - Jupyter Notebooks

This directory contains Jupyter notebook tutorials for learning Pandas DataFrames using real CJK (Chinese, Japanese, Korean) character data. These notebooks are designed to teach practical data manipulation skills needed for dictionary and character composer work.

## Prerequisites

Before starting these notebooks, you should have completed the notebooks in `../part_1_notebooks/`, which cover:
- Python basics (variables, types, control flow)
- Strings, lists, and dictionaries
- Functions and file operations
- Regular expressions

## Notebook Series Overview

This series consists of 8 notebooks that progressively build your Pandas skills:

1. **00_Pandas_Introduction.ipynb** - Introduction to Pandas and basic concepts
2. **01_Loading_Data.ipynb** - Loading data from CSV, JSON, and TSV files
3. **02_Exploring_DataFrames.ipynb** - Inspecting and exploring DataFrame structure
4. **03_Filtering_Data.ipynb** - Filtering and selecting data with boolean indexing
5. **04_Merging_Datasets.ipynb** - Merging and joining multiple datasets (most critical)
6. **05_Creating_Dictionary_Tables.ipynb** - Transforming data and creating lookup tables
7. **06_Basic_Statistics_and_GroupBy.ipynb** - Basic statistics and grouping operations
8. **07_Practical_Project.ipynb** - Complete end-to-end workflow project

## Time Allocation

The complete series takes approximately 2.5-3 hours to work through. In a teaching context, some content may be skipped to allow time for exercises and practice.

## Data Sources

All notebooks use real CJK character data from the following submodules:

### cjkvi-variants/
Contains variant character data in CSV-like format:
- `cjkvi-simplified.txt` - Simplified/traditional Chinese character mappings
- `joyo-variants.txt` - Japanese Jōyō kanji variants
- `jp-old-style.txt` - Japanese shinjitai/kyujitai variants
- And many more variant relationship files

### shinjitai-table/
Contains Japanese variant data in JSON format:
- `shinjitai.json` - Modern Japanese characters with their traditional forms
- `kyujitai.json` - Traditional Japanese characters

### cjkvi-ids-unicode/
Contains IDS (Ideographic Description Sequence) data:
- `rawdata/cjkvi-ids/ids.txt` - Full IDS dataset with ~89,000 character decompositions
- Tab-separated format showing how characters are built from components
- Note: The file has a 2-line copyright header that should be skipped when loading

## Learning Objectives

By the end of this series, you will be able to:

- Load data from various file formats (CSV, JSON, TSV)
- Inspect and explore DataFrame structure
- Filter and select data based on conditions
- **Merge multiple datasets** (critical skill for your work)
- Transform data and create lookup tables
- Perform basic statistical analysis with groupby
- Build complete data processing workflows

## Key Focus Areas

This tutorial emphasizes:

1. **Merging datasets** - Essential for combining variant data, IDS data, and character information
2. **Filtering and selection** - Finding specific characters, variants, or relationships
3. **Creating lookup tables** - Building dictionaries and character composer data structures
4. **Practical workflows** - Real-world data processing for CJK character research

## Reference Materials

For deeper learning, refer to the comprehensive **PANDAS-TUTORIAL** in `../PANDAS-TUTORIAL/`. That tutorial covers:
- Advanced statistics and visualization
- Time series analysis
- More complex data transformations
- Data visualization with graphs

This series focuses specifically on data manipulation skills needed for dictionary and character composer work, using domain-relevant CJK character data.

## How to Use

1. **Install Pandas** (if not already installed):
   ```bash
   pip install pandas
   ```

2. **Launch Jupyter Notebook**:
   ```bash
   jupyter notebook
   ```

3. **Work through notebooks in order**:
   - Start with `00_Pandas_Introduction.ipynb`
   - Complete each notebook before moving to the next
   - Try the "Try It Yourself" exercises for practice

4. **Practice at home**:
   - Each notebook includes exercises you can complete independently
   - Experiment with the data sources
   - Try creating your own lookup tables

## Data File Paths

When working with the notebooks, data files are referenced relative to the repository root:
- `../cjkvi-variants/` - Variant data files
- `../shinjitai-table/` - Japanese variant JSON files
- `../cjkvi-ids-unicode/rawdata/cjkvi-ids/ids.txt` - Full IDS dataset (~89,000 characters)

## Next Steps

After completing this series, you'll be ready for:
- Part 3: Working with AI assistance for data analysis
- Part 4: Advanced data processing and automation
- Building your own character lookup tools
- Processing CHISE and other CJK character databases

Happy learning! 🎓

