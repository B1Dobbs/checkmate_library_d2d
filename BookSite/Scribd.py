from BookData import BookData
from lxml import etree
from BookSite.common.utils import *
import requests, sys, webbrowser, bs4, traceback
import io
import json
import re 


"""Given a direct link to a book page at a site, parse it and return the SiteBookData of the info""" 
def get_book_data(url):
    # type: (str) -> SiteBookData 
    book_data = BookData()
    root = get_root_from_url(url)
    #print(queryHtml(root, "//div/section/dl/dd[2]"))
    try:
        #Get ISBN
        j = queryHtml(root, "//script[@type = 'application/ld+json']")[1].text
        y = json.loads(j)
        
        title = queryHtml(root, "//h1[@class='document_title']").text
        book_data.title = title
        book_data.format = y['@type']

        book_data.image_url = root.xpath(".//div[@class='document_cell']//img/@src")[0]
        book_data.image = get_image_from_url(book_data.image_url)
        book_data.description = queryHtml(root, ".//meta[@property='og:description']/@content")
    
        roottext = etree.tostring(root, encoding = "unicode")
        roottext = roottext.split('"')
        p = re.compile('^(97(8|9))?\d{9}(\d|X)$')

        for i in roottext:
            l = p.search(i)
            if(l != None):
                book_data.isbn_13 = l.string
#Get Author List
        authors = []
        for i in range (0, len(y['author'])):
            authors.append(y['author'][i]['name'])
            print(y['author'][i]['name'])
        print(authors)

        book_data.authors = authors

#Get Book ID From URL
        url = queryHtml(root, "//link[@rel = 'alternate'][1]/@href")
        url = url.split('/')
        url.pop(0)
        url.pop(0)
        url.pop(0)
    
        book_data.book_id = url[0]+'/'+url[1]+'/'+url[2]
        book_data.content = queryHtml(root, "/html")
        book_data.site_slug = "SD"

        book_data.url = convert_book_id_to_url(book_data.book_id)

        book_data.ready_for_sale = True

       # book_data.extra = {"price" : queryHtml(root, ".//span[@id='price']").text, "releaseDate" : queryHtml(root, ".//span[@id='release_date']").text}
        #print(etree.tostring(root, encoding = "unicode"))
    except:
        print("ERROR: Processing book at " + url)
        traceback.print_exc()

    return book_data

"""Given a SiteBookData, search for the book at the `book_site` site
and provide a list of likely matches paired with how good
of a match it is (1.0 is an exact match). 
This should take into account all the info we have about a book, 
including the cover.""" 
def find_book_matches(book_data):
    links = []

    titleLinkSearch = ""

    if book_data.authors != None: # If a title is sent in to search by, record link matches
        titleLinkSearch += book_data.get_authors_as_string()
    
    if book_data.title != None: # If a title is sent in to search by, record link matches
        if(titleLinkSearch != ""):
            titleLinkSearch += " "
            titleLinkSearch += book_data.title
        else:
            titleLinkSearch = book_data.title

    if book_data.isbn_13 != None: # If a title is sent in to search by, record link matches
        links += scribdLinkSearch(book_data.isbn)

    if(titleLinkSearch != ""):
        links += scribdLinkSearch(titleLinkSearch)

    linksNoDuplicates = [] 
    for i in links: 
        if i not in linksNoDuplicates: 
            linksNoDuplicates.append(i) #removes duplicate links from list
    # FINISH -> LINKS HAS ALL LINKS WITH ANY MATCHING

   # For each link, get the book data and compare it with the passed in book_data
    book_matches = []
    for lnk in linksNoDuplicates:
        search_book_data = get_book_data(lnk)
        match_value = compare_book_data(search_book_data, book_data)
        if(match_value != 0.0):
            book_matches.append((match_value, search_book_data))

    return book_matches


"""Given a book_id, return the direct url for the book.""" 
def convert_book_id_to_url(book_id):
    # type: (str) -> str 
    return "https://www.scribd.com/" + book_id