import glob
import pandas as pd
import json
import numpy as np

# get file paths
file_paths = [f for f in glob.glob('cjkvi-id--unicode/rawdata/manual_ids/*.txt')]

file_paths += [
    'cjkvi-ids-unicode/rawdata/cjkvi-ids/ids-analysis.txt',
    'cjkvi-ids-unicode/rawdata/cjkvi-ids/ids-cdp.txt',
    'cjkvi-ids-unicode/rawdata/cjkvi-ids/ids-ext-cdef.txt',
    'cjkvi-ids-unicode/rawdata/cjkvi-ids/ids.txt',
    'cjkvi-ids-unicode/rawdata/ids/IDS-UCS-Basic.txt',
    'cjkvi-ids-unicode/rawdata/ids/IDS-UCS-Compat-Supplement.txt',
    'cjkvi-ids-unicode/rawdata/ids/IDS-UCS-Compat.txt',
    'cjkvi-ids-unicode/rawdata/ids/IDS-UCS-Ext-A.txt',
    'cjkvi-ids-unicode/rawdata/ids/IDS-UCS-Ext-B-1.txt',
    'cjkvi-ids-unicode/rawdata/ids/IDS-UCS-Ext-B-2.txt',
    'cjkvi-ids-unicode/rawdata/ids/IDS-UCS-Ext-B-3.txt',
    'cjkvi-ids-unicode/rawdata/ids/IDS-UCS-Ext-B-4.txt',
    'cjkvi-ids-unicode/rawdata/ids/IDS-UCS-Ext-B-5.txt',
    'cjkvi-ids-unicode/rawdata/ids/IDS-UCS-Ext-B-6.txt',
    'cjkvi-ids-unicode/rawdata/ids/IDS-UCS-Ext-C.txt',
    'cjkvi-ids-unicode/rawdata/ids/IDS-UCS-Ext-D.txt',
    'cjkvi-ids-unicode/rawdata/ids/IDS-UCS-Ext-E.txt',
    'cjkvi-ids-unicode/rawdata/ids/IDS-UCS-Ext-F.txt',
    'cjkvi-ids-unicode/rawdata/ids/IDS-UCS-Ext-G.txt',
    'cjkvi-ids-unicode/rawdata/ids/IDS-UCS-Ext-H.txt',
    'cjkvi-ids-unicode/rawdata/ids/IDS-UCS-Ext-I.txt'
]

# Create ids DataFrame combining all files
ids_df = pd.DataFrame()
for file_path in file_paths:
    try:
        # Solution 1: Use usecols to only read the first 3 columns
        # This prevents errors when some lines have extra fields
        df = pd.read_csv(
            file_path,
            sep='\t',
            comment='#',
            names=['code_point', 'character', 'components'],
            usecols=[0, 1, 2],  # Only read first 3 columns
            encoding='utf-8',
            on_bad_lines='skip'  # Skip lines that can't be parsed (pandas 1.3+)
        )
        if ids_df.empty:
            ids_df = df
        else:
            ids_df = pd.concat([ids_df, df])
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        continue

# Drop duplicate rows
ids_df = ids_df.drop_duplicates()

# Save to csv
ids_df.to_csv('daniel_tables/ids_df.csv', index=False)

# Create shin-kyu table
shin_kyu_df = pd.read_csv(
    'cjkvi-variants/jp-old-style.txt',
    sep='\t',
    comment='#',
    skiprows=22,
    names=['shin', 'kyu'],
    usecols=[0, 1],  # Only read first 2 columns
    encoding='utf-8',
    on_bad_lines='skip'  # Skip lines that can't be parsed (pandas 1.3+)
)
temp = pd.read_csv(
    'cjkvi-variants/joyo-variants.txt',
    sep=',',
    comment='#',
    skiprows=5,
    names=['shin', 'd', 'kyu'],
    usecols=[0, 1, 2],  # Only read first 3 columns
    encoding='utf-8',
    on_bad_lines='skip'  # Skip lines that can't be parsed (pandas 1.3+)
)
temp = temp[['shin', 'kyu']]

