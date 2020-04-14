import unittest
import sys
sys.path.append(".")
from BookSite.scribd import Scribd
from Checkmate import get_book_site
from base_book_parse_test import BaseBookParseTest
from scribd.test_cases import ScribdTestCases
  

class TestScribdLinksLocal(BaseBookParseTest): 
  
    def test_collins(self):  
        local_url = "test/scribd/test_pages/the_hunger_games_by_suzanne_collins.html"
        self.common_test(local_url, ScribdTestCases.collins_local, Scribd())

    def test_dalio(self):
        local_url = "test/scribd/test_pages/principles_by_ray_dalio.html"
        self.common_test(local_url, ScribdTestCases.dalio_local, Scribd())

    def test_bryant(self):
        local_url = "test/scribd/test_pages/the_mamba_mentality_by_kobe_bryant.html"
        self.common_test(local_url, ScribdTestCases.bryant_local, Scribd())

class TestScribdLinksLive(BaseBookParseTest):

    def test_collins(self):  
        local_url = "https://www.scribd.com/audiobook/389029058/The-Hunger-Games-Special-Edition"
        self.common_test(local_url, ScribdTestCases.collins_live, Scribd())

    def test_dalio(self):
        local_url = "https://www.scribd.com/book/357813054/Principles-Life-and-Work"
        self.common_test(local_url, ScribdTestCases.dalio_live, Scribd())

    def test_bryant(self):
        local_url = "https://www.scribd.com/book/445929040/The-Mamba-Mentality-How-I-Play"
        self.common_test(local_url, ScribdTestCases.bryant_live, Scribd())


