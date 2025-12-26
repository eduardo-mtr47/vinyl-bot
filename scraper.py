import re
import cloudscraper
from bs4 import BeautifulSoup

def parse_price(raw_price: str):
    """
    Extrait le prix et le convertit en EUR si besoin
    """
    text = raw_price.replace(",", ".").lower()

    # EUR
    eur = re.search(r"€\s*([\d.]+)", text)
    if eur:
        return float(eur.group(1))

    # GBP → EUR (approx)
    gbp = re.search(r"£\s*([\d.]+)", text)
    if gbp:
        return round(float(gbp.group(1)) * 1.15, 2)

    # USD → EUR (approx)
    usd = re.search(r"\$\s*([\d.]+)", text)
    if usd:
        return round(float(usd.group(1)) * 0.92, 2)

    return None


def get_offers_for_release(release_id: int):
    url = f"https://www.discogs.com/sell/release/{release_id}"
    print(f"\n🌐 Requête vers {url}")

    scraper = cloudscraper.create_scraper(
        browser={"custom": "VinylFinderBot/1.0"}
    )

    try:
        response = scraper.get(url, timeout=20)
        print(f"🔁 Statut HTTP : {response.status_code}")

        if response.status_code != 200:
            print("⛔️ Accès refusé ou page indisponible.")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.select(".shortcut_navigable")
        print(f"🔍 {len(rows)} offres trouvées dans le HTML.")

        offers = []

        for row in rows:
            price_tag = row.select_one(".price")
            condition_tag = row.select_one(".item_condition")
            seller_tag = row.select_one(".seller_info")

            if not price_tag or not seller_tag:
                continue

            raw_price = price_tag.get_text(" ", strip=True)
            price_eur = parse_price(raw_price)

            shipping = "inclus" if "shipping" not in raw_price.lower() else "non inclus"

            offers.append({
                "price_eur": price_eur,
                "shipping": shipping,
                "condition": condition_tag.get_text(" ", strip=True) if condition_tag else "N/A",
                "seller": seller_tag.get_text(" ", strip=True)
            })

        return offers

    except Exception as e:
        print(f"❌ Erreur scraping : {e}")
        return []
