import fitz
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = "সনার চিঝি নাগুরী-1.pdf"
doc = fitz.open(pdf_path)

# The missing rhymes are on book pages 67-82 (PDF pages 68-83 since page 1 is cover)
# Let's render those pages as images
output_dir = "pdf_pages"
os.makedirs(output_dir, exist_ok=True)

# Render pages 68 to 83 (0-indexed: 67 to 82)
for page_num in range(66, 82):
    page = doc[page_num]
    # Render at 2x resolution for better quality
    mat = fitz.Matrix(2, 2)
    pix = page.get_pixmap(matrix=mat)
    output_path = f"{output_dir}/page_{page_num+1:03d}.png"
    pix.save(output_path)
    print(f"Saved: {output_path}")

doc.close()
print("Done!")
