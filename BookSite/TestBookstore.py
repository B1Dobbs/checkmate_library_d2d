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

    try:
        book_data.subtitle = root.xpath(".//p[@id='title']/strong")[0].text.split(": ")[1]
    except:
        book_data.subtitle = "None"
    
    book_data.authors = root.xpath(".//span[@id='author']")[0].text
    book_data.authors = str.strip(book_data.authors)
    
    book_data.book_id = root.xpath(".//span[@id='book_id']")[0].text
    book_data.book_id = str.strip(book_data.book_id)

    book_data.site_slug = root.xpath("//head/title")[0].text
    if(book_data.site_slug == "Test Bookstore"):
        book_data.site_slug = "TB"

    book_data.url = convert_book_id_to_url(book_data.book_id)
    #book_data.content

    # aria-hidden:true keeps me from getting the value
    book_data.ready_for_sale = (root.xpath(".//i[@class='fas fa-check-circle check']"))[0].get("aria-hidden")
    book_data.extra = {"price" : root.xpath(".//span[@id='price']")[0].text, "releaseDate" : root.xpath(".//span[@id='release_date']")[0].text}

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
    return "http://localhost:8000/library/" + book_id + "/"
    print("Convert book id function from TestBookstore")