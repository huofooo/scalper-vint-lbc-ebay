import requests
import time
import hashlib

# === PARAMÈTRES ===
VINTED_API_URL = "https://www.vinted.fr/api/v2/catalog/items?catalog[]=3042&order=newest_first"
TELEGRAM_TOKEN = "8182847473:AAFiNbnATsBMHWpxhDC4XMqAhElkeIkqkaw"
TELEGRAM_CHAT_ID = "-1002527933128"
INTERVAL = 60  # secondes

# === POUR MÉMORISER LES ANNONCES DÉJÀ ENVOYÉES ===
annonces_vues = set()

def envoyer_message(texte):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": texte,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

def hash_annonce(title, url):
    return hashlib.md5(f"{title}-{url}".encode()).hexdigest()

def verifier_vinted():
    print("🔍 Vérification Vinted en cours...")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(VINTED_API_URL, headers=headers)
        data = response.json()

        articles = data.get("items", [])
        nouveaux = 0

        for article in articles:
            title = article["title"]
            url = f"https://www.vinted.fr{article['url']}"
            prix = article["price"]
            identifiant = hash_annonce(title, url)

            if identifiant not in annonces_vues:
                annonces_vues.add(identifiant)
                texte = f"🆕 <b>{title}</b>\n💶 Prix : {prix} €\n🔗 {url}"
                envoyer_message(texte)
                print("✅ Annonce envoyée :", title)
                nouveaux += 1

        if nouveaux == 0:
            print("ℹ️ Aucune nouvelle annonce détectée.")
    except Exception as e:
        print("❌ Erreur pendant la récupération :", e)

# === BOUCLE INFINIE ===
while True:
    verifier_vinted()
    time.sleep(INTERVAL)

