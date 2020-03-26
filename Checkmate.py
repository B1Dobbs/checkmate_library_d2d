from BookSite.google_books import GoogleBooks
from BookSite.kobo import Kobo
from BookSite.livraria_cultura import LivrariaCultura
from BookSite.scribd import Scribd
from BookSite.test_bookstore import TestBookstore
"""
TB - TestBookstore
KB - Kobo
GB - Google Books
SD - Scribd
LC - LibrariaCultura
 """


def get_book_site(slug):
    """Will return one of the BookSite modules"""
    if slug == GoogleBooks.SLUG:
        return GoogleBooks()
    elif slug == Kobo.SLUG:
        return Kobo()
    elif slug == LivrariaCultura.SLUG:
        return LivrariaCultura()
    elif slug == Scribd.SLUG:
        return Scribd()
    elif slug == TestBookstore.SLUG:
        return TestBookstore()
    else:
        print("Site Slug not found.")
    
