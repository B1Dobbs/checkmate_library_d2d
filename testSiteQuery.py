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
        links += testBookStoreLinkSearch(book_data.authors)

    if book_data.isbn_13 != None: # If a title is sent in to search by, record link matches
        links += testBookStoreLinkSearch(book_data.isbn)

    if book_data.title != None: # If a title is sent in to search by, record link matches
        links += testBookStoreLinkSearch(book_data.title)

    print(links)
    
    linksNoDuplicates = [] 
    for i in links: 
        if i not in linksNoDuplicates: 
            linksNoDuplicates.append(i) #removes duplicate links from list
    

if __name__ == "__main__":
    testSiteQuery()
    #testKobo()