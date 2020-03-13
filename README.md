# Checkmate Library

## Small library for parsing online websites for book data that is coming March 2020.

### Branch descriptions...<br>
 - **master:** the main realease branch<br>
- **development:** the branch used for integration and testing before merging to master
- **\<issueID>_\<issueTitle>:** naming scheme for feature branches

### Dependencies
- requests==2.23.0
- lxml==4.5.0
- regex==2020.2.20
- isbnlib==3.9.10
- beautifulsoup4==4.8.2
- Pillow==7.0.0
- python_Levenshtein==0.12.0

### How to Run Tests
There are two types of tests in our Checkmate Library: one for finding matches, and one for book scraping. The <site_slug> arguement is optional but not using it will run all tests.
1. testBookData.py is for scraping one book at a time. 

>To Run: $python testBookData.py <site_slug>

2. testSiteQuery.py will run find_book_matches 

>To Run: $python testSiteQuery.py <site_slug>

#### Folder Structure
```
checkmate_library \
    |---BookSite \	        - Module of BookSites
	|---common \
		|---utils.py		- Common functions
	|---GoogleBooks.py
	|---Kobo.py
	|---Livraria Cultura.py
	|---Scribd.py
	|---TestBookstore.py
    |---BookData.py		- BookData Class
    |---Checkmate.py	    	- Library entry with get_book_site
    |---testBookData.py	   	- Tests for one page scrapers
    |---testSiteQuery.py 	- Tests for gathering matches
```
