import requests
from bs4 import BeautifulSoup
from csv import DictWriter

page_num = 1
BASE_URL = "http://quotes.toscrape.com"
URL = f"http://quotes.toscrape.com/page/{page_num}"
keep_going = True

with open("quotes.csv", "a") as csvfile:
    headers = ("Text", "Author", "Bio")
    csv_writer = DictWriter(csvfile, fieldnames=headers)
    csv_writer.writeheader()
    while keep_going:
        response = requests.get(f"{BASE_URL}/page/{page_num}")
        data = response.text
        soup = BeautifulSoup(data, "html.parser")
        if soup.find(class_="next"):
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
            print(f"Finished scraping {BASE_URL}/page/{page_num}")
            page_num += 1
        else:
            print("Finished")
            keep_going = False
