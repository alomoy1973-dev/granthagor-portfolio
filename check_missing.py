import docx
import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('writings.json', encoding='utf-8') as f:
    data = json.load(f)
website_poems = [x for x in data if x.get('category') == 'poem']
website_titles_set = set(p['title'].strip() for p in website_poems)

print(f"Current poems on website: {len(website_poems)}")

# Check which titles from our list are still missing
monpudi_missing = [
    "হোচপাঙ্ ভিলিনে",
]

tinn_missing_check = [
    "ওলি গীত ( ঘুমপাড়ানি গান)", "বিঝু বেড়ান্",
    "কামানি রুয়ে", "আয় তুঙ্গোবী",
    "কলিয়ে ভরমেল' পিত্থিমী", "অফিস পাড়া",
    "নাদঙ্ ছাড়া", "উং চুয়া প্যুঅঃ"
]

print("\nChecking still-missing poems:")
for t in monpudi_missing + tinn_missing_check:
    found = t in website_titles_set
    print(f"  {'✓' if found else '❌'} {t}")
