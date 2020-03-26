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

""" Needed for test clases """
siteSlugs = ["GB", "KB", "LC", "SD", "TB"]

def get_book_site(slug):
    """Will return one of the BookSite modules"""
    if slug == "GB":
        return GoogleBooks()
    elif slug == "KB":
        return Kobo()
    elif slug == "LC":
        return LivrariaCultura()
    elif slug == "SD":
        return Scribd()
    elif slug == "TB":
        return TestBookstore()
    else:
        print("Site Slug not found.")
    
