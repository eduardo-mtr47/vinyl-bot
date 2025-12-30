import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Charge le .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
DISCORD_USER_ID = os.getenv("DISCORD_USER_ID")  # ← À ajouter dans ton .env

if not DISCORD_WEBHOOK_URL:
    raise ValueError("⚠️ DISCORD_WEBHOOK_URL n'est pas défini.")

def send_discord_message(offer):
    try:
        mention = f"<@{DISCORD_USER_ID}>" if DISCORD_USER_ID else ""
        release_id = offer.get("release_id", "")
        link = f"https://www.discogs.com/sell/release/{release_id}" if release_id else "https://www.discogs.com/"

        content = (
            f"{mention}\n"
            f"**{offer['title']}**\n"
            f"💰 {offer['price']} {offer['currency']} (~{offer['price_eur']} €)\n"
            f"🏷️ {offer['condition']}\n"
            f"🛒 {offer['seller']}\n"
            f"🔗 {link}"
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
