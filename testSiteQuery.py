#from book_data import BookData, Format
import sys
sys.path.append(".")
from book_site.scribd import Scribd
from checkmate import get_book_site

    
def testSiteQuery(book_site):
    # book_data = BookData()
    # book_data.format = Format.DIGITAL
    # book_data.authors = ["vergara"]
    # book_site.find_book_matches(book_data)
    print(dir(book_site))
    print(book_site.get_links_for_page("test/scribd/test_pages/search_audiobooks.html", 'audiobooks'))
    

if __name__ == "__main__":

    testToRun = sys.argv[1]

    """ Site Query Test for Scribd """
    if testToRun == Scribd.SLUG or testToRun == None:
        print("Starting test for Scribd.")
        testSiteQuery(get_book_site("SD"))