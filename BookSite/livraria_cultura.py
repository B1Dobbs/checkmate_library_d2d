from BookData import BookData
from lxml import etree
from BookSite.common.utils import *
import requests, sys, webbrowser, bs4
from BookSite import book_site

class LivrariaCultura(book_site.BookSite):
    
    """Given a direct link to a book page at a site, parse it and return the SiteBookData of the info""" 
    def get_site_specific_data(self, root, book_data):
        book_data.site_slug = "LC"

        title = queryHtml(root, ".//meta[@property='og:title']/@content")
        book_data.title = str(title)

        subtitle = queryHtml(root, ".//th[contains(text(), 'Subtitulo')]/following-sibling::td")
        if(subtitle is not None):
            book_data.subtitle = subtitle.text

        imageUrl = queryHtml(root, ".//meta[@itemprop='image']/@content")
        book_data.image_url = str(imageUrl)
        book_data.image = get_image_from_url(book_data.image_url)

        book_data.isbn_13 = queryHtml(root, ".//th[contains(text(), 'ISBN')]/following-sibling::td").text
        book_data.description = str(queryHtml(root, ".//meta[@property='og:title']/following-sibling::meta[@property='og:description']/@content"))

        #Series and Volume Number are not available on site

        authorsTag = queryHtml(root, ".//th[contains(text(), 'Colaborado')]/following-sibling::td").text

        #Parsing Author Name
        collaborators = authorsTag.split("|")
        matchingAuthor = [s for s in collaborators if "Autor" in s]
        authorsArray = []

        for a in matchingAuthor:
            authorsNamesString = a.split(":")
            authorsNamesArray = authorsNamesString[1].split(",")
            authorsArray.append(authorsNamesArray[1].strip() + " " + authorsNamesArray[0].strip())
        
        book_data.authors = authorsArray

        bookURL = str(queryHtml(root, ".//meta[@itemprop='url']/@content"))
        bookID = bookURL.split('.br')
        book_data.book_id = bookID[1]
        book_data.content = queryHtml(root, "/html")

        #Price is gathered as extra data
        book_data.extra = {"price" : str(queryHtml(root, ".//meta[@property='product:price:amount']/@content"))}

        return book_data

    """Given a SiteBookData, search for the book at the `book_site` site
    and provide a list of likely matches paired with how good
    of a match it is (1.0 is an exact match). 
    This should take into account all the info we have about a book, 
    including the cover.""" 
    def get_site_links(self, book_data):
        links = []
        if book_data.authors != None: # If a title is sent in to search by, record link matches
            links += livrariaLinkSearch(book_data.get_authors_as_string())

        if book_data.isbn_13 != None: # If a title is sent in to search by, record link matches
            links += livrariaLinkSearch(book_data.isbn_13)

        if book_data.title != None: # If a title is sent in to search by, record link matches
            links += livrariaLinkSearch(book_data.title)
            
        return links

    def livrariaLinkSearch(self, searchVar):
        links = []
        link = 'https://www3.livrariacultura.com.br/ebooks/?ft=' + searchVar
        res = requests.get(link)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, "html.parser")

        for div in soup.find_all('div', class_="prateleiraProduto__informacao__preco"):
            for a in div.find_all('a'):
                links.append(a.get('href'))

        #This code is supposed to paginate, but for some reason libraria's pagination links don't work at all.
        # First get the number of books
        storageSpan = soup.find('span', class_="resultado-busca-numero")
        numBooksSpan = storageSpan.find('span', class_="value")
        numBooks = int(numBooksSpan.contents[0])

        booksPerPagesOption = soup.find('option', attrs={"selected" : "selected"})
        booksPerPages = int(booksPerPagesOption.contents[0])
        
        numPages = numBooks/booksPerPages

        
        if(numPages > 1):
            for i in range(2, int(numPages)):
                link = 'https://www3.livrariacultura.com.br/ebooks/?ft=' + searchVar + '#' + str(i)
                print(link)
                res = requests.get(link)
                res.raise_for_status()
                soup = bs4.BeautifulSoup(res.text, "html.parser")

                for div in soup.find_all('div', class_="prateleiraProduto__informacao__preco"):
                    for a in div.find_all('a'):                 
                        links.append(a.get('href'))


        return links


    """Given a book_id, return the direct url for the book.""" 
    def convert_book_id_to_url(self, book_id):
        # type: (str) -> str 
        return "https://www3.livrariacultura.com.br" + book_id