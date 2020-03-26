from BookSite.common.utils import *
from BookData import BookData
from lxml import etree
import sys, traceback

class BookSite:

######################################################
    def __init__(self):
        pass

######################################################
    def get_book_data(self, url):
        # type: (str) -> SiteBookData 
        book_data = BookData()
        book_data.url = url
        book_data.ready_for_sale = True
        book_data.format = "Digital"
        book_data.parse_status = "Successful"
        
        try:
            root = get_root_from_url(url)
            book_data = self.get_site_specific_data(root, book_data)
            
        except requests.exceptions.ConnectionError:
            print("ERROR: Could not connect to url ", url)
            book_data.parse_status = "UNSUCCESSFUL"
        except:
            print("ERROR: Processing book at " + url)
            traceback.print_exc()

        return book_data

######################################################
    def get_site_specific_data(self):
        pass

######################################################
    def find_book_matches(self, book_data):
        """Given a SiteBookData, search for the book at the `book_site` site
        and provide a list of likely matches paired with how good
        of a match it is (1.0 is an exact match). 
        This should take into account all the info we have about a book, 
        including the cover.""" 
        links = set(self.get_site_links(book_data))
        print(links)
        return get_matches_from_links(self.get_book_data, links, book_data)

######################################################
    def found_enough_matches(self, matches):
        hasGoodMatch = False
        for match in matches:
            if match[0] > 0.7 :
                hasGoodMatch = True
                break
        
        if hasGoodMatch and len(matches >= 30):
            return True
        else:
            return False

######################################################
    def get_site_links(self):
        pass

######################################################
    def convert_book_id_to_url(self, book_id):
        """Given a book_id, return the direct url for the book.""" 
        pass

    


