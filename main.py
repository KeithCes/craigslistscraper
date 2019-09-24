import tkinter as tk
import requests
from bs4 import BeautifulSoup


class Main(tk.Tk):

    def __init__(self):

        # setup and title
        tk.Tk.__init__(self)
        self.winfo_toplevel().title("Craigslist Scraper")

        # creates entries
        self.entryItem = tk.Entry(self)
        self.entryFloor = tk.Entry(self)
        self.entryCap = tk.Entry(self)
        self.entryKeywords = tk.Entry(self)

        # creates and pushes labels
        tk.Label(text='Item').grid(row=0)
        tk.Label(text='Minimum Price').grid(row=1)
        tk.Label(text='Maximum Price').grid(row=2)
        tk.Label(text='Keywords (Separate by Commas)').grid(row=3)

        # adds button
        self.button = tk.Button(self, text="Search", command=self.on_button)

        # pushes all non-label items to grid
        self.entryItem.grid(row=0, column=1)
        self.entryFloor.grid(row=1, column=1)
        self.entryCap.grid(row=2, column=1)
        self.entryKeywords.grid(row=3, column=1)
        self.button.grid(row=4, column=1)

    def on_button(self):

        # stores data from textboxes in vars
        item = self.entryItem.get().lower()
        priceFloor = self.entryFloor.get().lower()
        priceCap = self.entryCap.get().lower()
        keywords = self.entryKeywords.get().lower().split(', ')

        # makes a new window and textbox
        returnWindow = tk.Toplevel()
        returnWindow.title('Results')
        returnText = tk.Text(returnWindow, height=50, width=200)
        returnText.grid(row=0)

        # adds information to textbox
        returnText.insert('1.0', "Item Searched: " + item + "\n")
        returnText.insert('2.0', "Minimum Price: " + priceFloor + "\n")
        returnText.insert('3.0', "Maximum Price: " + priceCap + "\n")
        returnText.insert('4.0', "Keywords: " + ', '.join(keywords) + "\n")
        returnText.insert('5.0', "\n" + "\n")

        # nulls data if none entered
        if priceFloor == "":
            priceFloor = None
        if priceCap == "":
            priceCap = None

        # null checks priceFloor and priceCap (needed for choosing url) and
        # sends necessary data to scrape()
        if priceFloor is None and priceCap is None:
            returnText.insert('6.0', scrape(item, keywords, None, None) + "\n")
        elif priceFloor is None and priceCap is not None:
            returnText.insert(
                '6.0',
                scrape(
                    item,
                    keywords,
                    None,
                    int(priceCap)) +
                "\n")
        elif priceFloor is not None and priceCap is None:
            returnText.insert(
                '6.0',
                scrape(
                    item,
                    keywords,
                    int(priceFloor),
                    None) + "\n")
        elif priceFloor is not None and priceCap is not None:
            returnText.insert(
                '6.0',
                scrape(
                    item,
                    keywords,
                    int(priceFloor),
                    int(priceCap)) +
                "\n")


def scrape(item, keywords, priceFloor, priceCap):

    # chooses which url to scrape based on data received
    if priceFloor is None and priceCap is None:
        page = requests.get(
            "https://boston.craigslist.org/search/sss?query=" +
            item +
            "&sort=rel")
    elif priceFloor is None and priceCap is not None:
        page = requests.get(
            "https://boston.craigslist.org/search/sss?query=" +
            item +
            "&sort=rel" +
            "&max_price=" +
            str(priceCap))
    elif priceFloor is not None and priceCap is None:
        page = requests.get(
            "https://boston.craigslist.org/search/sss?query=" +
            item +
            "&sort=rel" +
            "&min_price=" +
            str(priceFloor))
    elif priceFloor is not None and priceCap is not None:
        page = requests.get(
            "https://boston.craigslist.org/search/sss?query=" +
            item +
            "&sort=rel" +
            "&max_price=" +
            str(priceCap) +
            "&min_price=" +
            str(priceFloor))

    # checks to make sure scraping was successful or not
    if page.status_code == 200:
        print("@@@ SUCCESSFULLY SCRAPED @@@")
    else:
        print("@@@ ERROR @@@")
    soup = BeautifulSoup(page.content, 'html.parser')

    # parses out the required sections from the scraped page
    offers = soup.find("div", {"id": "sortable-results"})
    offers = offers.find('ul')
    titles = offers.find_all('a', {"class": "result-title hdrlnk"})
    urls = offers.find_all('a', {"class": "result-title hdrlnk"}, href=True)
    prices = offers.find_all('span', {"class": "result-price"})

    # logic behind searching
    returnData = ""
    for p in range(0, len(titles) - 1):
        if len(keywords) > 0:
            for q in keywords:
                if q.lower() in titles[p].get_text().lower():
                    returnData += prices[p].get_text() + "\n" + titles[p].get_text() + \
                        "\n" + urls[p]['href'] + "\n" + "\n"
    returnData = returnData.encode('ascii', 'ignore').decode('ascii')
    return returnData


app = Main()
app.mainloop()
