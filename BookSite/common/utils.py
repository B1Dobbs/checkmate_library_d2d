""" This folder can expand to include multuple modules that will have common functionality.
Common functions can be grouped in utils.py until there is a need to separate them."""
from lxml import etree
import io
import requests
from PIL import Image
from isbnlib import *

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
    try:
        result = root.xpath(expr)
        if len(result) == 1:
            result = result[0]
        elif len(result) == 0:
            result = None
            raise LookupError

    except LookupError:
        print("WARNING: No data found for " + expr)
    except:
        print("WARNING: Could not retrieve data for " + expr)

    return result

"""ISBN 10 to ISBN 13 conversion """
def isbn10to13(isbn10):
    return to_isbn13(isbn10)