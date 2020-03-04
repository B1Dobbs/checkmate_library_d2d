from BookData import BookData
from lxml import etree
from BookSite.common.utils import *
import requests, sys, webbrowser, bs4
import io
import json
import re 


"""Given a direct link to a book page at a site, parse it and return the SiteBookData of the info""" 
def get_book_data(url):
    # type: (str) -> SiteBookData 
    print("Get book data function from Scribd")
    book_data = BookData()
    root = get_root_from_url(url)
    print(queryHtml(root, "//div/section/dl/dd[2]"))
    try:
        j = queryHtml(root, "//script[@type = 'application/ld+json']")[1].text
        y = json.loads(j)
        
        title = queryHtml(root, "//h1[@class='document_title']").text
        book_data.title = title
        book_data.format = y['@type']

        book_data.image_url = root.xpath(".//div[@class='document_cell']//img/@src")[0]
        book_data.image = get_image_from_url(book_data.image_url)
        book_data.description = queryHtml(root, "//div[@style='overflow-wrap: break-word;']")
    
        roottext = etree.tostring(root, encoding = "unicode")
        roottext = roottext.split('"')
        p = re.compile('^(97(8|9))?\d{9}(\d|X)$')

        for i in roottext:
            l = p.search(i)
            if(l != None):
                book_data.isbn = l.string
                
        
        book_data.authors = y['author'][0]['name']
        
        book_data.book_id = book_data.isbn
        book_data.content = queryHtml(root, "/html")
        book_data.site_slug = "SD"

        book_data.url = convert_book_id_to_url(book_data.book_id)

        book_data.ready_for_sale = True

       # book_data.extra = {"price" : queryHtml(root, ".//span[@id='price']").text, "releaseDate" : queryHtml(root, ".//span[@id='release_date']").text}
        print(etree.tostring(root, encoding = "unicode"))
    except:
        print("ERROR: Processing book at " + url)
        print(sys.exc_info()[0])

    return book_data

"""Given a SiteBookData, search for the book at the `book_site` site
and provide a list of likely matches paired with how good
of a match it is (1.0 is an exact match). 
This should take into account all the info we have about a book, 
including the cover.""" 
def find_book_matches(book_data):
    # type: (SiteBookData) -> List[Tuple[SiteBookData, float]] 
    print("Find book matches function from Scribd")


"""Given a book_id, return the direct url for the book.""" 
def convert_book_id_to_url(book_id):
    # type: (str) -> str 
    print("Convert book id function from Scribd")