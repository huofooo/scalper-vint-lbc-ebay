import requests
from bs4 import BeautifulSoup
import time
import hashlib

# === CONFIGURATION ===
TELEGRAM_TOKEN = "8182847473:AAFiNbnATsBMHWpxhDC4XMqAhElkeIkqkaw"
TELEGRAM_CHAT_ID = "-1002527933128"
CHECK_INTERVAL = 60  # secondes
URL_VINTED = "https://www.vinted.fr/catalog?catalog[]=3042&order=newest_first"

annonces_envoyees = set()

def envoyer_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload)
        print("📨 Notification envoyée.")
    except Exception as e:
        print("❌ Erreur envoi Telegram:", e)

def get_annonces_vinted():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        print("🌐 Récupération HTML de la page Vinted...")
        r = requests.get(URL_VINTED, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        articles = soup.select("a.tile")  # chaque annonce
        resultats = []

        for article in articles:
            titre = article.select_one("h3").text.strip() if article.select_one("h3") else "Sans titre"
            lien = "https://www.vinted.fr" + article.get("href")
            prix = article.select_one("div[class*='price']").text.strip() if article.select_one("div[class*='price']") else "Prix inconnu"

            identifiant = hashlib.md5((titre + lien).encode()).hexdigest()

            resultats.append({
                "id": identifiant,
                "titre": titre,
                "prix": prix,
                "lien": lien
            })

        return resultats

    except Exception as e:
        print("❌ Erreur pendant le scraping :", e)
        return []

def verifier_et_notifier():
    annonces = get_annonces_vinted()
    if not annonces:
        print("ℹ️ Aucune annonce récupérée.")
        return

    print(f"📦 {len(annonces)} annonces récupérées.")

    for annonce in annonces:
        if annonce["id"] not in annonces_envoyees:
            annonces_envoyees.add(annonce["id"])
            message = f"🆕 <b>{annonce['titre']}</b>\n💶 {annonce['prix']}\n🔗 {annonce['lien']}"
            envoyer_message(message)
        else:
            print("🔁 Annonce déjà envoyée :", annonce["titre"])

# === LANCEMENT ===
while True:
    print("🔁 Vérification en cours...")
    verifier_et_notifier()
    time.sleep(CHECK_INTERVAL)
