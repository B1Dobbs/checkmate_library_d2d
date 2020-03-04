""" This folder can expand to include multuple modules that will have common functionality.
Common functions can be grouped in utils.py until there is a need to separate them."""
from lxml import etree
import io
import requests
from PIL import Image
import requests, sys, webbrowser, bs4
import json
import re
import regex # pip install regex
import math


def get_image_from_url(url):
    """
    Will get the pillow image from a url

        Args:
            url: the URL for the image

        Returns:
            A Pillow image
    """
    image_response = requests.get(url)
    img = Image.open(io.BytesIO(image_response.content))
    return img

def get_root_from_url(url):
    """
    Will get the lxml root for an html file.

        Args:
            url: the URL for the website

        Returns:
            An etree root for the page.
    """
    content = requests.get(url).content
    parser = etree.HTMLParser(remove_pis=True)
    tree = etree.parse(io.BytesIO(content), parser)
    root = tree.getroot()
    return root

def queryHtml(root, expr):
    """
    Wrapper for node.xpath() to prevent IndexOutOfBounds Exception

        Args:
            root: the starting node for the xpath expression
            expr: the string expression to query with

        Returns:
            - Single node for unique query
            - Array for queries that are not unique
            - None when the query result is empty
    """
    try:
        result = root.xpath(expr)
        if len(result) == 1:
            result = result[0]
        elif len(result) == 0:
            result = None
    except:
        print("WARNING: Could not retrieve data for " + expr)

    return result


def librariaLinkSearch(searchVar):
    links = []
    link = 'https://www3.livrariacultura.com.br/ebooks/?ft=' + searchVar
    res = requests.get(link)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    for div in soup.find_all('div', class_="prateleiraProduto__informacao__preco"):
        for a in div.find_all('a'):
            links.append(a.get('href'))

    #This code is supposed to paginate, but for some reason libraria's pagination links don't work at all.
    # First get the number of books
    storageSpan = soup.find('span', class_="resultado-busca-numero")
    numBooksSpan = storageSpan.find('span', class_="value")
    numBooks = int(numBooksSpan.contents[0])

    booksPerPagesOption = soup.find('option', attrs={"selected" : "selected"})
    booksPerPages = int(booksPerPagesOption.contents[0])
    
    numPages = numBooks/booksPerPages

    
    if(numPages > 1):
        for i in range(2, int(numPages)):
            link = 'https://www3.livrariacultura.com.br/ebooks/?ft=' + searchVar + '#' + str(i)
            print(link)
            res = requests.get(link)
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text, "html.parser")

            for div in soup.find_all('div', class_="prateleiraProduto__informacao__preco"):
                for a in div.find_all('a'):                 
                    links.append(a.get('href'))


    return links

def googleLinkSearch(searchVar):
    links = []
    link = 'https://www.googleapis.com/books/v1/volumes?q=' + searchVar + '&filter=ebooks&key=AIzaSyCAFFlw7GGtYtnOwN7MZpHMaK_qq11GxdA&maxResults=40'
    apiResponse = requests.get(link)

    for item in apiResponse.json()['items']:
        links.append(item['volumeInfo']['infoLink'])
       
    return links

""" Search test Book Store for relevant links """
def testBookStoreLinkSearch(searchVar):
    links = []
    link = 'http://127.0.0.1:8000/testBookstore/library/?q=' + searchVar
    res = requests.get(link)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    for link in soup.find_all('a', class_="book_title"):
        links.append("http://127.0.0.1:8000/testBookstore" + link.get('href'))

    pattern = re.compile(r'Last')
    findPageNum = str(soup.find('a', text=pattern))

    if(findPageNum):
        temp = re.findall(r'\d+', findPageNum) 
        num_pages = temp[0]

        for i in range(2, int(num_pages)+1):
            print("Looping")
            link = 'http://127.0.0.1:8000/testBookstore/library/?page=' + str(i)
            res = requests.get(link)
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text, "html.parser")

            for link in soup.find_all('a', class_="book_title"):
                links.append("http://127.0.0.1:8000/testBookstore" + link.get('href'))


    return links

