import json
import os
import requests
from scraper import get_offers_for_release
from notifier import send_discord_message
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent / ".env")

SEEN_FILE = "sent_offers.json"
EXCHANGE_API = "https://api.frankfurter.app/latest"

def load_seen_offers():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                print("⚠️ Erreur dans sent_offers.json. Fichier réinitialisé.")
                return set()
    return set()

def save_seen_offers(data):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(data), f)

def convert_to_eur(amount, currency):
    if amount is None or currency is None:
        return None

    currency_map = {
        "€": "EUR", "$": "USD", "£": "GBP",
        "DKK": "DKK", "AUD": "AUD", "CAD": "CAD",
        "USD": "USD", "GBP": "GBP"
    }

    base = currency_map.get(currency)
    if base is None:
        return None

    if base == "EUR":
        return round(amount, 2)

    try:
        url = f"{EXCHANGE_API}?from={base}&to=EUR"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        rate = r.json()["rates"]["EUR"]
        return round(amount * rate, 2)
    except Exception as e:
        print(f"⚠️ Conversion error for {amount} {currency}: {e}")
        return None

def check_prerequisites():
    print("\n✅ Vérification des prérequis...")

    if not os.path.exists("wishlist.json"):
        print("❌ wishlist.json manquant.")
        return False
    print("📄 wishlist.json trouvé.")

    webhook = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook:
        print("❌ DISCORD_WEBHOOK_URL manquant dans .env")
        return False

    try:
        resp = requests.head(webhook, timeout=5)
        if resp.status_code >= 400:
            print(f"❌ Webhook invalide (HTTP {resp.status_code})")
            return False
        print("🌐 Webhook Discord OK.")
    except Exception as e:
        print(f"❌ Erreur lors de la vérification du webhook : {e}")
        return False

    print("✅ Tous les prérequis sont OK.\n")
    return True

def main():
    if not check_prerequisites():
        print("❌ Arrêt du script.")
        return

    seen_offers = load_seen_offers()
    new_seen = False

    with open("wishlist.json", "r") as f:
        wishlist = json.load(f)

    for item in wishlist:
        release_id = item["release_id"]
        max_price = item["max_price"]
        title = item.get("title", f"Release {release_id}")

        print(f"\n🎵 {title}")
        print(f"🔍 Recherche d’offres pour release ID {release_id} (max {max_price} €)...")

        offers = get_offers_for_release(release_id)
        print(f"➡️ {len(offers)} offres récupérées")

        valid_offers = []

        for offer in offers:
            offer["title"] = title
            offer["release_id"] = release_id

            # ✅ Identifiant unique basé sur vendeur + prix + condition
            offer_id = f"{offer.get('seller')}_{offer.get('price')}_{offer.get('condition')}"
            if offer_id in seen_offers:
                print(f"⏩ Offre déjà envoyée : {offer_id}")
                continue

            price = offer["price"]
            currency = offer["currency"]
            price_eur = convert_to_eur(price, currency)
            offer["price_eur"] = price_eur

            print(f"\n🔍 Offre brute : {price} {currency} (→ {price_eur} €) | Max : {max_price} €")

            if price_eur is None:
                print("⛔ Ignorée (conversion impossible).")
                continue

            if price_eur <= max_price:
                print("✅ Offre acceptée !")
                valid_offers.append(offer)
                seen_offers.add(offer_id)
                new_seen = True
            else:
                print("⛔ Trop cher.")

        if not valid_offers:
            print(f"❌ Aucune offre ≤ {max_price} €.")
            continue

        print(f"✅ {len(valid_offers)} offre(s) trouvée(s) ≤ {max_price} € :\n")

        for idx, offer in enumerate(valid_offers, 1):
            print(f"📦 Offre #{idx}")
            print(f"💰 Prix brut       : {offer['price']} {offer['currency']}")
            print(f"💱 Converti (EUR)  : {offer['price_eur']} €")
            print(f"🏷️ Condition       : {offer['condition']}")
            print(f"🛒 Vendeur         : {offer['seller']}")
            print(f"🔗 Lien            : https://www.discogs.com/sell/release/{release_id}")
            print("———")

            send_discord_message(offer)

    if new_seen:
        save_seen_offers(seen_offers)

if __name__ == "__main__":
    main()
