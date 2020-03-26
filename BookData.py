from PIL import Image
import re

class BookData:

    def __init__(self):
        self.format = None
        self.title = None
        self.image = None
        self.image_url = None
        self.isbn_13 = None
        self.description = None
        self.series = None
        self.vol_number = None
        self.authors = []
        self.ready_for_sale = None
        self.site_slug = None
        self.parse_status = None
        self.subtitle = None
        self.book_id = None
        self.url = None
        self.content = None
        self.extra = None
        self.content = None

    def __str__(self):
        print("Relative infomation about the book")

    def printData(self):
        print("Book")
        print("================")
        print("Format", end = ": \t")
        print(self.format)
        print("Title", end = ": \t \t")
        print(self.title)
        print("Image URL", end = ": \t")
        print(self.image_url)
      
        # if self.image != None:
        #     self.image.show()

        print("ISBN", end = ": \t \t")
        print(self.isbn_13)
        print("Description", end = ": \t")
        print(self.description)
        print("Series", end = ": \t")
        print(self.series)
        print("Vol. Number", end = ": \t")
        print(self.vol_number)
        print("Authors", end = ": \t")
        print(self.authors)
        print("Available", end = ": \t")
        print(self.ready_for_sale)
        print("Site Slug", end = ": \t")
        print(self.site_slug)
        print("Parse Status", end = ": \t")
        print(self.parse_status)
        print("Subtitle", end = ": \t")
        print(self.subtitle)
        print("Book ID", end = ": \t")
        print(self.book_id)
        print("URL", end = ": \t \t")
        print(self.url)
        print("Extra", end = ": \t \t")
        print(self.extra)
        print("Content", end = ": \t")
        print(self.content)

    def get_authors_as_string(self):
        pattern =  '[^A-Za-z0-9 ,]+'
        return re.sub(pattern, "", str(self.authors))
