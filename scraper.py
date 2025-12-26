import cloudscraper
from bs4 import BeautifulSoup

def get_offers_for_release(release_id):
    url = f"https://www.discogs.com/sell/release/{release_id}"

    print(f"\n🌐 Requête vers {url}")
    
    scraper = cloudscraper.create_scraper(
        browser={
            'custom': 'ScraperBot/1.0'
        }
    )

    try:
        response = scraper.get(url)
        print(f"🔁 Statut HTTP : {response.status_code}")

        if response.status_code == 403:
            print("⛔️ Accès toujours interdit (403), même avec cloudscraper.")
            return []

        if response.status_code != 200:
            print(f"❌ Échec de la requête : code {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        listings = soup.select(".shortcut_navigable")

        print(f"🔍 {len(listings)} offres trouvées dans le HTML.")

        offers = []

        for idx, item in enumerate(listings, 1):
            price_tag = item.select_one(".price")
            condition_tag = item.select_one(".item_condition")
            seller_tag = item.select_one(".seller_info")

            price = None
            import re  # à mettre en haut du fichier s'il n'y est pas déjà

            price = None
            if price_tag:
                price_text = price_tag.text.strip()
                # Supprimer toutes les lettres et symboles sauf chiffres et ponctuation
                price_clean = re.sub(r'[^\d.,]', '', price_text).replace(',', '.')
                try:
                    price = float(price_clean)
                except ValueError:
                    print(f"⚠️ Erreur parsing prix : {price_text}")

            offer = {
                "price": price,
                "condition": condition_tag.text.strip() if condition_tag else "",
                "seller": seller_tag.text.strip() if seller_tag else "",
            }

            print(f"📦 Offre #{idx} : {offer}")
            offers.append(offer)

        return offers

    except Exception as e:
        print(f"❌ Exception : {e}")
        return []
    
