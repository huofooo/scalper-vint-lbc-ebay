import time
import json
import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = "8182847473:AAFiNbnATsBMHWpxhDC4XMqAhElkeIkqkaw"
TELEGRAM_CHAT_ID = "-1002527933128"

VINTED_URL = "https://www.vinted.fr/catalog?search_text=Steelbook%204k&time=1747614181&currency=EUR&order=newest_first&disabled_personalization=true&page=1"
EBAY_URL = "https://www.ebay.fr/sch/i.html?_nkw=steelbook+4k&_sacat=0&_sop=10"
LEBONCOIN_URL = "https://www.leboncoin.fr/recherche?text=steelbook%204k&sort=time&order=desc"

DATA_FILE = "data.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, data=payload)

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {"vinted": [], "ebay": [], "leboncoin": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def check_vinted(data):
    print("Vérification Vinted...")
    html = requests.get(VINTED_URL, headers=HEADERS).text
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("div.feed-grid__item")
    new_items = []

    for item in items:
        link_tag = item.find("a")
        if not link_tag: continue
        link = "https://www.vinted.fr" + link_tag.get("href")
        if link not in data["vinted"]:
            title = item.get_text(strip=True)[:100]
            send_telegram_message(f"[VINTED] {title}\n{link}")
            new_items.append(link)

    data["vinted"].extend(new_items)

def check_ebay(data):
    print("Vérification eBay...")
    html = requests.get(EBAY_URL, headers=HEADERS).text
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("li.s-item")
    new_items = []

    for item in items:
        link_tag = item.find("a", class_="s-item__link")
        if not link_tag: continue
        link = link_tag.get("href")
        if link not in data["ebay"]:
            title = item.get_text(strip=True)[:100]
            send_telegram_message(f"[EBAY] {title}\n{link}")
            new_items.append(link)

    data["ebay"].extend(new_items)

def check_leboncoin(data):
    print("Vérification LeBonCoin...")
    html = requests.get(LEBONCOIN_URL, headers=HEADERS).text
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("a.styles_adCard__2YFTi")
    new_items = []

    for item in items:
        link = "https://www.leboncoin.fr" + item.get("href")
        if link not in data["leboncoin"]:
            title = item.get_text(strip=True)[:100]
            send_telegram_message(f"[LEBONCOIN] {title}\n{link}")
            new_items.append(link)

    data["leboncoin"].extend(new_items)

def main():
    print("Bot lancé. Surveillance en cours...")
    while True:
        data = load_data()
        check_vinted(data)
        check_ebay(data)
        check_leboncoin(data)
        save_data(data)
        time.sleep(120)  # 2 minutes

if __name__ == "__main__":
    main()
