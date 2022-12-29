import requests
from bs4 import BeautifulSoup
from csv import DictWriter
import time

page_num = 1
BASE_URL = "http://quotes.toscrape.com"
URL = f"http://quotes.toscrape.com/page/{page_num}"
next_page_url = "/page/1"

with open("quotes2.csv", "a") as csvfile:
    headers = ("Text", "Author", "Bio")
    csv_writer = DictWriter(csvfile, fieldnames=headers)
    csv_writer.writeheader()
    while next_page_url:
        response = requests.get(f"{BASE_URL}{next_page_url}")
        data = response.text
        soup = BeautifulSoup(data, "html.parser")
        all_quotes = soup.select(".quote")
        for quote in all_quotes:
            quote_text = quote.find(class_="text").get_text()
            author = quote.find(class_="author").get_text()
            link_ending = quote.find_all("a")[0]["href"]
            bio_link = BASE_URL + link_ending
            csv_writer.writerow({
                "Text": quote_text,
                "Author": author,
                "Bio": bio_link,
            })
        print(f"Finished scraping {BASE_URL}{next_page_url}")
        next_btn = soup.find(class_="next")
        next_page_url = next_btn.find("a")["href"] if next_btn else None
        time.sleep(2)
    print("Finished")
