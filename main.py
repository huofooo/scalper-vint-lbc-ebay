import requests
import time
import hashlib

# === CONFIGURATION ===
TELEGRAM_TOKEN = "8182847473:AAFiNbnATsBMHWpxhDC4XMqAhElkeIkqkaw"
TELEGRAM_CHAT_ID = "-1002527933128"
CHECK_INTERVAL = 60  # en secondes

# === URL VINTED testée (catégorie Blu-ray 4K) ===
VINTED_API_URL = "https://www.vinted.fr/api/v2/catalog/items?catalog[]=3042&order=newest_first"

# === POUR MÉMORISER LES ANNONCES ===
annonces_envoyees = set()

def envoyer_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload)
        print("📨 Notification envoyée.")
    except Exception as e:
        print("❌ Erreur envoi Telegram:", e)

def get_annonces_vinted():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        print("🌐 Requête envoyée à Vinted...")
        r = requests.get(VINTED_API_URL, headers=headers)
        print("🔢 Code HTTP :", r.status_code)

        if r.status_code != 200:
            print("❌ Erreur HTTP, contenu reçu :", r.text[:200])
            return []

        data = r.json()
        return data.get("items", [])

    except Exception as e:
        print("❌ Erreur pendant la récupération :", e)
        return []

def verifier_et_notifier():
    annonces = get_annonces_vinted()
    if not annonces:
        print("ℹ️ Aucune annonce récupérée.")
        return

    print(f"📦 {len(annonces)} annonces récupérées.")

    for article in annonces:
        title = article["title"]
        url = f"https://www.vinted.fr{article['url']}"
        price = article["price"]
        identifiant = hashlib.md5((title + url).encode()).hexdigest()

        if identifiant not in annonces_envoyees:
            annonces_envoyees.add(identifiant)
            message = f"🆕 <b>{title}</b>\n💶 Prix : {price} €\n🔗 {url}"
            envoyer_message(message)
        else:
            print("🔁 Annonce déjà envoyée :", title)

# === LANCEMENT BOUCLE ===
while True:
    print("🔁 Nouvelle vérification...")
    verifier_et_notifier()
    time.sleep(CHECK_INTERVAL)

