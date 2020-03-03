from BookData import BookData
from lxml import etree
import io
import requests, sys, webbrowser, bs4
from PIL import Image
from BookSite.common.utils import *
from Checkmate import *

def testSiteQuery():

    book_data = BookData()

    book_data.authors = "vergara"

    book_data.isbn_13 = None
    
    links = []

    if book_data.authors != None: # If a title is sent in to search by, record link matches
        links += koboLinkSearch(book_data.authors)

    if book_data.isbn_13 != None: # If a title is sent in to search by, record link matches
        links += koboLinkSearch(book_data.isbn)

    if book_data.title != None: # If a title is sent in to search by, record link matches
        links += koboLinkSearch(book_data.title)


    linksNoDuplicates = [] 
    for i in links: 
        if i not in linksNoDuplicates: 
            linksNoDuplicates.append(i) #removes duplicate links from list

    print(linksNoDuplicates)

def testScribd():

    book_data = BookData()

    #book_data.authors = ""

    book_data.title = "harry potter and the sorcerer's stone"

    book_data.isbn_13 = None

    book_site = get_book_site("SB")
    print(book_site.find_book_matches(book_data))

    
def testKobo():
    book_data = BookData()
    book_data.title = "Zombie"
    
    book_site = get_book_site("KB")
    print(book_site.find_book_matches(book_data))
    

if __name__ == "__main__":
    #testSiteQuery()
    testScribd()
    #testKobo()