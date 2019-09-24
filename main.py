import requests
from bs4 import BeautifulSoup

# changes what you search on craigslist (ex: "computer" would search computer)
searchRequest = "computer"

# changes what you search for within a search (ex: "refurbished" would only show posts with "refurbished in the post)
keywords = [""]

# minimum price
priceFloor = 0

# maximum price
priceCap = 500

# gets and scrapes craigslist
page = requests.get("https://boston.craigslist.org/search/sss?query=" + searchRequest + "&sort=rel")
if page.status_code == 200:
    print("@@@ SUCCESSFULLY SCRAPED @@@")
else:
    print("@@@ ERROR @@@")
soup = BeautifulSoup(page.content, 'html.parser')

# parses out the required sections from the scraped page
offers = soup.find("div", {"id": "sortable-results"})
offers = offers.find('ul')
titles = offers.find_all('a', {"class": "result-title hdrlnk"})
urls = offers.find_all('a',{"class": "result-title hdrlnk"}, href=True)
prices = offers.find_all('span', {"class": "result-price"})

# logic behind searching
for p in range(0, len(titles) - 1):
    priceNum = int(prices[p].get_text()[1:])
    if len(keywords) > 0:
        for q in keywords:
            if q.lower() in titles[p].get_text().lower() and (priceFloor <= priceNum <= priceCap):
                print(prices[p].get_text())
                print(titles[p].get_text())
                print(urls[p]['href'])
