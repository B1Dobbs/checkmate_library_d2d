from BookData import BookData
from BookSite.common.utils import query_html
from BookSite import base_parser
import requests

class GoogleBooks(base_parser.BookSite):

    SLUG = "GB"
    
    """Given a direct link to a book page at a site, parse it and return the BookData of the info"""
    def get_site_specific_data(self, root, book_data):
        title = str.strip(query_html(root, "//h1[@class='AHFaub']/span").text)
        if ":" in title:
            title_array = title.split(":")
            book_data.title = title_array[0]
            book_data.subtitle = title_array[1]
        else:
            book_data.title=title   

        book_data.image_url = query_html(root, "//meta[@property='og:image']/@content")
        book_data.isbn_13 = query_html(root, "//div[@class='IQ1z0d']/span")[3].text

        book_description =  query_html(root, "//meta[@itemprop='description']/@content")
        if type(book_description)==list:
            book_data.description = book_description[1]
        series_info = query_html(root, "//div[@class='sIskre']/h2")
        if series_info is not None:
            book_data.series = query_html(root, "//div[@class='sIskre']/h2").text
            book_data.vol_number = query_html(root, "//div[@class='j15tgb']").text

        authors = query_html(root, "//span[@itemprop='author']/a/text()")
        if authors != None:
            if type(authors)==list:
                book_data.authors += authors
            else:
                book_data.authors.append(authors)
        else:
            book_data.authors = None

        book_id = str(query_html(root, "//link[@rel='canonical']/@href"))
        book_data.book_id = book_id.split("=")[1]
        try:
            price = query_html(root, "//meta[@itemprop='price']/@content")[1]
        except:
            price = 0.0

        book_data.extra = {"Price" : price}
        book_data.content = query_html(root, "/html")

        return book_data

    def get_site_links(self, book_data):
        links = []

        if book_data.authors != None: # If a title is sent in to search by, record link matches
            links += self.get_links_for_search(book_data.get_authors_as_string())

        if book_data.isbn_13 != None: # If a title is sent in to search by, record link matches
            links += self.get_links_for_search(book_data.isbn_13)

        if book_data.title != None: # If a title is sent in to search by, record link matches
            links += self.get_links_for_search(book_data.title)
            
        return links

    def get_links_for_search(self, search_str):
        links = []
        link = 'https://www.googleapis.com/books/v1/volumes?q=' + search_str + '&filter=ebooks&key=AIzaSyCAFFlw7GGtYtnOwN7MZpHMaK_qq11GxdA&maxResults=40'
        api_response = requests.get(link)

        for item in api_response.json()['items']:
            links.append(item['volumeInfo']['infoLink'])
            if self.found_enough_matches(links):
                break
    
        return links


    """Given a book_id, return the direct url for the book.""" 
    def convert_book_id_to_url(self, book_id):
        return "https://play.google.com/store/books/details/?id=" + book_id
