from BookSite import GoogleBooks, Kobo, LibrariaCultura, Scribd, TestBookstore

def get_book_site(slug):
    print("Will return one of the BookSite modules")

class BookData:
    #put attributes here

    def __init__(self):
        print("Will set default data if needed")

    def __str__(self):
        print("Relative infomation about the book")
