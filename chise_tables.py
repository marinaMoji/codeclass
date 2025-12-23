import pandas as pd

# Load the IDS table
ids_df = pd.read_csv('daniel_tables/ids_df.csv',
    index_col=None,
    encoding='utf-8')

# cleaning
ids_df = ids_df.drop_duplicates()
ids_df = ids_df.dropna(subset=['character', 'components'], how='any')
ids_df = ids_df[~ids_df['components'].str.contains('←')]
ids_df = ids_df[~ids_df['components'].str.contains('→')]
ids_df = ids_df[~ids_df['components'].str.contains('CDP')].copy()

radical_list = [
    '一', '｜', '丶', 'ノ', '乙', '亅', '二', '亠', '人', '⺅', '𠆢', '儿', '入', 'ハ', '丷', '冂', '冖', '冫', 
    '几', '凵', '刀', '⺉', '力', '勹', '匕', '匚', '十', '卜', '卩', '厂', '厶', '又', 'マ', '九', 'ユ', '乃', 
    '𠂉', '⻌', '口', '囗', '土', '士', '夂', '夕', '大', '女', '子', '宀', '寸', '小', '⺌', '尢', '尸', '屮', 
    '山', '川', '巛', '工', '已', '巾', '干', '幺', '广', '廴', '廾', '弋', '弓', 'ヨ', '彑', '彡', '彳', '⺖', 
    '⺘', '⺡', '⺨', '⺾', '⻏', '⻖', '也', '亡', '及', '久', '⺹', '心', '戈', '戸', '手', '支', '攵', '文', '斗', 
    '斤', '方', '无', '日', '曰', '月', '木', '欠', '止', '歹', '殳', '比', '毛', '氏', '气', '水', '火', '⺣', 
    '爪', '父', '爻', '爿', '片', '牛', '犬', '⺭', '王', '元', '井', '勿', '尤', '五', '屯', '巴', '毋', '玄', 
    '瓦', '甘', '生', '用', '田', '疋', '疒', '癶', '白', '皮', '皿', '目', '矛', '矢', '石', '示', '禸', '禾', 
    '穴', '立', '⻂', '世', '巨', '冊', '母', '⺲', '牙', '瓜', '竹', '米', '糸', '缶', '羊', '羽', '而', '耒', 
    '耳', '聿', '肉', '自', '至', '臼', '舌', '舟', '艮', '色', '虍', '虫', '血', '行', '衣', '西', '臣', '見', 
    '角', '言', '谷', '豆', '豕', '豸', '貝', '赤', '走', '足', '身', '車', '辛', '辰', '酉', '釆', '里', '舛', 
    '麦', '金', '長', '門', '隶', '隹', '雨', '青', '非', '奄', '岡', '免', '斉', '面', '革', '韭', '音', '頁', 
    '風', '飛', '食', '首', '香', '品', '馬', '骨', '高', '髟', '鬥', '鬯', '鬲', '鬼', '竜', '韋', '魚', '鳥', 
    '鹵', '鹿', '麻', '亀', '啇', '黄', '黒', '黍', '黹', '無', '歯', '黽', '鼎', '鼓', '鼠', '鼻', '齊', '龠'
]

radical_list += [
    '阝', '釒', '亻', '艹', '忄', '扌', '氵', '犭', '礻', '罒', '辶', '牜', '八', '丨', '网', '丿', '刂', '𠂆',
    '黑', '𧾷', '龜', '龍', '攴'
]

import re

# TODO There are duplicates in the character column, which should be manually cleaned
# For the moment, we'll just drop them
ids_df = ids_df.drop_duplicates(subset=['character'])

# Empty list to fill with dictionaries
ls = []

# Letters to use as column names
letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Iterate through the DataFrame
for idx, row in ids_df.iterrows():
    # Set letter index counter to 0
    letter_idx = 0
    # Convert the row to a dictionary
    d = row.to_dict()
    # Extract characters from the components column
    components = row['components'] 
    # Remove structure characters
    structure_chars = '⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻'
    components = re.sub(f'[{structure_chars}]', '', components)
    # Add a radical string to the row dictionary
    d['radical_string'] = ''
    # Iterate through the characters
    for char in components:
        # If the character is in the list,
        if char in radical_list:
            # Then add it to the radical string
            d['radical_string'] += char
        # If the character ISN'T in the list,
        else:
            # Find the current letter from the letter index using slices
            letter = letters[letter_idx]
            # Add the character as the value of that key
            d[letter] = char
            # Increment the letter index counter
            letter_idx += 1
    # Append the dictionary to the list
    ls.append(d)

