import unittest
import sys
from scribd.scribd_book_data import TestScribdBookDataLocal, TestScribdBookDataLive

def load_scribd_local(loader):
    return loader.loadTestsFromTestCase(TestScribdBookDataLocal)

def load_scribd_live(loader):
    return loader.loadTestsFromTestCase(TestScribdBookDataLive)

def load_scribd(loader):
    tests = []
    tests.append(load_scribd_local(loader))
    tests.append(load_scribd_live(loader))
    return tests


#https://stackoverflow.com/questions/5360833/how-to-run-multiple-classes-in-single-test-suite-in-python-unit-testing/16823869
if __name__ == '__main__':
    # Run only the tests in the specified classes

    #test_classes_to_run = [TestScribdBookDataLocal]

    loader = unittest.TestLoader()
    suite  = unittest.TestSuite()

    suite.addTests(load_scribd(loader))
    
    runner = unittest.TextTestRunner(verbosity=3)
    result = runner.run(suite)

    # suites_list = []
    # for test_class in test_classes_to_run:
    #     suite = loader.loadTestsFromTestCase(test_class)
    #     suites_list.append(suite)

    # big_suite = unittest.TestSuite(suites_list)

    # runner = unittest.TextTestRunner()
    # results = runner.run(big_suite)