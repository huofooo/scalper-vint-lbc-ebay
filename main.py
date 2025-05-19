import requests
from bs4 import BeautifulSoup
import time
import telegram

# --- Tes liens de recherche ---
urls = {
    "vinted": "https://www.vinted.fr/catalog?search_text=Steelbook%204k&time=1747614181&currency=EUR&order=newest_first&disabled_personalization=true&page=1",
    "leboncoin": "https://www.leboncoin.fr/recherche?text=steelbook%204k&sort=time&order=desc",
    "ebay": "https://www.ebay.fr/sch/i.html?_nkw=steelbook+4k&_sacat=0&_sop=10"
}

# --- Ton token Telegram et chat_id ---
TELEGRAM_TOKEN = "8182847473:AAFiNbnATsBMHWpxhDC4XMqAhElkeIkqkaw"
CHAT_ID = "-1002527933128"

bot = telegram.Bot(token=TELEGRAM_TOKEN)

# --- Mémoire des annonces déjà envoyées ---
seen = set()

def send_telegram_message(text):
    try:
        bot.send_message(chat_id=CHAT_ID, text=text, parse_mode='HTML')
        print("Message envoyé :", text)
    except Exception as e:
        print("Erreur envoi Telegram :", e)

def extract_vinted(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    # Ici on cherche les annonces par leur titre, lien et prix
    items = soup.find_all('div', {'class': 'feed-grid__item'})  # À vérifier selon la page
    for item in items:
        title_tag = item.find('h3')
        price_tag = item.find('div', {'class': 'feed-price'})
        link_tag = item.find('a', href=True)
        if title_tag and price_tag and link_tag:
            title = title_tag.get_text(strip=True)
            price = price_tag.get_text(strip=True)
            link = "https://www.vinted.fr" + link_tag['href']
            results.append({'title': title, 'price': price, 'link': link})
    return results

def extract_leboncoin(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    ads = soup.find_all('li', {'data-qa-id': 'aditem_container'})
    for ad in ads:
        title_tag = ad.find('p', {'data-qa-id': 'aditem_title'})
        price_tag = ad.find('span', {'data-qa-id': 'aditem_price'})
        link_tag = ad.find('a', href=True)
        if title_tag and price_tag and link_tag:
            title = title_tag.get_text(strip=True)
            price = price_tag.get_text(strip=True)
            link = "https://www.leboncoin.fr" + link_tag['href']
            results.append({'title': title, 'price': price, 'link': link})
    return results

def extract_ebay(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    items = soup.find_all('li', {'class': 's-item'})
    for item in items:
        title_tag = item.find('h3', {'class': 's-item__title'})
        price_tag = item.find('span', {'class': 's-item__price'})
        link_tag = item.find('a', href=True)
        if title_tag and price_tag and link_tag:
            title = title_tag.get_text(strip=True)
            price = price_tag.get_text(strip=True)
            link = link_tag['href']
            results.append({'title': title, 'price': price, 'link': link})
    return results

def check_site(name, url, extractor):
    print(f"\n--- Vérification de {name} ---")
    try:
        response = requests.get(url)
        print("Extrait HTML :")
        print(response.text[:500])  # On affiche les 500 premiers caractères
        annonces = extractor(response.text)
        print(f"{len(annonces)} annonces trouvées")
        new_count = 0
        for annonce in annonces:
            unique_id = annonce['link']
            if unique_id not in seen:
                message = f"<b>{name.capitalize()}</b>\n{annonce['title']}\nPrix : {annonce['price']}\nLien : {annonce['link']}"
                send_telegram_message(message)
                seen.add(unique_id)
                new_count += 1
        print(f"{new_count} nouvelles annonces envoyées sur Telegram")
    except Exception as e:
        print(f"Erreur sur {name} :", e)

def main():
    while True:
        check_site("vinted", urls["vinted"], extract_vinted)
        check_site("leboncoin", urls["leboncoin"], extract_leboncoin)
        check_site("ebay", urls["ebay"], extract_ebay)
        print("\nPause 60 secondes...")
        time.sleep(60)

if __name__ == "__main__":
    main()
