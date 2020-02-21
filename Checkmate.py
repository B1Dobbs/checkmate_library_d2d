from BookSite import GoogleBooks, Kobo, LibrariaCultura, Scribd, TestBookstore

"""
TB - TestBookstore
KB - Kobo
GB - Google Books
SD - Scribd
LC - LibrariaCultura
 """
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
    elif "library" in slug:
        return TestBookstore
