from BookData import BookData
from lxml import etree
import io
import requests, sys, webbrowser, bs4
from PIL import Image
    
def testSiteQuery():
    author = 'peter vergara'
    link = 'http://127.0.0.1:8000/testBookstore/library/?q=' + author

    res = requests.get(link)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    links = []

    for link in soup.find_all('a', class_="book_title"):
        links.append("http://127.0.0.1:8000/testBookstore" + link.get('href'))

    print(links)

    #linkToOpen = min(5, len(linkElements))

    

if __name__ == "__main__":
    testSiteQuery()