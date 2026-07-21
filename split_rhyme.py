import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('writings.json', encoding='utf-8') as f:
    data = json.load(f)

# Find rhyme-n76 and split into two: n76 (ফুজিঁ) and n77 (উন্দুরোহান্ উল্)
for i, item in enumerate(data):
    if item.get('id') == 'rhyme-n76':
        # Fix n76 to be only ফুজিঁ (first part)
        data[i]['content'] = [
            "আমিলে ছিনলুঙ্ এক্ গজর,",
            "বাছুরির পেলুঙ্ এক্ ছাজর।",
            "ফুজিঁ মিজেলে বাছুরি,",
            "তুমবাচ্ তুমবাচ্ বাচগুরি।",
            "__STANZA__",
            "হুজি হুজি ফুজিঁ দুবো,",
            "হুবো থোইনে হুবো লেবো।",
            "উগোরেবারও চিত্ পুড়ে,",
            "চুমি চেলে পেঠ পুড়ে।"
        ]
        data[i]['excerpt'] = "আমিলে ছিনলুঙ্ এক্ গজর, বাছুরির পেলুঙ্ এক্ ছাজর।"
        
        # Insert n77 after n76
        rhyme_n77 = {
            "id": "rhyme-n77",
            "title": "উন্দুরোহান্ উল্",
            "category": "rhyme",
            "badge": "ছড়া",
            "excerpt": "ও ভুজি, ছিন ল' ফুজিঁ, গুলোদক্ সাবারাং।",
            "date": "১১/০৬/২০১৬",
            "readTime": "1 মিনিট পাঠ",
            "isFeatured": False,
            "content": [
                "ও ভুজি, ছিন ল' ফুজিঁ,",
                "গুলোদক্ সাবারাং।",
                "আবাদাঙুরি চোয়াত্ অব',",
                "উন্দুরোহান্ উল্ হেবাং।",
                "__STANZA__",
                "মিজেলে-হজালে, সাবারাং দি,",
                "দিবে সুজমুরিজ্।",
                "চাষাত্ বাঝে সং মিদিঙেঁ চুমেত্,",
                "তেলেদি আঙন্ দিস্।",
                "__STANZA__",
                "চনাহ্ চনাহ্ বাচ্ নিঘিলে,",
                "বাড়িবে চানানত্।",
                "এক্ গরাজ্ হেলে থাহর পেবে,",
                "হি উদে মনানত্।।।",
                "__STANZA__",
                "—১১/০৬/২০১৬"
            ]
        }
        data.insert(i + 1, rhyme_n77)
        print("Split rhyme-n76 and added rhyme-n77 separately!")
        break

with open('writings.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

# Verify
rhymes = [x for x in data if x.get('category') == 'rhyme']
print(f"Total rhymes now: {len(rhymes)}")
