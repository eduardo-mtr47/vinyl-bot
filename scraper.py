import cloudscraper
from bs4 import BeautifulSoup
import re

def extract_price_and_currency(price_text):
    raw = price_text.strip()
    currency_match = re.search(r'(€|£|\$|USD|GBP|CAD|AUD|DKK)', raw)
    currency = currency_match.group(1) if currency_match else None

    amount_str = re.sub(r'[^\d,\.]', '', raw)
    if ',' in amount_str and '.' in amount_str:
        if amount_str.index(',') > amount_str.index('.'):
            amount_str = amount_str.replace('.', '').replace(',', '.')
        else:
            amount_str = amount_str.replace(',', '')
    elif ',' in amount_str:
        amount_str = amount_str.replace(',', '.')

    try:
        amount = float(amount_str)
    except ValueError:
        amount = None

    return amount, currency

def get_offers_for_release(release_id):
    url = f"https://www.discogs.com/sell/release/{release_id}"
    print(f"\n🌐 Scraping {url}")

    scraper = cloudscraper.create_scraper(browser={'custom': 'VinylBot/1.0'})
    try:
        response = scraper.get(url, timeout=10)
        print(f"🔁 Statut HTTP : {response.status_code}")
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        listings = soup.select(".shortcut_navigable")
        offers = []

        for item in listings:
            price_el = item.select_one(".price")
            condition_el = item.select_one(".item_condition")
            seller_el = item.select_one(".seller_info")
            link_el = item.select_one("a[itemprop='url']")

            if not price_el:
                continue

            price_text = price_el.get_text(" ", strip=True)
            price, currency = extract_price_and_currency(price_text)

            offer = {
                "price": price,
                "currency": currency,
                "condition": condition_el.get_text(" ", strip=True) if condition_el else "",
                "seller": seller_el.get_text(" ", strip=True) if seller_el else "",
                "url": f"https://www.discogs.com{link_el['href']}" if link_el else ""
            }
            offers.append(offer)

        return offers

    except Exception as e:
        print(f"❌ Scraping error: {e}")
        return []
