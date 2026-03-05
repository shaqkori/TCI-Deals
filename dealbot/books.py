from bs4 import BeautifulSoup
import requests

star_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

categories = {
    "mystery": "mystery_3",
    "travel": "travel_2",
    "romance": "romance_8",
    "science": "science_22"
}

# --- Scrape all pages ---
for i in range(1, 51):
    print(f"Page {i}")
    html_text = requests.get(f"https://books.toscrape.com/catalogue/page-{i}.html").text
    soup = BeautifulSoup(html_text, "lxml")
    books = soup.find_all("article", class_="product_pod")

    for book in books:
        book_name = book.find("a", title=True)['title'].replace(' ', '')
        book_price = book.find('p', class_="price_color").text.replace(' ', '')
        book_stock = book.find('p', class_="instock availability").text.replace(' ', '')
        rating = star_map[book.find("p", class_="star-rating")['class'][1]]

        print(f"Book title: {book_name.strip()}")
        print(f"Book Price: {book_price.strip()}")
        print(f"Book Stock: {book_stock.strip()}")
        print(f"Book Rating: {rating}")
        print("---")


# --- Scrape by category ---
category_input = input("Enter a category (mystery, travel, romance, science): ").lower()  # ask ONCE before loop
category = categories.get(category_input)

if not category:
    print("Category not found")
else:
    for page in range(1, 51):
        url = f"https://books.toscrape.com/catalogue/category/books/{category}/page-{page}.html"
        response = requests.get(url)

        if response.status_code != 200:
            print("No more pages")
            break

        soup = BeautifulSoup(response.text, "lxml")  # response.text not the URL string
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            book_name = book.find("a", title=True)['title'].replace(' ', '')
            book_price = book.find('p', class_="price_color").text.replace(' ', '')
            book_stock = book.find('p', class_="instock availability").text.replace(' ', '')
            rating = star_map[book.find("p", class_="star-rating")['class'][1]]

            print(f"Book title: {book_name.strip()}")
            print(f"Book Price: {book_price.strip()}")
            print(f"Book Stock: {book_stock.strip()}")
            print(f"Book Rating: {rating}")
            print("---")
