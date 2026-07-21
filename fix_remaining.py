import docx
import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('writings.json', encoding='utf-8') as f:
    data = json.load(f)

def process_content(lines):
    result = []
    for line in lines:
        # Split on internal newlines
        for subline in line.split('\n'):
            subline = subline.strip()
            if not subline:
                if result and result[-1] != '__STANZA__':
                    result.append('__STANZA__')
            else:
                result.append(subline)
    while result and result[-1] == '__STANZA__':
        result.pop()
    return result

# Remove the 9 empty entries we just added (they have 0 content)
empty_titles = {
    "হোচপাঙ্ ভিলিনে", "ওলি গীত ( ঘুমপাড়ানি গান)", "বিঝু বেড়ান্",
    "কামানি রুয়ে", "আয় তুঙ্গোবী", "কলিয়ে ভরমেল' পিত্থিমী",
    "অফিস পাড়া", "নাদঙ্ ছাড়া", "উং চুয়া প্যুঅঃ"
}
# Remove empty ones
data = [x for x in data if not (x.get('title') in empty_titles and x.get('content', []) == [])]
print(f"After cleanup: {len(data)} entries")

# =============================================
# Re-extract with improved method handling embedded newlines
# =============================================

def extract_poems_improved(filename, known_titles):
    doc = docx.Document(filename)
    
    # Build a flat list of (title_or_content, is_possible_title)
    # Some paragraphs contain BOTH title and content separated by \n
    poems = {}
    current_title = None
    current_content = []
    
    for para in doc.paragraphs:
        raw = para.text  # Don't strip yet - preserve structure
        if not raw.strip():
            if current_title:
                current_content.append('')
            continue
        
        # Check if raw text starts with a known title
        matched_title = None
        for t in known_titles:
            if raw.strip().startswith(t) or raw.strip() == t:
                matched_title = t
                break
        
        if matched_title:
            # Save previous poem
            if current_title:
                poems[current_title] = current_content[:]
            current_title = matched_title
            current_content = []
            # Check if there's content after the title in the same paragraph
            remainder = raw.strip()[len(matched_title):].strip()
            if remainder:
                for line in remainder.split('\n'):
                    current_content.append(line)
        else:
            if current_title:
                # Add all lines from this paragraph
                for line in raw.split('\n'):
                    current_content.append(line)
    
    if current_title:
        poems[current_title] = current_content
    
    return poems

# Titles to search for
tinn_targets = {
    "ওলি গীত ( ঘুমপাড়ানি গান)": "poem-tn-ex-1",
    "বিঝু বেড়ান্": "poem-tn-ex-2",
    "কামানি রুয়ে": "poem-tn-ex-3",
    "আয় তুঙ্গোবী": "poem-tn-ex-4",
    "কলিয়ে ভরমেল' পিত্থিমী": "poem-tn-ex-5",
    "অফিস পাড়া": "poem-tn-ex-6",
    "নাদঙ্ ছাড়া": "poem-tn-ex-7",
    "উং চুয়া প্যুঅঃ": "poem-tn-ex-8",
}

mono_targets = {
    "হোচপাঙ্ ভিলিনে": "poem-mp-ex-1",
}

# Extract from TINNOMURI
print("\nExtracting from তিন্নোমুরি...")
tinn_poems = extract_poems_improved(
    "তিন্নোমুরি (TINNOMURI).docx",
    list(tinn_targets.keys())
)

for title, poem_id in tinn_targets.items():
    if title in tinn_poems:
        content = process_content(tinn_poems[title])
        excerpt = content[0] if content else title
        new_poem = {
            "id": poem_id,
            "title": title,
            "category": "poem",
            "badge": "কবিতা",
            "excerpt": excerpt[:100],
            "date": "তারিখ অজানা",
            "readTime": f"{max(1, len(content)//15)} মিনিট পাঠ",
            "isFeatured": False,
            "content": content,
            "source": "তিন্নোমুরি"
        }
        data.append(new_poem)
        print(f"  ✅ Added: {title} ({len(content)} lines)")
    else:
        print(f"  ❌ Not found: {title}")

# Extract from MONPUDI
print("\nExtracting from মনপুদি...")
mono_poems = extract_poems_improved(
    "মনপুদি.docx",
    list(mono_targets.keys())
)

for title, poem_id in mono_targets.items():
    if title in mono_poems:
        content = process_content(mono_poems[title])
        excerpt = content[0] if content else title
        new_poem = {
            "id": poem_id,
            "title": title,
            "category": "poem",
            "badge": "কবিতা",
            "excerpt": excerpt[:100],
            "date": "তারিখ অজানা",
            "readTime": f"{max(1, len(content)//15)} মিনিট পাঠ",
            "isFeatured": False,
            "content": content,
            "source": "মনপুদি"
        }
        data.append(new_poem)
        print(f"  ✅ Added: {title} ({len(content)} lines)")
    else:
        print(f"  ❌ Not found: {title}")

# Save
with open('writings.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

poems_total = [x for x in data if x.get('category') == 'poem']
print(f"\n✅ Total poems now: {len(poems_total)}")
print(f"Total entries: {len(data)}")
