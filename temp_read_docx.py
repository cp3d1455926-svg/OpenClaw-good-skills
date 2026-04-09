import zipfile
from xml.etree import ElementTree as ET

try:
    with zipfile.ZipFile('X:\\小说\\AI 助理的逆袭.docx', 'r') as z:
        with z.open('word/document.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            texts = []
            for p in root.findall('.//w:p', ns):
                para_text = ''
                for t in p.findall('.//w:t', ns):
                    if t.text:
                        para_text += t.text
                if para_text.strip():
                    texts.append(para_text)
            
            for i, text in enumerate(texts[:50], 1):
                print(f"{i}. {text}")
                
except Exception as e:
    print(f"Error: {e}")
