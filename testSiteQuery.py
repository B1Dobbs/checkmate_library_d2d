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
    
    links = []
    if book_data.authors != None: # If a title is sent in to search by, record link matches
        links += scribdLinkSearch(book_data.authors)

    if book_data.isbn != None: # If a title is sent in to search by, record link matches
        links += scribdLinkSearch(book_data.isbn)

    if book_data.title != None: # If a title is sent in to search by, record link matches
        links += scribdLinkSearch(book_data.title)
       
    linksNoDuplicates = [] 
    for i in links: 
        if i not in linksNoDuplicates: 
            linksNoDuplicates.append(i) #removes duplicate links from list
    # FINISH -> LINKS HAS ALL LINKS WITH ANY MATCHING
    for lnk in linksNoDuplicates:
        print(lnk)
    

if __name__ == "__main__":
    testSiteQuery()
    #testKobo()