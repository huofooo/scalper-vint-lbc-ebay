import time
import requests

# Tes variables Telegram à remplacer par les tiennes
TOKEN = "8182847473:AAFiNbnATsBMHWpxhDC4XMqAhElkeIkqkaw"
CHAT_ID = "-1002527933128"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    try:
        resp = requests.post(url, data=data)
        if resp.status_code == 200:
            print("Message envoyé sur Telegram.")
        else:
            print(f"Erreur Telegram: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"Exception lors de l'envoi Telegram: {e}")

def fetch_vinted_annonces():
    # Exemple simplifié : récupérer et analyser Vinted (à adapter)
    print("Simulation récupération annonces Vinted...")
    # Ici tu fais ta vraie requête et parse
    annonces = ["Steelbook 4k - 25€", "Steelbook 4k - 30€"]  # simulation
    return annonces

print("=== BOT DÉMARRÉ ===")

while True:
    print("Vérification des nouvelles annonces...")
    annonces = fetch_vinted_annonces()
    print(f"{len(annonces)} annonces trouvées.")

    for annonce in annonces:
        print(f"Annonce trouvée: {annonce}")
        send_telegram_message(f"Nouvelle annonce Vinted : {annonce}")

    print("Attente 2 minutes avant prochaine vérification...\n")
    time.sleep(120)
