from BookData import BookData
from lxml import etree
import io
import requests
from PIL import Image

"""Can propably be moved to common utils"""
def get_image_from_url(element):
    image_response = requests.get(element)
    img = Image.open(io.BytesIO(image_response.content))
    return img

"""Can propably be moved to common utils"""
def get_root_from_url(url):
    content = requests.get(url).content
    parser = etree.HTMLParser(remove_pis=True)
    tree = etree.parse(io.BytesIO(content), parser)
    root = tree.getroot()
    return root

"""Given a direct link to a book page at a site, parse it and return the SiteBookData of the info""" 
def get_book_data(url):
    book_data = BookData()

    root = get_root_from_url(url)

    book_data.format = root.xpath(".//p[@class='details']")[0].text
    book_data.title = root.xpath(".//p[@id='title']/strong")[0].text

    """Will work if you add an image to testbook store description page """
    #book_data.image_url = root.xpath(".//img/@src")[0]
    #book_data.image = get_image_from_url(book_data.image_url)

    book_data.isbn = root.xpath(".//span[@id='isbn']")[0].text
    book_data.description = root.xpath("//script[@type='text/javascript']/text()")[0].split("\"")[19]

    book_data.series = root.xpath(".//span[@id='series']")[0].text
    book_data.vol_number = root.xpath(".//span[@id='volume_number']")[0].text

    return book_data


"""Given a SiteBookData, search for the book at the `book_site` site
and provide a list of likely matches paired with how good
of a match it is (1.0 is an exact match). 
This should take into account all the info we have about a book, 
including the cover.""" 
def find_book_matches(book_data):
    # type: (SiteBookData) -> List[Tuple[SiteBookData, float]] 
    print("Find book matches function from TestBookstore")


"""Given a book_id, return the direct url for the book.""" 
def convert_book_id_to_url(book_id):
    # type: (str) -> str 
    print("Convert book id function from TestBookstore")