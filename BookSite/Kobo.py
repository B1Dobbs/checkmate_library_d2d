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
        book_data.image_url = "https:" + queryHtml(root, ".//div[@class='item-image']//img/@src")[0]
        book_data.image = get_image_from_url(book_data.image_url)
        book_data.isbn = queryHtml(root, ".//li[contains(text(), 'ISBN')]/span").text
        book_data.description = queryHtml(root, ".//div[@class='synopsis-description']/descendant::*/text()")
        series_info = queryHtml(root, ".//span[@class='product-sequence-field']/a[1]")
        if(series_info is not None):
            series_info = series_info.text.split("#")
            book_data.series = series_info[0]
            book_data.vol_number = series_info[1]

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
    # type: (SiteBookData) -> List[Tuple[SiteBookData, float]] 
    print("Find book matches function from Kobo")


"""Given a book_id, return the direct url for the book.""" 
def convert_book_id_to_url(book_id):
    # type: (str) -> str 
    print("Convert book id function from Kobo")