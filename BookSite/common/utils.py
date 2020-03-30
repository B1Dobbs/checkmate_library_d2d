""" This folder can expand to include multuple modules that will have common functionality.
Common functions can be grouped in utils.py until there is a need to separate them."""
from lxml import etree
import io
import requests
from PIL import Image
from isbnlib import to_isbn13


def get_image_from_url(url):
    """
    Will get the pillow image from a url

        Args:
            url: the URL for the image

        Returns:
            A Pillow image
    """
    image_response = requests.get(url)
    img = Image.open(io.BytesIO(image_response.content))
    return img

def get_root_from_url(url):
    """
    Will get the lxml root for an html file.

        Args:
            url: the URL for the website

        Returns:
            An etree root for the page.
    """
    content = requests.get(url).content
    parser = etree.HTMLParser(remove_pis=True)
    tree = etree.parse(io.BytesIO(content), parser)
    root = tree.getroot()
    return root

def query_html(root, expr, get_list=False):
    """
    Wrapper for node.xpath() to prevent IndexOutOfBounds Exception

        Args:
            root: the starting node for the xpath expression
            expr: the string expression to query with

        Returns:
            - Single node for unique query
            - Array for queries that are not unique
            - None when the query result is empty
    """
    try:
        result = root.xpath(expr)
        if len(result) == 1 and not get_list:
            result = result[0]
        elif len(result) == 0:
            result = None
    except:
        print("WARNING: Could not retrieve data for " + expr)

    return result

"""ISBN 10 to ISBN 13 conversion """
def isbn10_to_isbn13(isbn10):
    return to_isbn13(isbn10)
