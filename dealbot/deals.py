from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

categories = { #categories to be tracked 
    "home": "home-living",
    "electronics": "electronics",
    "family": "family-kids",
    "fashion": "fashion-accessories",
    "garden": "garden-do-it-yourself",
    "travel": "travel",
    "culture": "culture-leisure",
    "groceries": "groceries",
    "services": "services-contracts",
    "health": "health-beauty",
    "sports": "sports-outdoors",
    "gaming": "gaming",
    "broadband": "broadband-phone-contracts",
    "car": "car-motorcycle",
    "finance": "finance-insurance",
    "air fryer": "air-fryer",
    "coffee machine": "coffee-machine",
    "fans": "fans",
    "appliances": "home-appliances",
    "lighting": "lighting",
    "vacuum": "vacuum-cleaner",
    "fire stick": "amazon-fire-tv-stick",
    "apple tv": "apple-tv",
    "pixel": "google-pixel",
    "graphics card": "graphics-card",
    "laptop": "laptop",
    "phone": "mobile-phone",
    "tv": "tv",
    "iphone": "iphone",
}

category_input = input("Enter category: ").lower() #tracks input for now 
category = categories.get(category_input)

if not category: #checks if entered correctly - but in actual website will have selector tabs to avoid user entering category incorrectly 
    print("Category not found")

else:
    with sync_playwright() as p: # this allows us to index dynamic pages and wait for data to load before it is grabbed for example price 
        # Launch with extra args to avoid detection
        browser = p.chromium.launch(
            headless=False,   # keep visible while testing
            args=["--disable-blink-features=AutomationControlled"]
        )

        # Create context that looks like a real browser
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="en-GB",
        )

        tab = context.new_page()

        for page_num in range(1, 100): #loops through pages 
            url = f"https://www.hotukdeals.com/tag/{category}?page={page_num}"
            
            try:
                tab.goto(url, timeout=30000, wait_until="domcontentloaded")  # ← less strict wait
                tab.wait_for_timeout(3000)  # ← give JS 3 seconds to load prices
                
            except Exception as e:
                print(f"Page failed to load: {e}")
                break

            if page_num > 1 and tab.url != url: #skips page one and check through all the urls untill theres no more pages 
                print("No more pages")
                break

            html = tab.content()
            soup = BeautifulSoup(html, "lxml")
            items = soup.find_all('div', class_="threadListCard")

            if not items:
                print("No more pages")
                break

            for item in items:
                name = item.find('a', title=True) #searches for the attrabutes and tags with the correct data
                price = item.find('span', class_="thread-price")
                image = item.find('img')
                image_url = image["src"] if image else "N/A"

                item_name = name['title'] if name else "N/A"
                item_price = price.text.strip() if price else "N/A"

                print(f"Item Name: {item_name}")
                print(f"Item Price: {item_price}")
                print("---")
                print(image_url)

        browser.close()

