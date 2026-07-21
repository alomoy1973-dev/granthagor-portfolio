import fitz
import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = "সনার চিঝি নাগুরী-1.pdf"
doc = fitz.open(pdf_path)

# Get full TOC
toc_lines = []
for i in range(4, 8):
    page = doc[i]
    blocks = page.get_text("dict")["blocks"]
    for block in blocks:
        if block.get("type") == 0:
            for line in block.get("lines", []):
                line_text = ""
                for span in line.get("spans", []):
                    line_text += span.get("text", "")
                text = line_text.strip()
                if text:
                    toc_lines.append(text)
doc.close()

# Parse rhyme entries from TOC
pdf_rhymes = []
for line in toc_lines:
    m = re.match(r'^\((\d+)\)\s+(.+?)(?:\s*\.+\s*\d+)?\s*$', line.strip())
    if m:
        num = int(m.group(1))
        title = m.group(2).strip()
        pdf_rhymes.append((num, title))

print(f"=== PDF RHYMES (Total: {len(pdf_rhymes)}) ===")
for num, title in pdf_rhymes:
    print(f"  ({num:2d}) {title}")

# Load website rhymes
with open('writings.json', encoding='utf-8') as f:
    data = json.load(f)
website_rhymes = [x for x in data if x.get('category') == 'rhyme']

print(f"\n=== WEBSITE RHYMES (Total: {len(website_rhymes)}) ===")
for r in website_rhymes:
    # Get the number from id e.g. rhyme-03 -> 3 .. but these are website IDs not book numbers
    print(f"  [{r['id']}] {r['title'].strip()}")

print(f"\n=== SUMMARY ===")
print(f"Book (PDF): {len(pdf_rhymes)} rhymes")
print(f"Website:    {len(website_rhymes)} rhymes")
print(f"Difference: {len(pdf_rhymes) - len(website_rhymes)} rhymes MISSING from website")

print(f"\n=== MISSING RHYME NUMBERS FROM BOOK ===")
website_count = len(website_rhymes)
pdf_count = len(pdf_rhymes)
print(f"The following {pdf_count - website_count} rhymes from the book may not be on the website:")
for num, title in pdf_rhymes[website_count:]:
    print(f"  ({num}) {title}")
