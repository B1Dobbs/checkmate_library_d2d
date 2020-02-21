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
    if slug is "GB":
        return GoogleBooks
    elif slug is "KB":
        return Kobo
    elif slug is "LB":
        return LibrariaCultura
    elif slug is "SB":
        return Scribd
    elif slug is "TB":
        return TestBookstore
