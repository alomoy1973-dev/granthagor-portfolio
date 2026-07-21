import fitz  # PyMuPDF
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = "সনার চিঝি নাগুরী-1.pdf"

doc = fitz.open(pdf_path)
print(f"Total pages in PDF: {doc.page_count}")
print("=" * 60)

full_text = ""
for i, page in enumerate(doc):
    text = page.get_text()
    full_text += text
    print(f"\n--- PAGE {i+1} ---")
    print(text)

doc.close()
