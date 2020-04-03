import unittest
import sys
from scribd.scribd_book_data import TestScribdBookDataLocal, TestScribdBookDataLive
from google_books.google_book_data import TestGoogleBookDataLocal, TestGoogleBookDataLive
from kobo.kobo_book_data import TestKoboBookDataLocal, TestKoboBookDataLive
from BookSite.google_books import GoogleBooks
from BookSite.kobo import Kobo
from BookSite.livraria_cultura import LivrariaCultura
from BookSite.scribd import Scribd
from BookSite.test_bookstore import TestBookstore

def load_local_tests(loader, slugs):
    tests = []

    if Scribd.SLUG in slugs or slugs == None:
        tests += loader.loadTestsFromTestCase(TestScribdBookDataLocal)
    if GoogleBooks.SLUG in slugs or slugs == None:
        tests += loader.loadTestsFromTestCase(TestGoogleBookDataLocal)
    if Kobo.SLUG in slugs or slugs == None:
        tests += loader.loadTestsFromTestCase(TestKoboBookDataLocal)
    return tests

def load_live_tests(loader, slugs):
    tests = []

    if Scribd.SLUG in slugs or slugs == None:
        tests += loader.loadTestsFromTestCase(TestScribdBookDataLive)
    if GoogleBooks.SLUG in slugs or slugs == None:
        tests += loader.loadTestsFromTestCase(TestGoogleBookDataLive)
    if Kobo.SLUG in slugs or slugs == None:
        tests += loader.loadTestsFromTestCase(TestKoboBookDataLive)
    return tests


#https://stackoverflow.com/questions/5360833/how-to-run-multiple-classes-in-single-test-suite-in-python-unit-testing/16823869
if __name__ == '__main__':
    # Run only the tests in the specified classes

    #test_classes_to_run = [TestScribdBookDataLocal]

    loader = unittest.TestLoader()
    suite  = unittest.TestSuite()

    tests = load_live_tests(loader, {Kobo.SLUG})
    tests += load_local_tests(loader, {Kobo.SLUG})

    suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=3)
    result = runner.run(suite)

    # suites_list = []
    # for test_class in test_classes_to_run:
    #     suite = loader.loadTestsFromTestCase(test_class)
    #     suites_list.append(suite)

    # big_suite = unittest.TestSuite(suites_list)

    # runner = unittest.TextTestRunner()
    # results = runner.run(big_suite)