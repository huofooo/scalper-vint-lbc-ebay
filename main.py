import requests
from bs4 import BeautifulSoup
import time
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "disable_web_page_preview": True
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Erreur envoi Telegram:", e)

def scrape_vinted():
    url = "https://www.vinted.fr/catalog?search_text=Steelbook%204k&time=1747614181&currency=EUR&order=newest_first&disabled_personalization=true&page=1"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select("div.feed-grid__item")
        for item in items[:1]:
            title = item.get_text(strip=True)
            link = "https://www.vinted.fr" + item.find("a")["href"]
            send_telegram_message(f"🟣 Vinted : {title}
{link}")
    except Exception as e:
        print("Erreur Vinted:", e)

def scrape_ebay():
    url = "https://www.ebay.fr/sch/i.html?_nkw=steelbook+4k&_sacat=0&_sop=10"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select("li.s-item")
        for item in items[:1]:
            title = item.get_text(strip=True)
            link = item.find("a")["href"]
            send_telegram_message(f"🟡 eBay : {title}
{link}")
    except Exception as e:
        print("Erreur eBay:", e)

def scrape_leboncoin():
    url = "https://www.leboncoin.fr/recherche?text=steelbook%204k&sort=time&order=desc"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select("a[data-qa-id='aditem_container']")
        for item in items[:1]:
            title = item.get_text(strip=True)
            link = "https://www.leboncoin.fr" + item["href"]
            send_telegram_message(f"🟠 Leboncoin : {title}
{link}")
    except Exception as e:
        print("Erreur Leboncoin:", e)

def check_sites_and_notify():
    scrape_vinted()
    scrape_ebay()
    scrape_leboncoin()

if __name__ == "__main__":
    while True:
        check_sites_and_notify()
        time.sleep(120)
