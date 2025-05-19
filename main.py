import time
import requests
from bs4 import BeautifulSoup

# Tes infos Telegram
TOKEN = "8182847473:AAFiNbnATsBMHWpxhDC4XMqAhElkeIkqkaw"
CHAT_ID = "-1002527933128"

# URLs à scraper
URLS = {
    "Vinted": "https://www.vinted.fr/catalog?search_text=Steelbook%204k&time=1747614181&currency=EUR&order=newest_first&disabled_personalization=true&page=1",
    "Leboncoin": "https://www.leboncoin.fr/recherche?text=steelbook%204k&sort=time&order=desc",
    "eBay": "https://www.ebay.fr/sch/i.html?_nkw=steelbook+4k&_sacat=0&_sop=10"
}

# Stockage des annonces déjà vues pour éviter les doublons
seen_annonces = set()

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text, "disable_web_page_preview": True}
    try:
        resp = requests.post(url, data=data)
        if resp.status_code == 200:
            print("Message Telegram envoyé.")
        else:
            print(f"Erreur Telegram: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"Erreur envoi Telegram: {e}")

def scrape_vinted():
    print("Scraping Vinted...")
    annonces = []
    try:
        resp = requests.get(URLS["Vinted"], headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.select("div.feed-grid__item")  # sélecteur approximatif, à ajuster

        for item in items:
            title_tag = item.select_one("div.feed-grid__item-info-title")
            price_tag = item.select_one("div.feed-grid__item-info-price")
            link_tag = item.select_one("a")

            if title_tag and price_tag and link_tag:
                title = title_tag.get_text(strip=True)
                price = price_tag.get_text(strip=True)
                link = "https://www.vinted.fr" + link_tag.get("href")

                key = f"Vinted-{link}"
                if key not in seen_annonces:
                    annonces.append((title, price, link))
                    seen_annonces.add(key)
    except Exception as e:
        print(f"Erreur scraping Vinted: {e}")

    return annonces

def scrape_leboncoin():
    print("Scraping Leboncoin...")
    annonces = []
    try:
        resp = requests.get(URLS["Leboncoin"], headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.select("li._1fmiA")  # sélecteur approximatif, à ajuster

        for item in items:
            title_tag = item.select_one("h3._2tubl")
            price_tag = item.select_one("h4._1F5u3")
            link_tag = item.select_one("a")

            if title_tag and price_tag and link_tag:
                title = title_tag.get_text(strip=True)
                price = price_tag.get_text(strip=True)
                link = "https://www.leboncoin.fr" + link_tag.get("href")

                key = f"Leboncoin-{link}"
                if key not in seen_annonces:
                    annonces.append((title, price, link))
                    seen_annonces.add(key)
    except Exception as e:
        print(f"Erreur scraping Leboncoin: {e}")

    return annonces

def scrape_ebay():
    print("Scraping eBay...")
    annonces = []
    try:
        resp = requests.get(URLS["eBay"], headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.select("li.s-item")  # sélecteur approximatif, à ajuster

        for item in items:
            title_tag = item.select_one("h3.s-item__title")
            price_tag = item.select_one("span.s-item__price")
            link_tag = item.select_one("a.s-item__link")

            if title_tag and price_tag and link_tag:
                title = title_tag.get_text(strip=True)
                price = price_tag.get_text(strip=True)
                link = link_tag.get("href")

                key = f"eBay-{link}"
                if key not in seen_annonces:
                    annonces.append((title, price, link))
                    seen_annonces.add(key)
    except Exception as e:
        print(f"Erreur scraping eBay: {e}")

    return annonces

print("=== SCALPER MULTI-SITES DÉMARRÉ ===")

while True:
    all_annonces = []

    all_annonces += scrape_vinted()
    all_annonces += scrape_leboncoin()
    all_annonces += scrape_ebay()

    print(f"{len(all_annonces)} nouvelles annonces détectées.")

    for title, price, link in all_annonces:
        message = f"{title}\nPrix: {price}\n{link}"
        send_telegram_message(message)

    print("Attente 60 secondes...\n")
    time.sleep(60)
