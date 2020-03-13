from BookData import BookData
from lxml import etree
from BookSite.common.utils import *
import sys, traceback


"""Given a direct link to a book page at a site, parse it and return the SiteBookData of the info""" 
def get_book_data(url):
    # type: (str) -> SiteBookData 
    book_data = BookData()
    book_data.url = url
    book_data.site_slug = "GB"
    
    try:
        root = get_root_from_url(url)

        title = str.strip(queryHtml(root, "//h1[@class='AHFaub']/span").text)
        if ":" in title:
            title_array = title.split(":")
            book_data.title = title_array[0]
            book_data.subtitle = title_array[1]
        else:
            book_data.title=title   

        book_data.image_url = queryHtml(root, "//meta[@property='og:image']/@content")
        book_data.image = get_image_from_url(book_data.image_url)
        book_data.isbn_13 = queryHtml(root, "//div[@class='IQ1z0d']/span")[3].text

        book_description =  queryHtml(root, "//meta[@itemprop='description']/@content")
        if(type(book_description)==list):
            book_data.description = book_description[1]
        series_info = queryHtml(root, "//div[@class='sIskre']/h2")
        if(series_info is not None):
            book_data.series = queryHtml(root, "//div[@class='sIskre']/h2").text
            book_data.vol_number = queryHtml(root, "//div[@class='j15tgb']").text

        authors = queryHtml(root, "//span[@itemprop='author']/a/text()")
        if authors != None:
            if(type(authors)==list):
                book_data.authors += authors
            else:
                book_data.authors.append(authors)
        else:
            book_data.authors = None

        book_id = str(queryHtml(root, "//link[@rel='canonical']/@href"))
        book_data.book_id = book_id.split("=")[1]
        try:
            price = queryHtml(root, "//meta[@itemprop='price']/@content")[0]
        except:
            price = 0.0

        book_data.extra = {"Price" : price}
        book_data.content = queryHtml(root, "/html")

    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to url ", url)
        book_data.parse_status = "UNSUCCESSFUL"
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

    if book_data.authors != None: # If a title is sent in to search by, record link matches
        links += googleLinkSearch(book_data.get_authors_as_string())

    if book_data.isbn_13 != None: # If a title is sent in to search by, record link matches
        links += googleLinkSearch(book_data.isbn_13)

    if book_data.title != None: # If a title is sent in to search by, record link matches
        links += googleLinkSearch(book_data.title)
        
    linksNoDuplicates = [] 
    for i in links: 
        if i not in linksNoDuplicates: 
            linksNoDuplicates.append(i) #removes duplicate links from list
    # FINISH -> LINKS HAS ALL LINKS WITH ANY MATCHING
    
    return get_matches_from_links(get_book_data, linksNoDuplicates, book_data)

def googleLinkSearch(searchVar):
    links = []
    link = 'https://www.googleapis.com/books/v1/volumes?q=' + searchVar + '&filter=ebooks&key=AIzaSyCAFFlw7GGtYtnOwN7MZpHMaK_qq11GxdA&maxResults=40'
    apiResponse = requests.get(link)

    for item in apiResponse.json()['items']:
        links.append(item['volumeInfo']['infoLink'])
       
    return links


"""Given a book_id, return the direct url for the book.""" 
def convert_book_id_to_url(book_id):
    return "https://play.google.com/store/books/details/?id=" + book_id
