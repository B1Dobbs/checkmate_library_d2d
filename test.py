from Checkmate import *
from BookSite.common.utils import *
from BookData import BookData

def testBookstore():
    book_site = get_book_site("TB")
    #book_data = book_site.get_book_data("http://localhost:8000/library/1565112531635/")
    #Didn't have that book in my testBookStore
    book_data = book_site.get_book_data("http://127.0.0.1:8000/library/9781524243456/")
    book_data.printData()

def testKobo():
    book_site = get_book_site("KB")
    book_data = book_site.get_book_data("https://www.kobo.com/us/en/ebook/snow-white-before-the-hea-2")

    book_2 = BookData()
    book_2.authors = ["vergara"]

    print(compare_book_data(book_2, book_data))

def testLivrariaCultura():
    book_site = get_book_site("LC")
    book_data = book_site.get_book_data("https://www3.livrariacultura.com.br/what-if-its-us-2012739487/p")
    book_data.printData()

def testScribd():
    book_site = get_book_site("SD")
    book_data = book_site.get_book_data("https://www.scribd.com/book/445929040/The-Mamba-Mentality-How-I-Play")
    book_data.printData()

if __name__ == "__main__":
    #testBookstore()
    testKobo()
    #testScribd()
