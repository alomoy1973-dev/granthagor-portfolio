import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('writings.json', encoding='utf-8') as f:
    data = json.load(f)

poems = [x for x in data if x.get('category') == 'poem']
print(f"Total poems: {len(poems)}")

# Check for হোচপাঙ্
for p in poems:
    if 'হোচপাঙ' in p.get('title', ''):
        print(f"  Found: {p['title']} - content lines: {len(p.get('content', []))}")

# Show poems with 0 or very short content
print("\nPoems with very short content (possibly incomplete):")
for p in poems:
    c = len(p.get('content', []))
    if c < 3:
        print(f"  [{p['id']}] {p['title'][:40]} - {c} lines")

print("\nPoems by source:")
from collections import Counter
sources = Counter(p.get('source', 'unknown') for p in poems)
for src, cnt in sorted(sources.items()):
    print(f"  {src}: {cnt}")
