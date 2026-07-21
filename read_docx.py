import docx
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def read_docx_titles(filename):
    doc = docx.Document(filename)
    titles = []
    full_text = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            full_text.append(text)
    return full_text

print("=" * 60)
print("TINNOMURI (তিন্নোমুরি) - Full Content:")
print("=" * 60)
tinnomuri_lines = read_docx_titles("তিন্নোমুরি (TINNOMURI).docx")
for line in tinnomuri_lines:
    print(line)

print()
print("=" * 60)
print("MONPUDI (মনপুদি) - Full Content:")
print("=" * 60)
monpudi_lines = read_docx_titles("মনপুদি.docx")
for line in monpudi_lines:
    print(line)
