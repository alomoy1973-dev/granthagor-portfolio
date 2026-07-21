import json
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('writings.json', encoding='utf-8') as f:
    data = json.load(f)
rhymes = [x for x in data if x.get('category') == 'rhyme']
print(f'Total rhymes: {len(rhymes)}')
for r in rhymes[-25:]:
    rid = r['id']
    title = r['title'][:45]
    print(f'  [{rid}] {title}')
