import docx
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Print paragraphs 86-320 to find all missing titles
doc = docx.Document("তিন্নোমুরি (TINNOMURI).docx")
paras = list(doc.paragraphs)

print("Paragraphs 80-260 (looking for missing titles):")
short_paras = []
for i in range(80, 320):
    t = paras[i].text.strip()
    # Show only short, non-poem lines that could be titles
    if t and len(t) < 50 and '\n' not in paras[i].text:
        short_paras.append((i, t))

for i, t in short_paras:
    print(f"  [{i:3d}] {t}")
