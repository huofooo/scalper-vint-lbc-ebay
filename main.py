import time
import requests
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
TELEGRAM_TOKEN = "8182847473:AAFiNbnATsBMHWpxhDC4XMqAhElkeIkqkaw"
TELEGRAM_CHAT_ID = "-1002527933128"

VINTED_URL = "https://www.vinted.fr/catalog?search_text=Steelbook%204k&time=1747614181&currency=EUR&order=newest_first&disabled_personalization=true&page=1"
EBAY_URL = "https://www.ebay.fr/sch/i.html?_nkw=steelbook+4k&_sacat=0&_sop=10"
LEBONCOIN_URL = "https://www.leboncoin.fr/recherche?text=steelbook%204k&sort=time&order=desc"

# Pour éviter les doublons
seen_links = set()

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "disable_web_page_preview": False
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"❌ Erreur Telegram : {response.text}")
    else:
        print("✅ Message Telegram envoyé.")

def check_vinted():
    print("🔍 Vérification de Vinted...")
    response = requests.get(VINTED_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all("a", href=True)
    for a in links:
        href = a['href']
        if "/items/" in href:
            full_url = f"https://www.vinted.fr{href.split('?')[0]}"
            if full_url not in seen_links:
                seen_links.add(full_url)
                send_telegram_message(f"🧥 Nouvelle annonce Vinted :\n{full_url}")
                break

def check_ebay():
    print("🔍 Vérification de eBay...")
    response = requests.get(EBAY_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.select("li.s-item a.s-item__link")
    for item in items:
        href = item['href']
        if href not in seen_links:
            seen_links.add(href)
            send_telegram_message(f"📦 Nouvelle annonce eBay :\n{href}")
            break

def check_leboncoin():
    print("🔍 Vérification de Leboncoin...")
    response = requests.get(LEBONCOIN_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all("a", href=True)
    for link in links:
        href = link['href']
        if "/offre/" in href or "/annonce/" in href:
            full_url = f"https://www.leboncoin.fr{href}"
            if full_url not in seen_links:
                seen_links.add(full_url)
                send_telegram_message(f"📍 Nouvelle annonce Leboncoin :\n{full_url}")
                break

# --- BOUCLE PRINCIPALE ---
print("🚀 Le bot a bien démarré sur Render.")
while True:
    try:
        check_vinted()
        check_ebay()
        check_leboncoin()
        print("⏳ Attente de 2 minutes...\n")
        time.sleep(120)
    except Exception as e:
        print(f"⚠️ Erreur : {e}")
        time.sleep(60)
