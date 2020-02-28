from BookData import BookData
from lxml import etree
from BookSite.common.utils import *
import sys

"""Given a direct link to a book page at a site, parse it and return the SiteBookData of the info""" 
def get_book_data(url):
    book_data = BookData()
    root = get_root_from_url(url)

    try:
        book_data.title = str.strip(queryHtml(root, ".//span[@class='title product-field']").text)
        book_data.image_url = "https:" + queryHtml(root, ".//div[@class='item-image']//img/@src")
        book_data.image = get_image_from_url(book_data.image_url)

    except:
        print("ERROR: Processing book at " + url)
        print(sys.exc_info()[0])
        raise

    return book_data


"""Given a SiteBookData, search for the book at the `book_site` site
and provide a list of likely matches paired with how good
of a match it is (1.0 is an exact match). 
This should take into account all the info we have about a book, 
including the cover.""" 
def find_book_matches(book_data):

    links = []
    if 'authors' in book_data.keys(): # If an author is sent in to search by, record link matches
        links.append(koboLinkSearch(book_data['authors']))
        
    if 'isbn_13' in book_data.keys(): # If an isbn is sent in to search by, record link matches
        links.append(koboLinkSearch(book_data['isbn_13']))
        
    if 'title' in book_data.keys(): # If a title is sent in to search by, record link matches
        links.append(koboLinkSearch(book_data['title']))
    
    if 'series' in book_data.keys(): # If a title is sent in to search by, record link matches
        links.append(koboLinkSearch(book_data['series']))
        
    linksNoDuplicates = [] 
    for i in links: 
        if i not in linksNoDuplicates: 
            linksNoDuplicates.append(i) #removes duplicate links from list
    # FINISH -> LINKS HAS ALL LINKS WITH ANY MATCHING
    for lnk in linksNoDuplicates:
        print(lnk)


"""Given a book_id, return the direct url for the book.""" 
def convert_book_id_to_url(book_id):
    # type: (str) -> str 
    print("Convert book id function from Kobo")