import requests
import time
import json
from bs4 import BeautifulSoup
from telegram import Bot

# Tes infos Telegram
TOKEN = "8182847473:AAFiNbnATsBMHWpxhDC4XMqAhElkeIkqkaw"
CHAT_ID = "-1002527933128"

bot = Bot(token=TOKEN)

# URLs à scraper
URLS = {
    "Vinted": "https://www.vinted.fr/catalog?search_text=Steelbook%204k&time=1747650174&currency=EUR&order=newest_first&disabled_personalization=true&page=1",
    "LeBonCoin": "https://www.leboncoin.fr/recherche?text=steelbook+4k&sort=time&order=desc&kst=r&from=rs",
    "eBay": "https://www.ebay.fr/sch/i.html?_nkw=steelbook+4k&_sacat=0&_sop=10"
}

SEEN_FILE = "seen.json"

# Charger ou init la mémoire des annonces déjà vues
try:
    with open(SEEN_FILE, "r") as f:
        seen = json.load(f)
except FileNotFoundError:
    seen = {"Vinted": [], "LeBonCoin": [], "eBay": []}

def save_seen():
    with open(SEEN_FILE, "w") as f:
        json.dump(seen, f)

def send_telegram_message(text):
    try:
        bot.send_message(chat_id=CHAT_ID, text=text, parse_mode='HTML', disable_web_page_preview=True)
        print(f"Message envoyé : {text[:50]}...")
    except Exception as e:
        print(f"Erreur Telegram : {e}")

def parse_vinted(html):
    soup = BeautifulSoup(html, "html.parser")
    items = []
    # Chaque annonce est dans un <div data-testid="item-card">
    for div in soup.find_all("div", {"data-testid": "item-card"}):
        try:
            title = div.find("div", {"data-testid": "item-card-title"}).get_text(strip=True)
            price = div.find("div", {"data-testid": "item-card-price"}).get_text(strip=True)
            link_tag = div.find("a", href=True)
            link = "https://www.vinted.fr" + link_tag["href"]
            item_id = link.split("-")[-1]  # ID extrait de l'URL
            items.append({"id": item_id, "title": title, "price": price, "link": link})
        except Exception:
            continue
    return items

def parse_leboncoin(html):
    soup = BeautifulSoup(html, "html.parser")
    items = []
    # Chaque annonce est dans un <li> avec attribute data-testid="aditem"
    for li in soup.find_all("li", {"data-testid": "aditem"}):
        try:
            title = li.find("p", {"data-testid": "aditem_title"}).get_text(strip=True)
            price = li.find("p", {"data-testid": "aditem_price"}).get_text(strip=True)
            link_tag = li.find("a", href=True)
            link = "https://www.leboncoin.fr" + link_tag["href"]
            item_id = link.split("/")[-1].split("?")[0]  # ID extrait de l'URL
            items.append({"id": item_id, "title": title, "price": price, "link": link})
        except Exception:
            continue
    return items

def parse_ebay(html):
    soup = BeautifulSoup(html, "html.parser")
    items = []
    # Chaque annonce dans <li class="s-item">
    for li in soup.find_all("li", {"class": "s-item"}):
        try:
            title_tag = li.find("h3", {"class": "s-item__title"})
            price_tag = li.find("span", {"class": "s-item__price"})
            link_tag = li.find("a", href=True)
            if not title_tag or not price_tag or not link_tag:
                continue
            title = title_tag.get_text(strip=True)
            price = price_tag.get_text(strip=True)
            link = link_tag["href"]
            # ID eBay = dernier morceau d'URL après slash ou le param 'itm='
            if "itm=" in link:
                item_id = link.split("itm=")[-1].split("&")[0]
            else:
                item_id = link.split("/")[-1].split("?")[0]
            items.append({"id": item_id, "title": title, "price": price, "link": link})
        except Exception:
            continue
    return items

def fetch_and_parse(name, url):
    print(f"Vérification {name}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ScalperBot/1.0; +https://github.com/)"
    }
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        if name == "Vinted":
            return parse_vinted(r.text)
        elif name == "LeBonCoin":
            return parse_leboncoin(r.text)
        elif name == "eBay":
            return parse_ebay(r.text)
    except Exception as e:
        print(f"Erreur lors de la récupération {name} : {e}")
    return []

def main():
    while True:
        new_annonces = 0
        for site, url in URLS.items():
            annonces = fetch_and_parse(site, url)
            for ann in annonces:
                if ann["id"] not in seen[site]:
                    seen[site].append(ann["id"])
                    msg = f"<b>{site}</b>\n{ann['title']}\nPrix: {ann['price']}\n{ann['link']}"
                    send_telegram_message(msg)
                    new_annonces += 1
            # Nettoyage mémoire : garder max 500 ids pour limiter taille fichier
            if len(seen[site]) > 500:
                seen[site] = seen[site][-500:]
        if new_annonces == 0:
            print("Pas de nouvelle annonce détectée.")
        save_seen()
        time.sleep(60)

if __name__ == "__main__":
    main()

