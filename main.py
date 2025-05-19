import requests
from bs4 import BeautifulSoup
import time

TOKEN = "8182847473:AAFiNbnATsBMHWpxhDC4XMqAhElkeIkqkaw"
CHAT_ID = "-1002527933128"
HEADERS = {"User-Agent": "Mozilla/5.0"}
seen_links = set()

def send_telegram(message):
    url = f"https://api.telegram.org/bot{8182847473:AAFiNbnATsBMHWpxhDC4XMqAhElkeIkqkaw}/sendMessage"
    data = {"-1002527933128": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Erreur Telegram: {e}")

def check_vinted():
    url = "https://www.vinted.fr/catalog?search_text=Steelbook%204k&time=1747614181&currency=EUR&order=newest_first&disabled_personalization=true&page=1"
    soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/items/" in href and href not in seen_links:
            seen_links.add(href)
            send_telegram(f"🧥 Vinted : https://www.vinted.fr{href}")

def check_ebay():
    url = "https://www.ebay.fr/sch/i.html?_nkw=steelbook+4k&_sacat=0&_sop=10"
    soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "itm/" in href and href not in seen_links:
            seen_links.add(href)
            send_telegram(f"🛒 eBay : {href}")

def check_leboncoin():
    url = "https://www.leboncoin.fr/recherche?text=steelbook%204k&sort=time&order=desc"
    soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/offre/" in href and href not in seen_links:
            seen_links.add(href)
            send_telegram(f"📦 LeBonCoin : https://www.leboncoin.fr{href}")

print("🚀 Le bot démarre...")
while True:
    print("🔍 Vérification des nouvelles annonces...")
    check_vinted()
    check_ebay()
    check_leboncoin()
    print("⏳ Pause de 2 minutes...")
    time.sleep(120)
