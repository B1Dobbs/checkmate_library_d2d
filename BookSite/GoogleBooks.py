from BookData import BookData
from lxml import etree
from BookSite.common.utils import *
import sys


"""Given a direct link to a book page at a site, parse it and return the SiteBookData of the info""" 
def get_book_data(url):
    book_data = BookData()
    root = get_root_from_url(url)
    
    try:
        title = str.strip(queryHtml(root, "//h1[@class='AHFaub']/span").text)
        book_data.title = title  
        book_data.format = "E-Book"     

        book_data.image_url = queryHtml(root, "//meta[@property='og:image']/@content")
        book_data.image = get_image_from_url(book_data.image_url)
        book_data.isbn = queryHtml(root, "//div[@class='IQ1z0d']/span")[3].text
        book_data.description = queryHtml(root, "//meta[@itemprop='description']/@content")[1]
        series_info = queryHtml(root, "//div[@class='sIskre']/h2")
        if(series_info is not None):
            book_data.series = queryHtml(root, "//div[@class='sIskre']/h2").text
            book_data.vol_number = queryHtml(root, "//div[@class='j15tgb']").text

        book_data.authors = queryHtml(root, "//span[@itemprop='author']/a").text
        book_data.ready_for_sale = True
        book_data.site_slug = "GB"
        book_id = str(queryHtml(root, "//link[@rel='canonical']/@href"))
        book_data.book_id = book_id.split("?")[1]
        book_data.url = convert_book_id_to_url(book_data.book_id)
        book_data.extra = {"Price" : queryHtml(root, "//meta[@itemprop='price']/@content")[1]}
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
    # type: (SiteBookData) -> List[Tuple[SiteBookData, float]] 
    print("Find book matches function from Google")


"""Given a book_id, return the direct url for the book.""" 
def convert_book_id_to_url(book_id):
    # type: (str) -> str 
    return "https://www.play.google.com/store/books/details/?" + book_id
    print("Convert book id function from Google")