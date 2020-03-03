from BookData import BookData
from lxml import etree
from BookSite.common.utils import *
import sys
import re

"""Given a direct link to a book page at a site, parse it and return the SiteBookData of the info""" 
def get_book_data(url):
    # type: (str) -> SiteBookData 
    print("Get book data function from Scribd")
    return 0


"""Given a SiteBookData, search for the book at the `book_site` site
and provide a list of likely matches paired with how good
of a match it is (1.0 is an exact match). 
This should take into account all the info we have about a book, 
including the cover.""" 
def find_book_matches(book_data):
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

    print(links)
    linksNoDuplicates = [] 
    for i in links: 
        if i not in linksNoDuplicates: 
            linksNoDuplicates.append(i) #removes duplicate links from list
    # FINISH -> LINKS HAS ALL LINKS WITH ANY MATCHING

    book_matches = []
    for lnk in linksNoDuplicates:
        search_book_data = get_book_data(lnk)
        book_matches.append(search_book_data)
        #search_book_data.printData()
    return book_matches


"""Given a book_id, return the direct url for the book.""" 
def convert_book_id_to_url(book_id):
    # type: (str) -> str 
    print("Convert book id function from Scribd")