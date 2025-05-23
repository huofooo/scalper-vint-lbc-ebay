import time
import requests
import json

WEBHOOK_URL = "https://discordapp.com/api/webhooks/1375552352010109040/ASAptOz6NiXR6eWPLvjUl6Vsx-SgGRJyIjx3KeRuUOtZiknHvokvP73e0nWGm1hyTvIP"
URL_VINTED = "https://www.vinted.fr/catalog?search_text=steelbook%204k&time=1748027744&order=newest_first&page=1"

sent_ids = set()

def send_discord_message(title, url, price):
    data = {
        "embeds": [{
            "title": title,
            "url": url,
            "description": f"Prix : {price}",
            "color": 5814783
        }]
    }
    response = requests.post(WEBHOOK_URL, json=data)
    print("Notification envoyée sur Discord" if response.status_code == 204 else "Erreur envoi Discord")

def scrape_vinted():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(URL_VINTED, headers=headers)
        if response.status_code != 200:
            print("Erreur HTTP, statut :", response.status_code)
            return

        html = response.text
        items = html.split('"items":')[1].split(',"total_items')[0]
        items = json.loads(items)

        for item in items:
            item_id = item['id']
            if item_id not in sent_ids:
                title = item['title']
                url = "https://www.vinted.fr" + item['url']
                price = item['price']["amount"] + " €"
                send_discord_message(title, url, price)
                sent_ids.add(item_id)

    except Exception as e:
        print("Erreur :", e)

while True:
    print("Scraping Vinted...")
    scrape_vinted()
    time.sleep(60)