""" Searching Kobo for relevant links """
def koboLinkSearch(searchVar):
    links = []
    link = 'https://www.kobo.com/us/en/search?query=' + searchVar
    res = requests.get(link)
    res.raise_for_status
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    for p in soup.find_all('p', class_="title product-field"):
        for link in p.find_all('a'):
            links.append(link.get('href'))

    aLink = soup.find('a', class_="page-link final") # Find the function by looking for the pattern
    if(aLink): #There's more than one page
        num_pages = aLink.contents[0]
        num_pages = int(num_pages) + 1
        for i in range(2, num_pages):
            link = 'https://www.kobo.com/us/en/search?query=' + searchVar + '&pageNumber=' + str(i)
            res = requests.get(link)
            res.raise_for_status
            soup = bs4.BeautifulSoup(res.text, "html.parser")

            for p in soup.find_all('p', class_="title product-field"):
                for link in p.find_all('a'):
                    links.append(link.get('href'))

    return links

def scribdLinkSearch(searchVar):
    links = []
    link = 'https://www.scribd.com/search?content_type=books&page=1&query=' + searchVar + '&language=1'
    res = requests.get(link)

    # The following code gets a json blob from inside a specific javascript function call.  
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    pattern = re.compile(r'function prefetchResource') # Create a python regex to find the function in which the json resides
    string = str(soup.find('script', text=pattern)) # Find the function by looking for the pattern

    pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}') # Because python regex is not as powerful, we have to import a more powerful standardized regex
                                                    # This code selects actual json code

    newString = pattern.findall(string)

    parsed_json = json.loads(newString[1]) # parse the json

    if(parsed_json['result_count'] != '0'): # If there are any results
        results = parsed_json['results']  
        for book in results['books']['content']['documents']:
            links.append(book['book_preview_url'])

        num_pages = parsed_json['page_count']

        for i in range(2, num_pages + 1):
            link = 'https://www.scribd.com/search?content_type=books&page=' + str(i) + '&query=' + searchVar + '&language=1'
            res = requests.get(link)

            # The following code gets a json blob from inside a specific javascript function call.  
            soup = bs4.BeautifulSoup(res.text, "html.parser")
            pattern = re.compile(r'function prefetchResource') # Create a python regex to find the function in which the json resides
            string = str(soup.find('script', text=pattern)) # Find the function by looking for the pattern

            pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}') # Because python regex is not as powerful, we have to import a more powerful standardized regex
                                                            # This code selects actual json code

            newString = pattern.findall(string)

            parsed_json = json.loads(newString[1]) # parse the json
            results = parsed_json['results']
            
            for book in results['books']['content']['documents']:
                links.append(book['book_preview_url'])


    link = 'https://www.scribd.com/search?content_type=audiobooks&page=1&query=' + searchVar + '&language=1'
    res = requests.get(link)

    # The following code gets a json blob from inside a specific javascript function call.  
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    pattern = re.compile(r'function prefetchResource') # Create a python regex to find the function in which the json resides
    string = str(soup.find('script', text=pattern)) # Find the function by looking for the pattern

    pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}') # Because python regex is not as powerful, we have to import a more powerful standardized regex
                                                    # This code selects actual json code

    newString = pattern.findall(string)

    parsed_json = json.loads(newString[1]) # parse the json

    if(parsed_json['result_count'] != '0'): # If there are any results
        results = parsed_json['results']
        for audiobook in results['audiobooks']['content']['documents']:
            links.append(audiobook['book_preview_url'])

        num_pages = parsed_json['page_count']

        for i in range(2, num_pages + 1):
            link = 'https://www.scribd.com/search?content_type=audiobooks&page=' + str(i) + '&query=' + searchVar + '&language=1'
            res = requests.get(link)

            # The following code gets a json blob from inside a specific javascript function call.  
            soup = bs4.BeautifulSoup(res.text, "html.parser")
            pattern = re.compile(r'function prefetchResource') # Create a python regex to find the function in which the json resides
            string = str(soup.find('script', text=pattern)) # Find the function by looking for the pattern

            pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}') # Because python regex is not as powerful, we have to import a more powerful standardized regex
                                                            # This code selects actual json code

            newString = pattern.findall(string)

            parsed_json = json.loads(newString[1]) # parse the json
            results = parsed_json['results']
            
            for book in results['audiobooks']['content']['documents']:
                links.append(book['book_preview_url'])

    
    return links







