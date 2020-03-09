""" This folder can expand to include multuple modules that will have common functionality.
Common functions can be grouped in utils.py until there is a need to separate them."""
from lxml import etree
import io
import requests
from PIL import Image
from Levenshtein import ratio, distance
import requests, sys, webbrowser, bs4
import json
import re
import regex # pip install regex
from Levenshtein import distance, ratio
from isbnlib import *
import math


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

def queryHtml(root, expr):
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
        if len(result) == 1:
            result = result[0]
        elif len(result) == 0:
            result = None
    except:
        print("WARNING: Could not retrieve data for " + expr)

    return result

def get_matches_from_links(get_book_data, linkList, book_data):
     # For each link, get the book data and compare it with the passed in book_data
    book_matches = []
    for lnk in linkList:
        search_book_data = get_book_data(lnk)
        match_value = compare_book_data(search_book_data, book_data)
        search_book_data.printData()
        print("MATCH: ", match_value)
        if(match_value != 0.0):
            book_matches.append((match_value, search_book_data))

    return book_matches


def compare_book_data(book1, book2):
    """ Calculates the perecent match between two book_data objects using the Levenshtein Formula

    Args:
        book1 (book_data): The book data used for the 1st book in the comparison
        book2 (book_data): The book data used for the 2nd book in the comparison

    Returns:
        float: the percent match between the two book_data objects
    """
    percent = 0
    count = 0
    for attr, value in book1.__dict__.items():
        isEmptyList = value == [] or book2.__dict__[attr] == []

        # Testing if both values of a certain attribute are none for both book_data objects
        if(value != None and book2.__dict__[attr] != None and not isEmptyList):

            # Creating a regex pattern that will filter out all special characters from the values
            pattern =  '[^A-Za-z0-9 ,]+'
            book2Str = str.lower(re.sub(pattern, "", str(book2.__dict__[attr])))
            book1Str = str.lower(re.sub(pattern, "", str(book1.__dict__[attr])))

            # Testing if book2's value is a substring of book1's value
            # or if the distance (number of edits) are less than or equal to 5
            isSubstring = book2Str in book1Str or book1Str in book2Str
            if(isSubstring or distance(book2Str, book1Str) <= 5):
                percent += ratio(book2Str, book1Str)
            count += 1

    # Testing if there were 0 matches else return the percent match rounded to the 2nd decimal place
    if(count == 0):
        return 0.0
    else:
        return round((percent / count), 2)


"""ISBN 10 to ISBN 13 conversion """
def isbn10to13(isbn10):
    return to_isbn13(isbn10)
