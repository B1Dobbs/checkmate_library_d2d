from BookSite import GoogleBooks, Kobo, LibrariaCultura, Scribd, TestBookstore

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
        return GoogleBooks
    elif slug == "KB":
        return Kobo
    elif slug == "LC":
        return LibrariaCultura
    elif slug == "SD":
        return Scribd
    elif slug == "TB":
        return TestBookstore
    else:
        print("Site Slug not found.")
    
