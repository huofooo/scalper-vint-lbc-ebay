import requests
import time
import hashlib

# === PARAMÈTRES ===
VINTED_URL = "https://www.vinted.fr/catalog?catalog[]=3042&order=newest_first&disabled_personalization=true&page=1"
TELEGRAM_TOKEN = "8182847473:AAFiNbnATsBMHWpxhDC4XMqAhElkeIkqkaw"
TELEGRAM_CHAT_ID = "-1002527933128"
INTERVAL = 60  # secondes

# === STOCKER LES ANNONCES DÉJÀ VUES ===
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
    print("🔍 Vérification des annonces Vinted...")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(VINTED_URL, headers=headers)
        if response.status_code != 200:
            print("❌ Erreur de requête :", response.status_code)
            return

        html = response.text
        articles = html.split('data-testid="item-box"')[1:]
        nouveaux = 0

        for article in articles:
            try:
                title_start = article.index('title="') + 7
                title_end = article.index('"', title_start)
                title = article[title_start:title_end]

                url_start = article.index('href="') + 6
                url_end = article.index('"', url_start)
                relative_url = article[url_start:url_end]
                full_url = f"https://www.vinted.fr{relative_url}"

                identifiant = hash_annonce(title, full_url)
                if identifiant not in annonces_vues:
                    annonces_vues.add(identifiant)
                    texte = f"🆕 <b>{title}</b>\n🔗 {full_url}"
                    envoyer_message(texte)
                    print("✅ Nouvelle annonce envoyée :", title)
                    nouveaux += 1
            except Exception as e:
                print("⚠️ Erreur dans une annonce :", e)

        if nouveaux == 0:
            print("ℹ️ Aucune nouvelle annonce détectée.")
    except Exception as e:
        print("❌ Erreur pendant la récupération :", e)

# === BOUCLE PRINCIPALE ===
while True:
    verifier_vinted()
    time.sleep(INTERVAL)
