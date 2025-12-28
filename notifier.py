import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Charge le fichier .env depuis le même dossier que ce script
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

if not DISCORD_WEBHOOK_URL:
    raise ValueError("⚠️ DISCORD_WEBHOOK_URL n'est pas défini dans les variables d'environnement.")

def send_discord_message(offer):
    try:
        content = (
            f"**{offer['title']}**\n"
            f"💰 {offer['price']} {offer['currency']} (~{offer['price_eur']} €)\n"
            f"🏷️ {offer['condition']}\n"
            f"🛒 {offer['seller']}\n"
            f"🔗 {offer['url'] or 'https://www.discogs.com'}"
        )

        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json={"content": content},
            timeout=10
        )
        response.raise_for_status()
        return True

    except Exception as e:
        print(f"⚠️ Erreur Discord : {response.status_code if 'response' in locals() else '?'} - {e}")
        return False
