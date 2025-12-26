import json
from scraper import get_offers_for_release

# Charger wishlist.json
with open("wishlist.json", "r") as f:
    wishlist = json.load(f)


def main():
    for item in wishlist:
        release_id = item["release_id"]
        max_price = item["max_price"]
        title = item.get("title", f"Release ID {release_id}")

        print(f"\n🎵 {title}")
        print(f"🔍 Recherche d’offres pour le release ID {release_id}...")

        offers = get_offers_for_release(release_id)

        if not offers:
            print("❌ Aucune offre trouvée.")
            continue

        # Filtrer les offres en dessous du max_price
        filtered = [o for o in offers if o["price"] is not None and o["price"] <= max_price]

        if not filtered:
            print(f"❌ Aucune offre sous {max_price} €.")
            continue

        print(f"✅ {len(filtered)} offre(s) trouvée(s) sous {max_price} € :\n")
        for idx, offer in enumerate(filtered, 1):
            print(f"📦 Offre #{idx}")
            print(f"💰 Prix      : {offer['price']} €")
            print(f"🏷️ Condition : {offer['condition'].strip()}")
            print(f"🛒 Vendeur   : {offer['seller'].strip()}")
            print("———")

if __name__ == "__main__":
    main()
