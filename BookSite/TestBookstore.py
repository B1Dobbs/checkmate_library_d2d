from BookData import BookData
from lxml import etree
from BookSite.common.utils import *
import requests, sys, webbrowser, bs4

"""Given a direct link to a book page at a site, parse it and return the SiteBookData of the info""" 
def get_book_data(url):
    book_data = BookData()
    root = get_root_from_url(url)

    try:
        book_data.format = queryHtml(root, ".//p[@class='details']").text
        title = queryHtml(root, ".//p[@id='title']/strong").text
        if ":" in title:
            title_array = title.split(":")
            book_data.title = title_array[0]
            book_data.subtitle = title_array[1]
        else:
            book_data.title = title

        """Will work if you add an image to testbook store description page """
        #book_data.image_url = root.xpath(".//img/@src")[0]
        #book_data.image = get_image_from_url(book_data.image_url)

        book_data.isbn = str.strip(queryHtml(root, ".//span[@id='isbn']").text)
        book_data.description = queryHtml(root, "//script[@type='text/javascript']/text()").split("\"")[19]

        book_data.series = str.strip(queryHtml(root, ".//span[@id='series']").text)
        book_data.vol_number = str.strip(queryHtml(root, ".//span[@id='volume_number']").text)
        
        authorsUnstripped = queryHtml(root, ".//span[@id='author']").text
        book_data.authors = str.strip(authorsUnstripped)
        
        book_data.book_id = book_data.isbn

        book_data.site_slug = "TB"

        book_data.url = convert_book_id_to_url(book_data.book_id)
        book_data.content = queryHtml(root, "/html")

        book_data.ready_for_sale = queryHtml(root, ".//i/@class")
        if(book_data.ready_for_sale == "fa fa-times-circle x-mark"):
            book_data.ready_for_sale = False
        else: 
            book_data.ready_for_sale = True

        book_data.extra = {"price" : queryHtml(root, ".//span[@id='price']").text, "releaseDate" : queryHtml(root, ".//span[@id='release_date']").text}
    
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
        links += testBookStoreLinkSearch(book_data.authors)

    if book_data.isbn_13 != None: # If a title is sent in to search by, record link matches
        links += testBookStoreLinkSearch(book_data.isbn)

    if book_data.title != None: # If a title is sent in to search by, record link matches
        links += testBookStoreLinkSearch(book_data.title)
    
    linksNoDuplicates = [] 
    for i in links: 
        if i not in linksNoDuplicates: 
            linksNoDuplicates.append(i) #removes duplicate links from list
    # FINISH -> LINKS HAS ALL LINKS WITH ANY MATCHING

     # For each link, get the book data and compare it with the passed in book_data
    return get_matches_from_links(get_book_data, linksNoDuplicates, book_data)



"""Given a book_id, return the direct url for the book.""" 
def convert_book_id_to_url(book_id):
    # type: (str) -> str
    return "http://localhost:8000/library/" + book_id + "/"
    print("Convert book id function from TestBookstore")