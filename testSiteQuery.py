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

    book_data.title = "caveman"

    book_data.isbn_13 = None
    
    links = []

    titleLinkSearch = ""

    if book_data.authors != None: # If a title is sent in to search by, record link matches
        titleLinkSearch += book_data.authors
    
    if book_data.title != None: # If a title is sent in to search by, record link matches
        if(titleLinkSearch != ""):
            titleLinkSearch += " "
            titleLinkSearch += book_data.title

    if book_data.isbn_13 != None: # If a title is sent in to search by, record link matches
        links += scribdLinkSearch(book_data.isbn)

    if(titleLinkSearch != ""):
        links += scribdLinkSearch(titleLinkSearch)
       
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