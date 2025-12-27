import json
import requests
from scraper import get_offers_for_release
from notifier import send_discord_message

EXCHANGE_API = "https://api.frankfurter.app/latest"

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

def main():
    with open("wishlist.json", "r") as f:
        wishlist = json.load(f)

    for item in wishlist:
        release_id = item["release_id"]
        max_price = item["max_price"]
        title = item.get("title", f"Release {release_id}")

        print(f"\n🎵 {title}")
        print(f"🔍 Recherche d’offres pour release ID {release_id} (max {max_price} €)...")

        offers = get_offers_for_release(release_id)
        valid = []

        for offer in offers:
            price = offer["price"]
            currency = offer["currency"]
            price_eur = convert_to_eur(price, currency)

            if price_eur is None:
                continue

            if price_eur <= max_price:
                offer["price_eur"] = price_eur
                valid.append(offer)

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

            # Envoi Discord
            msg = f"""📀 **{title}** — Offre #{idx}
            💰 `{offer['price']} {offer['currency']}` → **{offer['price_eur']} €**
            🏷️ {offer['condition'].strip()}
            🛒 {offer['seller'].strip()}
            🔗 {offer['url']}
            """
            send_discord_message(msg)

if __name__ == "__main__":
    main()
