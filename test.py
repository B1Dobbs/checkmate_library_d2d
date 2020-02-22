from Checkmate import *

def testBookstore():
    book_site = get_book_site("TB")
    book_data = book_site.get_book_data("http://localhost:8000/library/1565112531635/")
    # Didn't have that book in my testBookStore
    #book_data = book_site.get_book_data("http://127.0.0.1:8000/library/9781524243456/")
    print(book_data.format)
    print(book_data.title)
    #print(book_data.image_url)
    print(book_data.isbn)
    print(book_data.description)
    print(book_data.series)
    print(book_data.vol_number)
    print(book_data.authors)
    print(book_data.ready_for_sale)
    print(book_data.site_slug)
    print(book_data.subtitle)
    print(book_data.book_id)
    print(book_data.url)
    print(book_data.extra)


if __name__ == "__main__":
    testBookstore()