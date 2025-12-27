import requests
import os

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1454440464995582047/5XyhNReXfWt6SrK3G6NkTTtlRf9KB1qJUWCDU2HIrbeoU03CijC_BfWiluBygZTL4g2A"


# Change ceci par ton propre webhook

def send_discord_message(offer):
    try:
        title = offer.get("title", "Offre vinyle")
        price = offer.get("price")
        price_eur = offer.get("price_eur")
        currency = offer.get("currency")
        condition = offer.get("condition", "")
        seller = offer.get("seller", "")
        url = offer.get("url") or "https://www.discogs.com"

        message = (
            f"📢 **{title}**\n"
            f"💰 Prix brut : {price} {currency}\n"
            f"💱 Converti (EUR) : {price_eur} €\n"
            f"🏷️ Condition : {condition}\n"
            f"🛒 Vendeur : {seller}\n"
            f"🔗 [Voir l'offre]({url})"
        )

        payload = {"content": message}

        r = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)

        if r.status_code >= 400:
            print(f"⚠️ Erreur Discord : {r.status_code} - {r.text}")

    except Exception as e:
        print(f"❌ Exception lors de l’envoi Discord : {e}")
