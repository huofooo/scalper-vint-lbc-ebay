import requests
import time
from bs4 import BeautifulSoup

# Telegram
TOKEN = "8182847473:AAFiNbnATsBMHWpxhDC4XMqAhElkeIkqkaw"
CHAT_ID = "-1002527933128"

# URL Vinted
VINTED_URL = "https://www.vinted.fr/catalog?search_text=steelbook%204k&search_id=23485255761&order=newest_first&time=1747726758&catalog[]=3042&disabled_personalization=true&page=1"

# Pour stocker les ID déjà envoyés
seen_items = set()

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, data=data)

def check_vinted():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(VINTED_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    listings = soup.find_all("a", href=True)

    new_items = []

    for link in listings:
        href = link["href"]
        if "/items/" in href:
            item_id = href.split("/")[-1]
            if item_id not in seen_items:
                seen_items.add(item_id)
                item_url = "https://www.vinted.fr" + href
                new_items.append(item_url)

    return new_items

if __name__ == "__main__":
    while True:
        print("[🔎] Vérification des annonces Vinted...")
        try:
            new_listings = check_vinted()
            for item in new_listings:
                send_telegram(f"🆕 Nouvelle annonce Vinted : {item}")
                print(f"[✅] Envoyé : {item}")
        except Exception as e:
            print(f"[❌] Erreur : {e}")

        time.sleep(60)
