
import unittest
import sys
sys.path.append(".")
from Checkmate import get_book_site
  

class BaseBookParseTest(unittest.TestCase): 

    def set_none_fields(self, book_data, fields=['description','image','content']):
        for field in fields:
            book_data[field] = None

    def common_test(self, local_url, test_case, parser):
        expected_data = test_case
        returned_book = parser.get_book_data(local_url)

        # returned_book.print_data()
        # print("EXPECTED: ", expected_data)
        self.assertTrue(test_case['description'] in returned_book.description)
        test_case['description'] = None

        self.assertTrue(returned_book.content != None)
        self.assertTrue(returned_book.image != None)
        self.set_none_fields(returned_book.data, ['description','image', 'content'])
        
        self.assertEqual(returned_book.data, expected_data)

