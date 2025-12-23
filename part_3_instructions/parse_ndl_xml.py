"""
NDL XML Parser

This script parses NDL (National Diet Library) SRU API XML responses
and extracts book titles and authors with their characters, transliterations, and dates.

Key concepts demonstrated:
- XML namespace handling
- Nested XML parsing (outer SRU response, inner RDF data)
- HTML entity unescaping
- XPath queries with namespaces
"""

import html
import re
import pandas as pd
from lxml import etree

# Namespace URIs
SRW_NS = "http://www.loc.gov/zing/srw/"
RDF_NS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
DC_NS = "http://purl.org/dc/elements/1.1/"
DCTERMS_NS = "http://purl.org/dc/terms/"
DCNDL_NS = "http://ndl.go.jp/dcndl/terms/"
FOAF_NS = "http://xmlns.com/foaf/0.1/"

# Namespace dictionary for XPath queries
namespaces = {
    'srw': SRW_NS,
    'rdf': RDF_NS,
    'dc': DC_NS,
    'dcterms': DCTERMS_NS,
    'dcndl': DCNDL_NS,
    'foaf': FOAF_NS
}


def extract_dates_from_name(name_text):
    """
    Extract date information from author name strings.
    
    Examples:
    - "山東, 京伝, 1761-1816" -> "1761-1816"
    - "喜多川, 歌麿, 1753-1806" -> "1753-1806"
    - "墨川亭, 雪麿, 1797-1856" -> "1797-1856"
    - "亀遊, 天明頃" -> "" (no dates)
    
    Args:
        name_text: String containing author name, possibly with dates
        
    Returns:
        String with dates if found, empty string otherwise
    """
    if not name_text:
        return ""
    
    # Pattern to match dates: 4 digits, optional dash, optional 4 more digits
    # Examples: "1761-1816", "1793-", "1867"
    date_pattern = r'\d{4}(?:-\d{4}|-)?'
    match = re.search(date_pattern, name_text)
    
    if match:
        return match.group(0)
    return ""


def extract_title(rdf_root):
    """
    Extract title information from RDF XML.
    
    Looks for:
    - <dc:title><rdf:Description> with <rdf:value> and <dcndl:transcription> (preferred, has transliteration)
    - <dcterms:title> (simple text, fallback)
    
    Args:
        rdf_root: Root element of the parsed RDF XML
        
    Returns:
        Dictionary with 'characters', 'transliteration', 'type', 'dates'
        or None if no title found
    """
    # Try dc:title first (has transliteration)
    title_elem = rdf_root.find('.//{%s}title' % DC_NS)
    if title_elem is not None:
        # Look for rdf:Description inside
        desc = title_elem.find('.//{%s}Description' % RDF_NS)
        if desc is not None:
            # Get characters from rdf:value
            value_elem = desc.find('.//{%s}value' % RDF_NS)
            characters = value_elem.text.strip() if value_elem is not None and value_elem.text else ''
            
            # Get transliteration from dcndl:transcription
            trans_elem = desc.find('.//{%s}transcription' % DCNDL_NS)
            transliteration = trans_elem.text.strip() if trans_elem is not None and trans_elem.text else ''
            
            if characters:
                return {
                    'characters': characters,
                    'transliteration': transliteration,
                    'type': 'title',
                    'dates': ''
                }
    
    # Fallback to dcterms:title (simpler format, no transliteration)
    title_elem = rdf_root.find('.//{%s}title' % DCTERMS_NS)
    if title_elem is not None and title_elem.text:
        return {
            'characters': title_elem.text.strip(),
            'transliteration': '',
            'type': 'title',
            'dates': ''
        }
    
    return None


def extract_authors(rdf_root):
    """
    Extract author information from RDF XML.
    
    Looks for <dcterms:creator> elements containing <foaf:Agent>
    with <foaf:name> and <dcndl:transcription>.
    
    Args:
        rdf_root: Root element of the parsed RDF XML
        
    Returns:
        List of dictionaries, each with 'characters', 'transliteration', 'type', 'dates'
    """
    authors = []
    
    # Find all dcterms:creator elements
    creator_elems = rdf_root.findall('.//{%s}creator' % DCTERMS_NS)
    
    for creator in creator_elems:
        # Look for foaf:Agent inside
        agent = creator.find('.//{%s}Agent' % FOAF_NS)
        if agent is not None:
            # Get name (characters)
            name_elem = agent.find('.//{%s}name' % FOAF_NS)
            if name_elem is not None and name_elem.text:
                name_text = name_elem.text.strip()
                
                # Extract dates from name
                dates = extract_dates_from_name(name_text)
                
                # Remove dates from name if present (for cleaner character field)
                # Keep the full name for now, can be cleaned later if needed
                characters = name_text
                
                # Get transliteration
                trans_elem = agent.find('.//{%s}transcription' % DCNDL_NS)
                transliteration = trans_elem.text.strip() if trans_elem is not None and trans_elem.text else ''
                
                authors.append({
                    'characters': characters,
                    'transliteration': transliteration,
                    'type': 'author',
                    'dates': dates
                })
    
    return authors


def parse_ndl_xml(xml_file):
    """
    Parse NDL SRU XML response and extract titles and authors.
    
    The XML has two layers:
    1. Outer SRU response with namespace http://www.loc.gov/zing/srw/
    2. Inner RDF data (escaped as HTML entities) with multiple namespaces
    
    Args:
        xml_file: Path to the XML file
        
    Returns:
        pandas DataFrame with columns: characters, transliteration, type, dates
    """
    # Parse the outer XML
    tree = etree.parse(xml_file)
    root = tree.getroot()
    
    # Extract all records
    records = root.findall('.//{%s}record' % SRW_NS)
    
    all_data = []
    
    for record in records:
        # Get recordData element
        record_data_elem = record.find('.//{%s}recordData' % SRW_NS)
        if record_data_elem is None:
            continue
        
        # Get the text content (which contains escaped XML)
        escaped_xml = record_data_elem.text
        if not escaped_xml:
            continue
        
        # Unescape HTML entities (&lt; -> <, &gt; -> >, etc.)
        unescaped_xml = html.unescape(escaped_xml)
        
        # Parse the inner RDF XML
        try:
            rdf_root = etree.fromstring(unescaped_xml.encode('utf-8'))
        except etree.XMLSyntaxError as e:
            print(f"Warning: Could not parse RDF XML: {e}")
            continue
        
        # Extract title
        title_data = extract_title(rdf_root)
        if title_data:
            all_data.append(title_data)
        
        # Extract authors
        authors_data = extract_authors(rdf_root)
        all_data.extend(authors_data)
    
    # Create DataFrame
    df = pd.DataFrame(all_data)
    
    # Ensure all columns exist even if empty
    if df.empty:
        df = pd.DataFrame(columns=['characters', 'transliteration', 'type', 'dates'])
    else:
        # Fill any missing values with empty strings
        df = df.fillna('')
    
    return df


if __name__ == "__main__":
    # Example usage
    import os
    
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
    
    print(f"\nSample titles:")
    print(df[df['type'] == 'title'].head(10))
    
    print(f"\nSample authors:")
    print(df[df['type'] == 'author'].head(10))

