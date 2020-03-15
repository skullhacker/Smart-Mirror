import requests
from bs4 import BeautifulSoup as bs
from itertools import cycle


class News:

    def __init__(self):
        url = 'https://inshorts.com/en/read'
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError
        soup = bs(response.text, features="html5lib")
        self.headlines = soup.find_all(attrs={"itemprop": "headline"})
        self.headline = cycle(self.headlines)

    def getheadline(self):
        return next(self.headline).text


if __name__ == "__main__":
    n = News()
    for i in range(50):
        print(n.getheadline())
