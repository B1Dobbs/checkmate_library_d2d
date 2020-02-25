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

        book_data.image_url = "https:" + queryHtml(root, ".//div[@class='item-image']//img/@src")
        book_data.image = get_image_from_url(book_data.image_url)


        book_data.authors = queryHtml(root, ".//a[@class='contributor-name']").text
        book_data.ready_for_sale = True
        book_data.site_slug = "KB"

        book_id = str(queryHtml(root, ".//link[@rel='canonical']/@href"))
        book_data.book_id = book_id.split("/")[-1]

        book_data.url = convert_book_id_to_url(book_data.book_id)
        book_data.extra = {"Price" : queryHtml(root, ".//div[@class='price-wrapper']/span").text, "Release Date" : queryHtml(root, ".//div[@class='bookitem-secondary-metadata']/ul[1]/li[2]/span[1]").text}
        book_data.content = queryHtml(root, "/html")

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
    return "https://www.kobo.com/us/en/ebook/" + book_id
    print("Convert book id function from Kobo")