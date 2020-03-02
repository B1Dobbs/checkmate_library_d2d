from Checkmate import *

def testBookstore():
    book_site = get_book_site("TB")
    #book_data = book_site.get_book_data("http://localhost:8000/library/1565112531635/")
    #Didn't have that book in my testBookStore
    book_data = book_site.get_book_data("http://localhost:8000/library/9781386820031/")
    book_data.printData()

def testKobo():
    book_site = get_book_site("KB")
    book_data = book_site.get_book_data("https://www.kobo.com/us/en/ebook/the-target-3")
    book_data.printData()

def testLivrariaCultura():
    book_site = get_book_site("LC")
    book_data = book_site.get_book_data("https://www3.livrariacultura.com.br/what-if-its-us-2012739487/p")
    book_data.printData()


if __name__ == "__main__":
    testBookstore()
    testKobo()
    testLivrariaCultura()