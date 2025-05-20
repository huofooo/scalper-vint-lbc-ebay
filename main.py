import requests
from bs4 import BeautifulSoup
import time
import hashlib

# === Configuration ===
URL = "https://www.vinted.fr/catalog?search_text=steelbook%204k&search_id=23485255761&order=newest_first&time=1747726758&catalog[]=3042&disabled_personalization=true&page=1"
TELEGRAM_TOKEN = "8182847473:AAFiNbnATsBMHWpxhDC4XMqAhElkeIkqkaw"
TELEGRAM_CHAT_ID = "-1002527933128"

# === Pour éviter les doublons ===
annonces_envoyees = set()

def envoyer_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "disable_web_page_preview": False
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print("Erreur Telegram:", response.text)

def get_hash_annonce(titre, lien):
    return hashlib.md5(f"{titre}{lien}".encode()).hexdigest()

def verifier_vinted():
    print("🔍 Vérification des nouvelles annonces Vinted...")
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("div", class_="feed-grid__item")

        nouveaux_detectes = 0

        for article in articles:
            lien_tag = article.find("a", href=True)
            titre_tag = article.find("h3")
            prix_tag = article.find("span", class_="text-body-2")

            if lien_tag and titre_tag and prix_tag:
                lien = "https://www.vinted.fr" + lien_tag["href"]
                titre = titre_tag.text.strip()
                prix = prix_tag.text.strip()

                identifiant = get_hash_annonce(titre, lien)

                if identifiant not in annonces_envoyees:
                    message = f"🆕 Nouvelle annonce Vinted :\n\n{titre}\n💶 {prix}\n🔗 {lien}"
                    envoyer_telegram(message)
                    annonces_envoyees.add(identifiant)
                    nouveaux_detectes += 1

        if nouveaux_detectes == 0:
            print("✅ Aucune nouvelle annonce détectée.")
        else:
            print(f"✅ {nouveaux_detectes} nouvelle(s) annonce(s) envoyée(s).")

    except Exception as e:
        print("❌ Erreur durant le scraping Vinted :", str(e))

# === Boucle infinie ===
while True:
    verifier_vinted()
    time.sleep(60)
