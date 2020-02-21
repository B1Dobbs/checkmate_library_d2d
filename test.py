from Checkmate import *

def testBookstore():
    book_site = get_book_site("http://127.0.0.1:8000/library/")
    book_site.get_book_data("http://127.0.0.1:8000/library/9781524243456/")


if __name__ == "__main__":
    testBookstore()