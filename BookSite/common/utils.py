""" This folder can expand to include multuple modules that will have common functionality.
Common functions can be grouped in utils.py until there is a need to separate them."""
from lxml import etree
import io
import requests
from PIL import Image
import requests, sys, webbrowser, bs4


"""From Test Bookstore"""
def get_image_from_url(element):
    image_response = requests.get(element)
    img = Image.open(io.BytesIO(image_response.content))
    return img

"""From Test Bookstore"""
def get_root_from_url(url):
    content = requests.get(url).content
    parser = etree.HTMLParser(remove_pis=True)
    tree = etree.parse(io.BytesIO(content), parser)
    root = tree.getroot()
    return root

"""From Kobo"""
def queryHtml(root, expr):
    result = None
    try:
        result = root.xpath(expr)[0]
    except:
        print("WARNING: Could not retrieve data for " + expr)

    return result

def testBookStoreLinkSearch(searchVar):
        links = []
        link = 'http://127.0.0.1:8000/testBookstore/library/?q=' + searchVar
        res = requests.get(link)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, "html.parser")

        for link in soup.find_all('a', class_="book_title"):
            links.append("http://127.0.0.1:8000/testBookstore" + link.get('href'))

        return links
