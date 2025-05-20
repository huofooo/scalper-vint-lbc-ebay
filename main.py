import requests
import time

# Paramètres Telegram
TOKEN = "8182847473:AAFiNbnATsBMHWpxhDC4XMqAhElkeIkqkaw"
CHAT_ID = "-1002527933128"
MESSAGE = "🔔 Message automatique envoyé toutes les 20 secondes."

# Fonction pour envoyer le message
def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("[✅] Message envoyé sur Telegram.")
    else:
        print(f"[❌] Erreur d'envoi : {response.text}")

# Boucle infinie avec intervalle de 20 secondes
if __name__ == "__main__":
    while True:
        send_telegram_message(TOKEN, CHAT_ID, MESSAGE)
        time.sleep(240)
