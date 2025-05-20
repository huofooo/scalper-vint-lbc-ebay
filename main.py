import requests
import time

# === CONFIGURATION ===
TOKEN = "8182847473:AAFiNbnATsBMHWpxhDC4XMqAhElkeIkqkaw"
CHAT_ID = "-1002527933128"
VINTED_API_URL = "https://www.vinted.fr/api/v2/catalog/items?search_text=steelbook%204k&catalog[]=3042&order=newest_first"

# === SUIVI DES ANNONCES ===
seen_ids = set()

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"[❌] Erreur Telegram : {response.text}")

def check_vinted():
    print("[🔎] Connexion à l’API Vinted...")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(VINTED_API_URL, headers=headers)
        data = response.json()
        items = data.get("items", [])

        print(f"[📦] {len(items)} annonces reçues.")
        new_items = []

        for item in items:
            item_id = item["id"]
            if item_id not in seen_ids:
                seen_ids.add(item_id)
                title = item["title"]
                price = item["price"] + " €"
                url = f"https://www.vinted.fr/items/{item_id}"
                message = f"🆕 <b>{title}</b>\n💰 {price}\n🔗 {url}"
                new_items.append(message)

        return new_items

    except Exception as e:
        print(f"[❌] Erreur pendant la récupération : {e}")
        return []

# === BOUCLE PRINCIPALE ===
if __name__ == "__main__":
    while True:
        print("\n[⏰] Vérification en cours...")
        results = check_vinted()
        if results:
            for msg in results:
                send_telegram(msg)
                print(f"[✅] Notification envoyée : {msg}")
        else:
            print("[ℹ️] Aucune nouvelle annonce détectée.")
        time.sleep(60)