# From shinjitai-table
with open('../shinjitai-table/shinjitai.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    
# Convert to a more usable format
# Create a list of dictionaries for each character-variant pair
shinjitai_list = []
for shinjitai, kyujitai_list in data.items():
    if kyujitai_list:  # Only if there are variants
        for kyujitai in kyujitai_list:
            shinjitai_list.append({
                'shin': shinjitai,
                'kyu': kyujitai
            })

df_shinjitai = pd.DataFrame(shinjitai_list)

# Concatenate DataFrames
shin_kyu_df = pd.concat([shin_kyu_df, temp, df_shinjitai])

# Drop duplicate rows
shin_kyu_df = shin_kyu_df.drop_duplicates()

# Save to csv
shin_kyu_df.to_csv('daniel_tables/shin_kyu_df.csv', index=False)

# Stroke count table
stroke_count_df = pd.read_csv(
    'cjkvi-ids/ucs-strokes.txt',
    sep='\t',
    comment='#',
    names=['code_point', 'character', 'stroke_count'],
    usecols=[0, 1, 2],  # Only read first 3 columns
    encoding='utf-8',
    on_bad_lines='skip'  # Skip lines that can't be parsed (pandas 1.3+)
)

# Save to csv
stroke_count_df.to_csv('daniel_tables/stroke_count_df.csv', index=False)


"""
First, as an exercise, I will have my collaborator go to https://jisho.org/#radical and copy and paste all the radicals into gedit.

1一｜丶ノ乙亅2二亠人⺅𠆢儿入ハ丷冂冖冫几凵刀⺉力勹匕匚十卜卩厂厶又マ九ユ乃𠂉3⻌口囗土士夂夕大女子宀寸小⺌尢尸屮山川巛工已巾干幺广廴廾弋弓ヨ彑彡彳⺖⺘⺡⺨⺾⻏⻖也亡及久4⺹心戈戸手支攵文斗斤方无日曰月木欠止歹殳比毛氏气水火⺣爪父爻爿片牛犬⺭王元井勿尤五屯巴毋5玄瓦甘生用田疋疒癶白皮皿目矛矢石示禸禾穴立⻂世巨冊母⺲牙6瓜竹米糸缶羊羽而耒耳聿肉自至臼舌舟艮色虍虫血行衣西7臣見角言谷豆豕豸貝赤走足身車辛辰酉釆里舛麦8金長門隶隹雨青非奄岡免斉9面革韭音頁風飛食首香品10馬骨高髟鬥鬯鬲鬼竜韋11魚鳥鹵鹿麻亀啇黄黒12黍黹無歯13黽鼎鼓鼠14鼻齊17龠

Then, she will use regex to remove numbers and create a list for use in python. 
"""

# Resulting list:

radicals = [
    '一', '｜', '丶', 'ノ', '乙', '亅', '二', '亠', '人', '⺅', '𠆢', '儿', '入', 'ハ', '丷', '冂', '冖', '冫', 
    '几', '凵', '刀', '⺉', '力', '勹', '匕', '匚', '十', '卜', '卩', '厂', '厶', '又', 'マ', '九', 'ユ', '乃', 
    '𠂉', '⻌', '口', '囗', '土', '士', '夂', '夕', '大', '女', '子', '宀', '寸', '小', '⺌', '尢', '尸', '屮', 
    '山', '川', '巛', '工', '已', '巾', '干', '幺', '广', '廴', '廾', '弋', '弓', 'ヨ', '彑', '彡', '彳', '⺖', 
    '⺘', '⺡', '⺨', '⺾', '⻏⻖', '也', '亡', '及', '久', '⺹', '心', '戈', '戸', '手', '支', '攵', '文', '斗', 
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