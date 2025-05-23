import time
import requests

WEBHOOK_URL = "https://discordapp.com/api/webhooks/1375552352010109040/ASAptOz6NiXR6eWPLvjUl6Vsx-SgGRJyIjx3KeRuUOtZiknHvokvP73e0nWGm1hyTvIP"
API_URL = "https://www.vinted.fr/api/v2/catalog/items?search_text=steelbook+4k&catalog[]=3042&order=newest_first"

sent_ids = set()

def send_discord_message(title, url, price):
    data = {
        "embeds": [{
            "title": title,
            "url": url,
            "description": f"💰 Prix : {price}",
            "color": 5814783
        }]
    }
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("✅ Notification envoyée")
    else:
        print("❌ Erreur Discord :", response.text)

def scrape_vinted():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(API_URL, headers=headers)
        data = response.json()

        items = data["items"]
        for item in items:
            item_id = item["id"]
            if item_id not in sent_ids:
                title = item["title"]
                url = "https://www.vinted.fr" + item["url"]
                price = item["price"] + " €"
                send_discord_message(title, url, price)
                sent_ids.add(item_id)

    except Exception as e:
        print("❌ Erreur :", e)

while True:
    print("🔄 Scraping Vinted...")
    scrape_vinted()
    time.sleep(60)

