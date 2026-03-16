from bs4 import BeautifulSoup
from curl_cffi import requests as cf_requests
import time
import random

BASE_URL = "https://uk.camelcamelcamel.com"

categories = {
    "automotive":                 "248877031",
    "baby-products":              "59624031",
    "beauty":                     "117332031",
    "books":                      "266239",
    "clothing":                   "83450031",
    "computers-accessories":      "340831031",
    "diy-tools":                  "79903031",
    "electronics-photo":          "560798",
    "grocery":                    "340834031",
    "health-personal-care":       "65801031",
    "home-garden":                "3146281",
    "jewellery":                  "193716031",
    "kindle-store":               "341677031",
    "large-appliances":           "908798031",
    "lighting":                   "213077031",
    "luggage":                    "2454166031",
    "music":                      "229816",
    "musical-instruments-dj":     "340837031",
    "other":                      "0",
    "pc-video-games":             "300703",
    "pet-supplies":               "340840031",
    "shoes-bags":                 "355005011",
    "shops":                      "284658",
    "software":                   "300435",
    "sports-outdoors":            "318949011",
    "stationery-office-supplies": "192413031",
    "toys-games":                 "468292",
    "video":                      "283920",
}

# ── SESSION ─────────────────────────────────────────────────

session = cf_requests.Session(
    impersonate="safari15_5",
    headers={
        "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection":      "keep-alive",
        "Referer":         f"{BASE_URL}/",
    }
)

# ── SCRAPER ─────────────────────────────────────────────────

def scrape_category(category_name, category_id, pages=3):
    deals = []

    for page_num in range(1, pages + 1):
        url = f"{BASE_URL}/top_drops?bn={category_id}&d=1&i=7&s=relative&t=recent&p={page_num}"
        print(f"Scraping {category_name} — page {page_num}...")

        try:
            response = session.get(url)

            if response.status_code == 403:
                print(f"  ✗ 403 — still being blocked")
                break
            elif response.status_code != 200:
                print(f"  ✗ Failed with status {response.status_code}")
                break

            soup     = BeautifulSoup(response.text, "lxml")
            products = soup.find_all("div", class_="grid-x grid-margin-x")

            if not products:
                print(f"  No products found on page {page_num}")
                break

            for product in products:
                try:
                    # Name
                    title_tag     = product.find("a", class_="truncy_title")
                    name          = title_tag["title"].replace("Price history for ", "").strip()

                    # Camel URL
                    camel_url     = title_tag["href"]
                    if camel_url.startswith("/"):
                        camel_url = BASE_URL + camel_url

                    # Current price
                    current_price = product.find("div", class_="current_price").text.strip()

                    # Discount
                    discount      = product.find("div", class_="compare_price").text.strip()

                    # Image
                    img_tag       = product.find("div", class_="thumbph")
                    img_url       = img_tag.find("img")["src"] if img_tag else "N/A"

                    # Amazon UK buy link
                    buy_tag       = product.find("a", class_="buy")
                    amazon_url    = buy_tag["href"] if buy_tag else "N/A"

                    deal = {
                        "name":          name,
                        "category":      category_name,
                        "current_price": current_price,
                        "discount":      discount,
                        "img_url":       img_url,
                        "src_url":       amazon_url,
                        "camel_url":     camel_url,
                    }
                    deals.append(deal)

                    print(f"  ✓ {name}")
                    print(f"    Price: {current_price} | {discount}")

                except (AttributeError, TypeError) as e:
                    print(f"  ✗ Skipped — {e}")
                    continue

            # Random delay between pages
            time.sleep(random.uniform(2, 4))

        except Exception as e:
            print(f"  ✗ Request failed: {e}")
            break

    return deals


def scrape_all_categories(pages=3):
    all_deals = []

    # Hit homepage first to get cookies
    session.get(BASE_URL)
    time.sleep(random.uniform(1, 3))

    for category_name, category_id in categories.items():
        deals = scrape_category(category_name, category_id, pages)
        all_deals.extend(deals)
        print(f"  → {len(deals)} deals found in {category_name}\n")

    return all_deals


def scrape_single_category(pages=3):
    print("Available categories:")
    for name in categories:
        print(f"  - {name}")

    category_input = input("\nEnter a category: ").lower().strip()
    category_id    = categories.get(category_input)

    if not category_id:
        print("Category not found")
        return []

    # Hit homepage first to get cookies
    session.get(BASE_URL)
    time.sleep(random.uniform(1, 3))

    return scrape_category(category_input, category_id, pages)


# ── RUN ─────────────────────────────────────────────────────

if __name__ == "__main__":
    mode = input("Scrape (a)ll categories or (s)ingle? ").lower().strip()

    if mode == "a":
        deals = scrape_all_categories(pages=3)
    else:
        deals = scrape_single_category(pages=3)

    print(f"\n── Results ──────────────────────────────────────")
    print(f"Total deals scraped: {len(deals)}")
    for deal in deals:
        print(f"  {deal['name']}")
        print(f"  Price: {deal['current_price']} | {deal['discount']}")
        print(f"  Amazon: {deal['src_url']}")
        print(f"  ---")
