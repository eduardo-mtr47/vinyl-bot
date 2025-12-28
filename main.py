import os
import json
import requests
from scraper import get_offers_for_release
from notifier import send_discord_message, DISCORD_WEBHOOK_URL
from dotenv import load_dotenv

load_dotenv()

SEEN_FILE = "seen_offers.json"
EXCHANGE_API = "https://api.frankfurter.app/latest"

# Chargement des offres déjà vues
if os.path.exists(SEEN_FILE):
    with open(SEEN_FILE, "r") as f:
        seen_offers = set(json.load(f))
else:
    seen_offers = set()

def save_seen_offers():
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen_offers), f)


def convert_to_eur(amount, currency):
    if amount is None or currency is None:
        return None

    currency_map = {
        "€": "EUR",
        "$": "USD",
        "£": "GBP",
        "DKK": "DKK",
        "AUD": "AUD",
        "CAD": "CAD"
    }

    base = currency_map.get(currency)
    if base is None:
        return None

    if base == "EUR":
        return round(amount, 2)

    try:
        url = f"https://api.frankfurter.app/latest?from={base}&to=EUR"
        r = requests.get(url, timeout=5)
        data = r.json()
        rate = data["rates"]["EUR"]
        return round(amount * rate, 2)
    except Exception as e:
        print(f"⚠️ Conversion error for {amount} {currency}: {e}")
        return None


def sanity_check():
    print("✅ Vérification des prérequis...\n")

    # Vérification du fichier wishlist
    if not os.path.exists("wishlist.json"):
        print("❌ wishlist.json manquant.")
        return False
    else:
        print("📄 wishlist.json trouvé.")

    # Vérification webhook Discord
    if not DISCORD_WEBHOOK_URL:
        print("❌ DISCORD_WEBHOOK_URL manquant.")
        return False
    else:
        print("🌐 Webhook Discord OK.")

    print("✅ Tous les prérequis sont OK.\n")
    return True



def main():
    if not sanity_check():
        print("❌ Arrêt du script.")
        return

    with open("wishlist.json", "r") as f:
        wishlist = json.load(f)

    new_seen = False

    for item in wishlist:
        release_id = item["release_id"]
        max_price = item["max_price"]
        title = item.get("title", f"Release {release_id}")

        print(f"\n🎵 {title}")
        print(f"🔍 Recherche d’offres pour release ID {release_id} (max {max_price} €)...")

        offers = get_offers_for_release(release_id)
        valid = []

        for offer in offers:
            url = offer.get("url") or f"https://www.discogs.com/sell/release/{release_id}"

            if url in seen_offers:
                continue

            price = offer["price"]
            currency = offer["currency"]
            price_eur = convert_to_eur(price, currency)

            if price_eur is None or price_eur > max_price:
                continue

            offer["price_eur"] = price_eur
            offer["url"] = url
            offer["title"] = title

            valid.append(offer)
            seen_offers.add(url)
            new_seen = True

        if not valid:
            print(f"❌ Aucune offre ≤ {max_price} €.")
            continue

        print(f"✅ {len(valid)} offre(s) trouvée(s) ≤ {max_price} € :\n")

        for idx, offer in enumerate(valid, 1):
            print(f"📦 Offre #{idx}")
            print(f"💰 Prix brut       : {offer['price']} {offer['currency']}")
            print(f"💱 Converti (EUR)  : {offer['price_eur']} €")
            print(f"🏷️ Condition       : {offer['condition']}")
            print(f"🛒 Vendeur         : {offer['seller']}")
            print(f"🔗 Lien            : {offer['url']}")
            print("———")
            send_discord_message(offer)

    if new_seen:
        save_seen_offers()


if __name__ == "__main__":
    main()
