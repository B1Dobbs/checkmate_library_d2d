from BookData import BookData
from lxml import etree
import io
import requests, sys, webbrowser, bs4
from PIL import Image
from BookSite.common.utils import *
    
def testSiteQuery():

    book_data = {'authors': 'vergara'}
    
    links = []
    if 'authors' in book_data.keys(): # If an author is sent in to search by, record link matches
        links.append(testBookStoreLinkSearch(book_data['authors']))
        
    if 'isbn_13' in book_data.keys(): # If an isbn is sent in to search by, record link matches
        links.append(testBookStoreLinkSearch(book_data['isbn_13']))
        
    if 'title' in book_data.keys(): # If a title is sent in to search by, record link matches
        links.append(testBookStoreLinkSearch(book_data['title']))
        
    linksNoDuplicates = [] 
    for i in links: 
        if i not in linksNoDuplicates: 
            linksNoDuplicates.append(i) #removes duplicate links from list
    # FINISH -> LINKS HAS ALL LINKS WITH ANY MATCHING
    for lnk in linksNoDuplicates:
        print(lnk)

    

if __name__ == "__main__":
    testSiteQuery()