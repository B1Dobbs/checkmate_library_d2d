from BookData import BookData
from lxml import etree
from BookSite.common.utils import *
import sys

"""Given a direct link to a book page at a site, parse it and return the SiteBookData of the info""" 
def get_book_data(url):
    book_data = BookData()
    root = get_root_from_url(url)

    try:
        title = str.strip(queryHtml(root, ".//span[@class='title product-field']").text)
        if ":" in title:
            title_array = title.split(":")
            book_data.title = title_array[0]
            book_data.subtitle = str.strip(title_array[1])
        else:
            book_data.title = title

        book_data.image_url = "https:" + queryHtml(root, ".//div[@class='item-image']//img/@src")[0]
        book_data.image = get_image_from_url(book_data.image_url)
        book_data.isbn = queryHtml(root, ".//li[contains(text(), 'ISBN')]/span").text
        book_data.description = queryHtml(root, ".//div[@class='synopsis-description']/descendant::*/text()")
        series_info = queryHtml(root, ".//span[@class='product-sequence-field']/a[1]")
        if(series_info is not None):
            series_info = series_info.text.split("#")
            book_data.series = series_info[0]
            if(len(series_info) > 1):
                book_data.vol_number = series_info[1]


        book_data.authors = queryHtml(root, ".//a[@class='contributor-name']/text()")
        book_data.ready_for_sale = True
        book_data.site_slug = "KB"

        book_id = str(queryHtml(root, ".//link[@rel='canonical']/@href"))
        book_data.book_id = book_id.split("/")[-1]

        book_data.url = "https://www.kobo.com/us/en/ebook/" + book_data.book_id
        book_data.extra = {"Price" : queryHtml(root, ".//div[@class='price-wrapper']/span")[0].text, "Release Date" : queryHtml(root, ".//div[@class='bookitem-secondary-metadata']/ul[1]/li[2]/span[1]").text}
        book_data.content = queryHtml(root, "/html")

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
    if book_data.authors != None: # If an author is sent in to search by, record link matches
        links += koboLinkSearch(book_data.authors)
        
    if book_data.isbn != None: # If an isbn is sent in to search by, record link matches
        links += koboLinkSearch(book_data.isbn)
        
    if book_data.title != None: # If a title is sent in to search by, record link matches
        links += koboLinkSearch(book_data.title)
    
    if book_data.series != None: # If a title is sent in to search by, record link matches
        links += koboLinkSearch(book_data.series)
        
    linksNoDuplicates = [] 
    for i in links: 
        if i not in linksNoDuplicates: 
            linksNoDuplicates.append(i) #removes duplicate links from list
    # FINISH -> LINKS HAS ALL LINKS WITH ANY MATCHING

    book_matches = []
    for lnk in linksNoDuplicates:
        search_book_data = get_book_data(lnk)
        book_matches.append(search_book_data)
        search_book_data.printData()
    return book_matches



"""Given a book_id, return the direct url for the book.""" 
def convert_book_id_to_url(book_id):
    # type: (str) -> str 
    print("Convert book id function from Kobo")