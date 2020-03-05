from BookData import BookData
from lxml import etree
from BookSite.common.utils import *
import sys, traceback

"""Given a direct link to a book page at a site, parse it and return the SiteBookData of the info""" 
def get_book_data(url):
    book_data = BookData()
    root = get_root_from_url(url)

    book_data.format = "Digital"

    try:
        title = str.strip(queryHtml(root, ".//span[@class='title product-field']").text)
        if ":" in title:
            title_array = title.split(":")
            book_data.title = title_array[0]
            book_data.subtitle = str.strip(title_array[1])
        else:
            book_data.title = title

        image_url = queryHtml(root, ".//div[@class='item-image']//img/@src")
        if(type(image_url) == list):
            book_data.image_url = "https:" + queryHtml(root, ".//div[@class='item-image']//img/@src")[0]
        else:
            book_data.image_url = "https:" + queryHtml(root, ".//div[@class='item-image']//img/@src")

        book_data.image = get_image_from_url(book_data.image_url)
        book_data.isbn_13 = queryHtml(root, ".//li[contains(text(), 'ISBN')]/span").text

        book_data.description = " "
        description = queryHtml(root, ".//div[@class='synopsis-description']/descendant-or-self::*/text()")
        if description != None:
            for string in description:   
                book_data.description += string

        series_info = queryHtml(root, ".//span[@class='product-sequence-field']/a[1]")
        if(series_info is not None):
            series_info = series_info.text.split("#")
            book_data.series = series_info[0]
            if(len(series_info) > 1):
                book_data.vol_number = series_info[1]


        authors = queryHtml(root, ".//a[@class='contributor-name']/text()")
        if authors != None:
            if(type(authors) == list):
                book_data.authors += authors
            else:
                book_data.authors.append(authors)

        book_data.ready_for_sale = True
        book_data.site_slug = "KB"

        book_id = str(queryHtml(root, ".//link[@rel='canonical']/@href"))
        book_data.book_id = book_id.split("/")[-1]

        book_data.url = "https://www.kobo.com/us/en/ebook/" + book_data.book_id

        try:
            price = queryHtml(root, ".//div[@class='price-wrapper']/span")[0].text
        except:
            price = 0.0
        book_data.extra = {"Price" : price, "Release Date" : queryHtml(root, ".//div[@class='bookitem-secondary-metadata']/ul[1]/li[2]/span[1]").text}
        book_data.content = queryHtml(root, "/html")

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
        links += koboLinkSearch(book_data.isbn_13)

    if(titleLinkSearch != ""):
        links += koboLinkSearch(titleLinkSearch)
        
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
        #search_book_data.printData()
        #print("MATCH: ", match_value)
        if(match_value != 0.0):
            book_matches.append((match_value, search_book_data))
        
    return book_matches



"""Given a book_id, return the direct url for the book.""" 
def convert_book_id_to_url(book_id):
    # type: (str) -> str 
    print("Convert book id function from Kobo")