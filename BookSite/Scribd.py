from BookData import BookData
from lxml import etree
from BookSite.common.utils import *
import requests, sys, webbrowser, bs4, traceback
import io
import json
import re 


"""Given a direct link to a book page at a site, parse it and return the SiteBookData of the info""" 
def get_book_data(url):
    # type: (str) -> SiteBookData 
    book_data = BookData()
    
    book_data.site_slug = "SD"
    book_data.ready_for_sale = True
    book_data.ready_for_sale = True
    book_data.format = "Digital"
    book_data.parse_status = "Successful"

    try:
        root = get_root_from_url(url)
        #Get ISBN
        j = queryHtml(root, "//script[@type = 'application/ld+json']")[1].text
        y = json.loads(j)
        
        title = queryHtml(root, "//h1[@class='document_title']").text
        if(':' in title):
            title = title.split(': ')
            book_data.title = title[0]
            book_data.subtitle = title[1]
        else:    
            book_data.title = title

        book_data.image_url = root.xpath(".//div[@class='document_cell']//img/@src")[0]
        book_data.image = get_image_from_url(book_data.image_url)
        book_data.description = queryHtml(root, ".//meta[@property='og:description']/@content")
    
        roottext = etree.tostring(root, encoding = "unicode")
        roottext = roottext.split('"')
        p = re.compile('^(97(8|9))?\d{9}(\d|X)$')

        for i in roottext:
            l = p.search(i)
            if(l != None):
                book_data.isbn_13 = l.string
        #Get Author List
        authors = []
        for i in range (0, len(y['author'])):
            authors.append(y['author'][i]['name'])
            #print(y['author'][i]['name'])

        author_list = []
        if(type(authors) == list):
            author_list += authors
        else:
            author_list.append(authors)
            
        book_data.authors = author_list

        #Get Book ID From URL
        bookID = queryHtml(root, "//link[@rel = 'alternate'][1]/@href")
        book_data.book_id = url.replace('https://www.scribd.com/', '')
        
        book_data.content = queryHtml(root, "/html")

        book_data.url = convert_book_id_to_url(book_data.book_id)
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to url ", url)
        book_data.parse_status = "UNSUCCESSFUL"
    except:
        print("ERROR: Processing book at " + url)
        traceback.print_exc()

    return book_data

"""Given a SiteBookData, search for the book at the `book_site` site
and provide a list of likely matches paired with how good
of a match it is (1.0 is an exact match). 
This should take into account all the info we have about a book, 
including the cover.""" 
def find_book_matches(book_data):
    links = []

    titleLinkSearch = ""

    if book_data.authors != None: # If a title is sent in to search by, record link matches
        titleLinkSearch += book_data.get_authors_as_string()
    
    if book_data.title != None: # If a title is sent in to search by, record link matches
        if(titleLinkSearch != ""):
            titleLinkSearch += " "
            titleLinkSearch += book_data.title
        else:
            titleLinkSearch = book_data.title

    if book_data.isbn_13 != None: # If a title is sent in to search by, record link matches
        links += scribdLinkSearch(book_data.isbn)

    if(titleLinkSearch != ""):
        links += scribdLinkSearch(titleLinkSearch)

    linksNoDuplicates = [] 
    for i in links: 
        if i not in linksNoDuplicates: 
            linksNoDuplicates.append(i) #removes duplicate links from list
    # FINISH -> LINKS HAS ALL LINKS WITH ANY MATCHING

    # For each link, get the book data and compare it with the passed in book_data
    return get_matches_from_links(get_book_data, linksNoDuplicates, book_data)

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


"""Given a book_id, return the direct url for the book.""" 
def convert_book_id_to_url(book_id):
    # type: (str) -> str 
    return "https://www.scribd.com/" + book_id