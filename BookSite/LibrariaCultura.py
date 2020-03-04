from BookData import BookData
from lxml import etree
from BookSite.common.utils import *
import requests, sys, webbrowser, bs4

"""Given a direct link to a book page at a site, parse it and return the SiteBookData of the info""" 
def get_book_data(url):
    book_data = BookData()
    root = get_root_from_url(url)


    try:
        book_data.format = "Digital"
        title = queryHtml(root, ".//meta[@property='og:title']/@content")
        book_data.title = str(title)

        subtitle = queryHtml(root, ".//th[contains(text(), 'Subtitulo')]/following-sibling::td")
        if(subtitle is not None):
            book_data.subtitle = subtitle.text

        imageUrl = queryHtml(root, ".//meta[@itemprop='image']/@content")
        book_data.image_url = str(imageUrl)
        book_data.image = get_image_from_url(book_data.image_url)

        book_data.isbn = queryHtml(root, ".//th[contains(text(), 'ISBN')]/following-sibling::td").text
        book_data.description = str(queryHtml(root, ".//meta[@property='og:title']/following-sibling::meta[@property='og:description']/@content"))

        #Series and Volume Number are not available on site

        authorsTag = queryHtml(root, ".//th[contains(text(), 'Colaborado')]/following-sibling::td").text

        #Parsing Author Name
        collaborators = authorsTag.split("|")
        matchingAuthor = [s for s in collaborators if "Autor" in s]
        authorsArray = []

        for a in matchingAuthor:
            authorsNamesString = a.split(":")
            authorsNamesArray = authorsNamesString[1].split(",")
            authorsArray.append(authorsNamesArray[1].strip() + " " + authorsNamesArray[0].strip())
        
        book_data.authors = authorsArray

        book_data.site_slug = "LC"

        bookURL = str(queryHtml(root, ".//meta[@itemprop='url']/@content"))
        book_data.url = bookURL

        bookID = bookURL.split('.br')
        book_data.book_id = bookID[1]

        book_data.content = queryHtml(root, "/html")

        book_data.ready_for_sale = True

        #Price is gathered as extra data
        book_data.extra = {"price" : str(queryHtml(root, ".//meta[@property='product:price:amount']/@content"))}

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
    links = []
    if book_data.authors != None: # If a title is sent in to search by, record link matches
        links += librariaLinkSearch(book_data.get_authors_as_string())

    if book_data.isbn != None: # If a title is sent in to search by, record link matches
        links += librariaLinkSearch(book_data.isbn)

    if book_data.title != None: # If a title is sent in to search by, record link matches
        links += librariaLinkSearch(book_data.title)
        
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
    print("Convert book id function from Libraria")