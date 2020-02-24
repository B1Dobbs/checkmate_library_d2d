from BookSite import GoogleBooks, Kobo, LibrariaCultura, Scribd, TestBookstore

"""
TB - TestBookstore
KB - Kobo
GB - Google Books
SD - Scribd
LC - LibrariaCultura
 """
def get_book_site(slug):
    """Will return one of the BookSite modules"""
    if slug == "GB":
        return GoogleBooks
    elif slug == "KB":
        return Kobo
    elif slug == "LB":
        return LibrariaCultura
    elif slug == "SB":
        return Scribd
    elif slug == "TB":
        return TestBookstore
