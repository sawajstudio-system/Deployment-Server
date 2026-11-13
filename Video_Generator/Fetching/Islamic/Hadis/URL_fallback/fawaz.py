import os
import re
import random
import requests

BASE_URLS = [
    "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1",
    "https://raw.githubusercontent.com/fawazahmed0/hadith-api/1",
]

BOOKS = [
    {"eng": "eng-bukhari", "ara": "ara-bukhari", "name": "Sahih al-Bukhari", "max": 7563},
    {"eng": "eng-muslim", "ara": "ara-muslim", "name": "Sahih Muslim", "max": 7450},
    {"eng": "eng-abudawud", "ara": "ara-abudawud", "name": "Sunan Abu Dawud", "max": 5274},
    {"eng": "eng-tirmidhi", "ara": "ara-tirmidhi", "name": "Jami at-Tirmidhi", "max": 3956},
    {"eng": "eng-nasai", "ara": "ara-nasai", "name": "Sunan an-Nasa'i", "max": 5758},
    {"eng": "eng-ibnmajah", "ara": "ara-ibnmajah", "name": "Sunan Ibn Majah", "max": 4341},
]

def _sanitize(text):
    if not text: return ""
    text = re.sub(r"[\u200b-\u200f\ufeff\u202a-\u202e]", "", str(text))
    text = text.replace("\n", " ").replace("\r", " ")
    return re.sub(r"\s+", " ", text).strip()

def fetch(book=None, number=None):
    if book:
        matching = [b for b in BOOKS if book.lower() in b["eng"]]
        selected_book = matching[0] if matching else random.choice(BOOKS)
    else:
        selected_book = random.choice(BOOKS)

    # 🟢 5 बार ट्राई करेगा ताकि हमें अरबी टेक्स्ट जरूर मिल जाए
    for attempt in range(5):
        hadith_num = int(number) if number else random.randint(1, selected_book["max"])

        for base in BASE_URLS:
            try:
                # 1. इंग्लिश फेच करो
                url_eng = f"{base}/editions/{selected_book['eng']}/{hadith_num}.json"
                r = requests.get(url_eng, timeout=15)
                if r.status_code != 200: continue
                    
                data = r.json()
                hadiths = data.get("hadiths", [])
                if not hadiths: continue
                    
                first = hadiths[0]
                eng_text = _sanitize(first.get("text", ""))
                if len(eng_text) < 30: continue

                # 2. अरबी फेच करो
                ara_text = ""
                try:
                    url_ara = f"{base}/editions/{selected_book['ara']}/{hadith_num}.json"
                    r2 = requests.get(url_ara, timeout=10)
                    if r2.status_code == 200:
                        ara_hadiths = r2.json().get("hadiths", [])
                        if ara_hadiths: 
                            ara_text = _sanitize(ara_hadiths[0].get("text", ""))
                except Exception: 
                    pass

                # 🟢 अगर अरबी टेक्स्ट नहीं मिला, तो अगली हदीस ट्राई करो
                if not ara_text:
                    print(f"[fawaz] ⚠️ Arabic missing for Hadith #{hadith_num}, trying next...")
                    break # Inner loop से बाहर निकलो, नई हदीस नंबर जनरेट करो

                print(f"[fawaz] ✅ Success! Hadith No. {hadith_num} (Arabic + English)")
                return {
                    "collection": selected_book["name"],
                    "number": str(first.get("hadithnumber") or hadith_num),
                    "english": eng_text,
                    "arabic": ara_text,
                    "source": "API"
                }
            except Exception as e:
                continue

    # अगर 5 बार में भी अरबी नहीं मिली, तो हार्डकोडेड बैकअप
    print("[fawaz] ⚠️ Could not find Hadith with Arabic. Using Hardcoded Fallback.")
    return _hardcoded()

def _hardcoded():
    fallback_hadiths = [
        {"collection": "Sahih al-Bukhari", "number": "1", "english": "The reward of deeds depends upon the intentions and every person will get the reward according to what he has intended.", "arabic": "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى", "source": "Hardcoded"},
        {"collection": "Sahih al-Bukhari", "number": "13", "english": "None of you will have faith till he wishes for his (Muslim) brother what he likes for himself.", "arabic": "لاَ يُؤْمِنُ أَحَدُكُمْ حَتَّى يُحِبَّ لأَخِيهِ مَا يُحِبُّ لِنَفْسِهِ", "source": "Hardcoded"},
        {"collection": "Sahih Muslim", "number": "45", "english": "No one of you becomes a true believer until he likes for his brother what he likes for himself.", "arabic": "لاَ يُؤْمِنُ أَحَدُكُمْ حَتَّى يُحِبَّ لأَخِيهِ مَا يُحِبُّ لِنَفْسِهِ", "source": "Hardcoded"}
    ]
    return random.choice(fallback_hadiths)
