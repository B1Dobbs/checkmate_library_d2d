from BookData import BookData
from lxml import etree
from BookSite.common.utils import *
import requests, sys, webbrowser, bs4

from BookSite import book_site

class TestBookstore(book_site.BookSite):
        
    """Given a direct link to a book page at a site, parse it and return the SiteBookData of the info""" 
    def get_site_specific_data(self, root, book_data):
        book_data.site_slug = "TB"

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

        book_data.isbn_13 = str.strip(queryHtml(root, ".//span[@id='isbn']").text)
        book_data.description = queryHtml(root, "//script[@type='text/javascript']/text()").split("\"")[19]

        book_data.series = str.strip(queryHtml(root, ".//span[@id='series']").text)
        book_data.vol_number = str.strip(queryHtml(root, ".//span[@id='volume_number']").text)
        
        book_data.authors = str.strip(queryHtml(root, ".//span[@id='author']/text()")).split(", ")
        
        book_data.book_id = book_data.isbn_13
        book_data.content = queryHtml(root, "/html")

        book_data.ready_for_sale = queryHtml(root, ".//i/@class")
        if book_data.ready_for_sale == "fa fa-times-circle x-mark":
            book_data.ready_for_sale = False
        else: 
            book_data.ready_for_sale = True

        book_data.extra = {"price" : queryHtml(root, ".//span[@id='price']").text, "releaseDate" : queryHtml(root, ".//span[@id='release_date']").text}

        return book_data


    """Given a SiteBookData, search for the book at the `book_site` site
    and provide a list of likely matches paired with how good
    of a match it is (1.0 is an exact match). 
    This should take into account all the info we have about a book, 
    including the cover.""" 
    def get_site_links(self, book_data):

        links = []

        if book_data.authors != None: # If an author is sent in to search by, record link matches
            links += self.testBookStoreLinkSearch(book_data.get_authors_as_string())

        if book_data.isbn_13 != None: # If an isbn is sent in to search by, record link matches
            links += self.testBookStoreLinkSearch(book_data.isbn_13)

        if book_data.title != None: # If a title is sent in to search by, record link matches
            links += self.testBookStoreLinkSearch(book_data.title)

        # For each link, get the book data and compare it with the passed in book_data
        return links

    """ Search test Book Store for relevant links """
    def testBookStoreLinkSearch(self, searchVar):
        links = []
        link = 'http://127.0.0.1:8000/testBookstore/library/?q=' + searchVar
        res = requests.get(link)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, "html.parser")

        for link in soup.find_all('a', class_="book_title"):
            links.append("http://127.0.0.1:8000/testBookstore" + link.get('href'))

        pattern = re.compile(r'Last')
        findPageNum = str(soup.find('a', text=pattern))
        if findPageNum != "None":
            temp = re.findall(r'\d+', findPageNum)
            num_pages = temp[0]
        
            for i in range(2, int(num_pages)+1):
                link = 'http://127.0.0.1:8000/testBookstore/library/?page=' + str(i)
                res = requests.get(link)
                res.raise_for_status()
                soup = bs4.BeautifulSoup(res.text, "html.parser")

                for link in soup.find_all('a', class_="book_title"):
                    links.append("http://127.0.0.1:8000/testBookstore" + link.get('href')) 

        
        return links 




    """Given a book_id, return the direct url for the book.""" 
    def convert_book_id_to_url(self, book_id):
        # type: (str) -> str
        return "http://localhost:8000/library/" + book_id + "/"