import requests
from bs4 import BeautifulSoup
import time
import telegram

TELEGRAM_TOKEN = "8182847473:AAFiNbnATsBMHWpxhDC4XMqAhElkeIkqkaw"
TELEGRAM_CHAT_ID = "-1002527933128"

bot = telegram.Bot(token=TELEGRAM_TOKEN)

# URLs à surveiller
URLS = {
    "vinted": "https://www.vinted.fr/catalog?search_text=Steelbook%204k&time=1747614181&currency=EUR&order=newest_first&disabled_personalization=true&page=1",
    "ebay": "https://www.ebay.fr/sch/i.html?_nkw=steelbook+4k&_sacat=0&_sop=10",
    "leboncoin": "https://www.leboncoin.fr/recherche?text=steelbook%204k&sort=time&order=desc"
}

# Pour éviter les doublons
seen_ads = set()

def get_vinted_ads():
    response = requests.get(URLS["vinted"])
    soup = BeautifulSoup(response.text, 'html.parser')
    ads = []
    for item in soup.select('div.feed-grid__item a[href*="/items/"]'):
        title = item.get('title', 'Annonce Vinted')
        url = "https://www.vinted.fr" + item.get('href')
        ad_id = url.split("/")[-1]
        if ad_id not in seen_ads:
            seen_ads.add(ad_id)
            ads.append((title, url))
    return ads

def get_ebay_ads():
    response = requests.get(URLS["ebay"])
    soup = BeautifulSoup(response.text, 'html.parser')
    ads = []
    for item in soup.select('li.s-item'):
        link = item.find('a', href=True)
        title_tag = item.find('h3', class_='s-item__title')
        if link and title_tag:
            url = link['href']
            title = title_tag.get_text()
            ad_id = url.split("?")[0]
            if ad_id not in seen_ads:
                seen_ads.add(ad_id)
                ads.append((title, url))
    return ads

def get_leboncoin_ads():
    response = requests.get(URLS["leboncoin"])
    soup = BeautifulSoup(response.text, 'html.parser')
    ads = []
    for item in soup.select('a[href^="/offre/"]'):
        url = "https://www.leboncoin.fr" + item['href']
        title = item.get_text().strip() or "Annonce LeBonCoin"
        ad_id = url.split("/")[-1]
        if ad_id not in seen_ads:
            seen_ads.add(ad_id)
            ads.append((title, url))
    return ads

def send_to_telegram(title, url):
    message = f"🆕 {title}\n🔗 {url}"
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

while True:
    print("Vérification Vinted...")
    for title, url in get_vinted_ads():
        print(f"Nouvelle annonce Vinted : {title}")
        send_to_telegram(title, url)

    print("Vérification eBay...")
    for title, url in get_ebay_ads():
        print(f"Nouvelle annonce eBay : {title}")
        send_to_telegram(title, url)

    print("Vérification LeBonCoin...")
    for title, url in get_leboncoin_ads():
        print(f"Nouvelle annonce LeBonCoin : {title}")
        send_to_telegram(title, url)

    print("Attente 60 secondes...\n")
    time.sleep(60)

