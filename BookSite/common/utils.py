""" This folder can expand to include multuple modules that will have common functionality.
Common functions can be grouped in utils.py until there is a need to separate them."""
from lxml import etree
import io
import requests
from PIL import Image
from Levenshtein import ratio

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