# Convert the list of dictionaries back to a DataFrame
ids_df = pd.DataFrame(ls)

# Fill NaN with empty string
ids_df['radical_string'] = ids_df['radical_string'].fillna('')

# Create all_components column from the original components column
# This removes structure characters but keeps all component characters (radicals + non-radicals)
def extract_all_components(components_str):
    """Extract all characters from components, removing only structure characters"""
    if pd.isna(components_str):
        return ''
    structure_chars = '⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻'
    # Remove structure characters and arrows, keep everything else
    cleaned = re.sub(f'[{structure_chars}→←]', '', str(components_str))
    return cleaned

ids_df['all_components'] = ids_df['components'].apply(extract_all_components)

print("\nFirst few rows with extracted radicals:")
print(ids_df[['character', 'components', 'radical_string', 'all_components', 'a']].head(10))
temp = ids_df[ids_df['a'].isna()]
print(f"{len(temp)}/{len(ids_df)} rows are completely broken down into radicals")



def go_deeper(df, col):
    """
    Get radicals from next level (components of components)
    param df: DataFrame to work with
    param col: column to work with
    returns df: DataFrame to work with
    """
    # Reduce DataFrame to columns we need and make copy
    cc = df[[col, 'radical_string']].copy()
    # Fill empty radical_string with the character
    cc['radical_string'] = cc['radical_string'].fillna('')
    # Drop empty rows
    cc = cc[cc['radical_string'] != ''].copy()
    cc = cc.dropna(subset=col)
    cc = cc[cc[col] != ''].copy()
    # Rename columns
    cc = cc.rename(columns={col: 'character', 'radical_string': 'new_rads'})
    # Deduplicate again TODO this might be fucked
    cc = cc.drop_duplicates(subset=['character'])
    # Merge with original DataFrame
    df = pd.merge(df, cc, on='character', how='left')
    # Fill empty radical_string with the character
    df['new_rads'] = df['new_rads'].fillna(value='')
    # Split into those with and without new_rads
    df_with = df[df['new_rads'] != ''].copy()
    df_without = df[df['new_rads'] == ''].copy()
    # Add new_rads to radical_string
    df_with['radical_string'] = df_with['radical_string'] + df_with['new_rads']
    # For df_without, the component character doesn't have radicals in our lookup
    # We should NOT add the component character itself to radical_string (it's not a radical!)
    # So we keep radical_string unchanged for df_without
    # (Previously this was: df_without['radical_string'] = df_without['radical_string'] + df_without[col]
    #  which was wrong because: 1) it adds non-radical characters, 2) NaN values cause NaN propagation)
    # Concatenate the two DataFrames
    df = pd.concat([df_with, df_without])
    # Drop new_rads column
    df = df.drop(columns=['new_rads', col])
    # Drop duplicates
    df = df.drop_duplicates()
    # Fill empty radical_string with the character
    df['radical_string'] = df['radical_string'].fillna('')
    # Return the DataFrame
    return df

# Apply the function to column a
ids_df = go_deeper(ids_df, 'a')

# Apply the function to column b
ids_df = go_deeper(ids_df, 'b')

# Cut down to needed columns (keep all_components for searching)
ids_df = ids_df[['character', 'components', 'radical_string', 'all_components']].copy()

# Search in all_components (which contains all radicals and components)
a = ids_df[
    ids_df['all_components'].str.contains('忄', na=False) &
    ids_df['all_components'].str.contains('舀', na=False)
]
print(f"\nSearch for 忄 and 舀: {len(a)} results")
print(a)

b = ids_df[
    ids_df['all_components'].str.contains('車', na=False) &
    ids_df['all_components'].str.contains('鳥', na=False)
]
print(f"\nSearch for 車 and 鳥: {len(b)} results")
print(b)

# 稻
# 糬