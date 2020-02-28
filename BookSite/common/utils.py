""" This folder can expand to include multuple modules that will have common functionality.
Common functions can be grouped in utils.py until there is a need to separate them."""
from lxml import etree
import io
import requests
from PIL import Image
from Levenshtein import ratio
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

def compare_book_data(book1, book2):
    percent = 0
    count = 0
    for attr, value in book1.__dict__.items():
        if(value != None and book2.__dict__[attr] != None):
            percent += ratio(str(book1.__dict__[attr]), str(book2.__dict__[attr])) * 100
            count += 1
    return round((percent / count), 2)

def librariaLinkSearch(searchVar):
    links = []
    link = 'https://www3.livrariacultura.com.br/ebooks/?ft=' + searchVar
    res = requests.get(link)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    for p in soup.find_all('div', class_="prateleiraProduto__informacao__preco"):
        for link in p.find_all('a'):
            links.append(link.get('href'))

    return links

def googleLinkSearch(searchVar):
    links = []
    link = 'https://play.google.com/store/search?q=' + searchVar + '&c=books&hl=en_US'
    res = requests.get(link)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    for p in soup.find_all('div', class_="prateleiraProduto__informacao__preco"):
        for link in p.find_all('a'):
            links.append(link.get('href'))

    return links

""" Search test Book Store for relevant links """
def testBookStoreLinkSearch(searchVar):
    links = []
    link = 'http://127.0.0.1:8000/testBookstore/library/?q=' + searchVar
    res = requests.get(link)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    for link in soup.find_all('a', class_="book_title"):
        links.append("http://127.0.0.1:8000/testBookstore" + link.get('href'))

    return links

""" Searching Kobo for relevant links """
def koboLinkSearch(searchVar):
    links = []
    link = 'https://www.kobo.com/us/en/search?query=' + searchVar
    res = requests.get(link)
    res.raise_for_status
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    for p in soup.find_all('p', class_="title product-field"):
        for link in p.find_all('a'):
            links.append(link.get('href'))

    return links





