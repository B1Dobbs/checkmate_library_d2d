from BookData import BookData
from lxml import etree
import io
import requests, sys, webbrowser, bs4
from PIL import Image
from BookSite.common.utils import *
from Checkmate import *

    
def testSiteQuery(book_site):
    book_data = BookData()
    book_data.authors = ["vergara"]
    print(book_site.find_book_matches(book_data))
    

if __name__ == "__main__":

    if sys.argv[1] != None and sys.argv[1] not in siteSlugs:
        print("Site slug not found.")
    else:
        testToRun = sys.argv[1]

        """ Site Query Test for Scribd """
        if testToRun == "SD" or testToRun == None:
            print("Starting test for Scribd.")
            testSiteQuery(get_book_site("SD"))

        """ Site Query Test for Kobo """
        if testToRun == "KB" or testToRun == None:
            print("Starting test for Kobo.")
            testSiteQuery(get_book_site("KB"))

        """ Site Query Test for Google """
        if testToRun == "GB" or testToRun == None:
            print("Starting test for Google Books.")
            testSiteQuery(get_book_site("GB"))

        """ Site Query Test for Livraria Cultura """
        if testToRun == "LC" or testToRun == None:
            print("Starting test for Livraria Cultura.")
            testSiteQuery(get_book_site("KB"))

        """ Site Query Test for Test Bookstore """
        if testToRun == "TB" or testToRun == None:
            print("Starting test for Test Bookstore.")
            testSiteQuery(get_book_site("TB"))
