from BookData import BookData
from lxml import etree
from BookSite.common.utils import *
import sys, traceback
from BookSite import book_site

class Kobo(book_site.BookSite):

    """Given a direct link to a book page at a site, parse it and return the BookData of the info""" 
    def get_site_specific_data(self, root, book_data):
        title = str.strip(queryHtml(root, ".//span[@class='title product-field']").text)
        subtitle = queryHtml(root, ".//span[@class='subtitle product-field']")
        if ":" in title:
            title_array = title.split(":")
            book_data.title = title_array[0]
            book_data.subtitle = title_array[1]
        elif subtitle != None:
            book_data.subtitle = str.strip(subtitle.text)
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

        book_id = str(queryHtml(root, ".//link[@rel='canonical']/@href"))
        book_data.book_id = book_id.split("/")[-1]

        try:
            price = queryHtml(root, ".//div[@class='active-price']//span[@class='price']")[0].text
        except:
            price = 0.0
        book_data.extra = {"Price" : price, "Release Date" : queryHtml(root, ".//div[@class='bookitem-secondary-metadata']/ul[1]/li[2]/span[1]").text}
        book_data.content = queryHtml(root, "/html")

        return book_data

    """Given a SiteBookData, search for the book at the `book_site` site
    and provide a list of likely matches paired with how good
    of a match it is (1.0 is an exact match). 
    This should take into account all the info we have about a book, 
    including the cover.""" 
    def get_site_links(self, book_data):
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
            links += self.koboLinkSearch(book_data.isbn_13)

        if(titleLinkSearch != ""):
            links += self.koboLinkSearch(titleLinkSearch)
            
        return links

    """ Searching Kobo for relevant links """
    def koboLinkSearch(self, searchVar):
        links = []
        link = 'https://www.kobo.com/us/en/search?query=' + searchVar
        res = requests.get(link)
        res.raise_for_status
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        
        for p in soup.find_all('p', class_="title product-field"):
            for link in p.find_all('a'):
                links.append(link.get('href'))

        aLink = soup.find('a', class_="page-link final") # Find the function by looking for the pattern
        if(aLink != "None"): #There's more than one page
            num_pages = aLink.contents[0]
            num_pages = int(num_pages) + 1
            print(num_pages)
            for i in range(2, num_pages):
                link = 'https://www.kobo.com/us/en/search?query=' + searchVar + '&pageNumber=' + str(i)
                res = requests.get(link)
                res.raise_for_status
                soup = bs4.BeautifulSoup(res.text, "html.parser")

                for p in soup.find_all('p', class_="title product-field"):
                    for link in p.find_all('a'):
                        links.append(link.get('href'))
    
        return links

    """Given a book_id, return the direct url for the book.""" 
    def convert_book_id_to_url(self, book_id):
        # type: (str) -> str 
        return "https://www.kobo.com/us/en/ebook/" + book_id