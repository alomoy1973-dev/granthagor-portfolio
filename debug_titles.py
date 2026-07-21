import docx
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document("তিন্নোমুরি (TINNOMURI).docx")

# Print paragraphs around key titles we're missing
targets = ["ওলি", "বিঝু বেড়", "কামানি", "আয় তুঙ", "কলিয়ে", "অফিস", "নাদঙ", "উং"]

paras = list(doc.paragraphs)
for i, para in enumerate(paras):
    t = para.text.strip()
    for tgt in targets:
        if tgt in t:
            # Print surrounding context
            print(f"\n--- Found near '{tgt}' at para {i} ---")
            for j in range(max(0, i-1), min(len(paras), i+3)):
                print(f"  [{j}] repr: {repr(paras[j].text[:80])}")
            break
