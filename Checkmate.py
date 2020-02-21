from BookSite import GoogleBooks, Kobo, LibrariaCultura, Scribd, TestBookstore

def get_book_site(slug):
    print("Will return one of the BookSite modules")
    if "google" in slug:
        return GoogleBooks
    elif "kobo" in slug:
        return Kobo
    elif "librariacultura" in slug:
        return LibrariaCultura
    elif "scribd" in slug:
        return Scribd
    elif "testBookstore" in slug:
        return TestBookstore

class BookData:
    #put attributes here

    def __init__(self):
        print("Will set default data if needed")

    def __str__(self):
        print("Relative infomation about the book")
