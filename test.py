from Checkmate import *
from BookSite.common.utils import *
from BookData import BookData

def testBookstore():
    book_site = get_book_site("TB")
    #book_data = book_site.get_book_data("http://localhost:8000/library/1565112531635/")
    #Didn't have that book in my testBookStore
    book_data = book_site.get_book_data("http://localhost:8000/library/9781386820031/")
    book_data.printData()
    book_data2 = BookData()
    #book_data2.title = '10 Steps'
    book_data2.authors = ['Sasha']
    book_data.authors = ['Sacha Black', 'Ben']
    print(compare_book_data(book_data, book_data2))

def testKobo():
    book_site = get_book_site("KB")
    book_data = book_site.get_book_data("https://www.kobo.com/us/en/ebook/the-target-3")
    book_data.printData()


if __name__ == "__main__":
    #testBookstore()
    testKobo()