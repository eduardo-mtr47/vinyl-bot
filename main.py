import json
from scraper import get_offers_for_release

def main():
    # Charger wishlist.json
    with open("wishlist.json", "r") as f:
        wishlist = json.load(f)

    for item in wishlist:
        release_id = item["release_id"]
        max_price = item["max_price"]
        title = item.get("title", f"Release {release_id}")

        print(f"\n🎵 {title}")
        print(f"🔍 Recherche d’offres pour le release ID {release_id} (max {max_price} €)...")

        offers = get_offers_for_release(release_id)

        if not offers:
            print("❌ Aucune offre trouvée.")
            continue

        # Filtrer par prix
        valid_offers = [
            o for o in offers
            if o["price_eur"] is not None and o["price_eur"] <= max_price
        ]

        if not valid_offers:
            print(f"❌ Aucune offre sous {max_price} €.")
            continue

        print(f"✅ {len(valid_offers)} offre(s) trouvée(s) sous {max_price} € :\n")

        for idx, offer in enumerate(sorted(valid_offers, key=lambda x: x["price_eur"]), 1):
            print(f"📦 Offre #{idx}")
            print(f"💰 Prix      : {offer['price_eur']} €")
            print(f"🚚 Shipping  : {offer['shipping']}")
            print(f"🏷️ Condition : {offer['condition']}")
            print(f"🛒 Vendeur   : {offer['seller']}")
            print("———")

if __name__ == "__main__":
    main()
