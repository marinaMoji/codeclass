"""
NDL XML Parser (Beginner-Friendly Version)

This is a simplified version designed for learning XML parsing.
Perfect for students learning to parse XML in 1-2 hours.

The pipeline is clear and linear:
1. Read the XML file
2. Parse it with BeautifulSoup
3. Find all records
4. For each record, extract titles and authors
5. Build a list of dictionaries
6. Convert to DataFrame

Key learning points:
- BeautifulSoup makes XML parsing simple: soup.find('tag')
- The pipeline shape is clear: read → parse → iterate → extract → DataFrame
- Helper functions (like extract_dates_from_name) show decomposition
- We handle the nested XML structure, but keep it simple
"""

import re
import pandas as pd
from bs4 import BeautifulSoup


def extract_dates_from_name(name_text):
    """
    Extract date patterns from author names.
    
    Examples:
    - "山東, 京伝, 1761-1816" -> "1761-1816"
    - "喜多川, 歌麿, 1753-1806" -> "1753-1806"
    - "亀遊, 天明頃" -> "" (no dates)
    """
    if not name_text:
        return ""
    
    # Look for patterns like "1761-1816" or "1793-"
    match = re.search(r'\d{4}(?:-\d{4}|-)?', name_text)
    return match.group(0) if match else ""


def parse_ndl_xml(xml_file):
    """
    Parse NDL XML and extract titles and authors.
    
    Simple pipeline that's easy to follow:
    1. Read the file
    2. Parse with BeautifulSoup
    3. Find all records
    4. Extract data from each record
    5. Return as DataFrame
    """
    # Step 1: Read the file
    with open(xml_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Step 2: Parse the outer XML structure
    # BeautifulSoup automatically handles HTML entities (&lt; becomes <)
    soup = BeautifulSoup(content, 'xml')
    
    # Step 3: Find all record elements
    # Each record contains information about one book
    records = soup.find_all('record')
    
    # Step 4: Extract data from each record
    # We'll build a list of dictionaries, then convert to DataFrame
    all_data = []
    
    for record in records:
        # Each record has a 'recordData' element that contains the book info
        # The book info is stored as escaped XML, so we need to parse it again
        record_data = record.find('recordData')
        if not record_data or not record_data.text:
            continue
        
        # Parse the inner XML (the actual book data)
        # BeautifulSoup automatically unescapes it for us
        book_soup = BeautifulSoup(record_data.text, 'xml')
        
        # Extract title
        # Titles can be in two formats:
        # 1. dc:title with nested rdf:Description (has transliteration)
        # 2. dcterms:title (simple text, no transliteration)
        
        # Try the complex format first (has transliteration)
        dc_title = book_soup.find('dc:title')
        if dc_title:
            # The title might be nested inside rdf:Description
            desc = dc_title.find('rdf:Description')
            if desc:
                # Get the actual title text
                value = desc.find('rdf:value')
                # Get the transliteration (romanized reading)
                transcription = desc.find('dcndl:transcription')
                
                if value and value.text:
                    all_data.append({
                        'characters': value.text.strip(),
                        'transliteration': transcription.text.strip() if transcription and transcription.text else '',
                        'type': 'title',
                        'dates': ''
                    })
        
        # Fallback to simple format (no transliteration)
        if not dc_title or not dc_title.find('rdf:Description'):
            title_elem = book_soup.find('dcterms:title')
            if title_elem and title_elem.text:
                all_data.append({
                    'characters': title_elem.text.strip(),
                    'transliteration': '',
                    'type': 'title',
                    'dates': ''
                })
        
        # Extract authors
        # Authors are in dcterms:creator elements
        creators = book_soup.find_all('dcterms:creator')
        
        for creator in creators:
            # Authors are stored in foaf:Agent elements
            # (FOAF = Friend of a Friend, a standard for describing people)
            agent = creator.find('foaf:Agent')
            if agent:
                # Get the author's name
                name = agent.find('foaf:name')
                # Get the transliteration
                transcription = agent.find('dcndl:transcription')
                
                if name and name.text:
                    name_text = name.text.strip()
                    # Extract dates from the name (e.g., "1761-1816")
                    dates = extract_dates_from_name(name_text)
                    
                    all_data.append({
                        'characters': name_text,
                        'transliteration': transcription.text.strip() if transcription and transcription.text else '',
                        'type': 'author',
                        'dates': dates
                    })
    
    # Step 5: Create DataFrame
    df = pd.DataFrame(all_data)
    
    # Handle empty case
    if df.empty:
        df = pd.DataFrame(columns=['characters', 'transliteration', 'type', 'dates'])
    else:
        df = df.fillna('')
    
    return df


if __name__ == "__main__":
    import os
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    xml_file = os.path.join(script_dir, "sru_first_20.xml")
    
    df = parse_ndl_xml(xml_file)
    
    print(f"Extracted {len(df)} records")
    print(f"\nDataFrame shape: {df.shape}")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nFirst few rows:")
    print(df.head(20))
    
    print(f"\nType distribution:")
    print(df['type'].value_counts())

