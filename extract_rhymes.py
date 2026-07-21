import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('writings.json', encoding='utf-8') as f:
    data = json.load(f)

rhymes = [x for x in data if x.get('category') == 'rhyme']
print(f'Total rhymes on website: {len(rhymes)}')
print()
for i, r in enumerate(rhymes, 1):
    rid = r['id']
    title = r['title']
    print(f'{i}. [{rid}] {title}')
