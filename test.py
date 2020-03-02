from Checkmate import *

def testBookstore():
    book_site = get_book_site("TB")
    #book_data = book_site.get_book_data("http://localhost:8000/library/1565112531635/")
    #Didn't have that book in my testBookStore
    book_data = book_site.get_book_data("http://127.0.0.1:8000/library/9781524243456/")
    book_data.printData()

def testKobo():
    book_site = get_book_site("KB")
    book_data = book_site.get_book_data("https://www.kobo.com/us/en/ebook/the-alchemist-38")
    book_data.printData()

# def testGoogle():
#     book_site = get_book_site("GB")
#     book_data = book_site.get_book_data("https://books.google.com/books?id=5iTebBW-w7QC")
#     book_data.printData()


if __name__ == "__main__":
    testBookstore()
    #testKobo()