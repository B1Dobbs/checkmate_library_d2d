from PIL import Image

class BookData:

    def __init__(self):
        self.format = None
        self.title = None
        self.image = None
        self.image_url = None
        self.isbn = None
        self.description = None
        self.series = None
        self.vol_number = None
        self.authors = None
        self.ready_for_sale = None
        self.site_slug = None
        self.subtitle = None
        self.book_id = None
        self.url = None
        self.extra = None

    def __str__(self):
        print("Relative infomation about the book")

    def printData(self):
        print(self.format)
        print(self.title)
        print(self.image_url)
        if(self.image != None):
            self.image.show()
        print(self.isbn)
        print(self.description)
        print(self.series)
        print(self.vol_number)
        print(self.authors)
        print(self.ready_for_sale)
        print(self.site_slug)
        print(self.subtitle)
        print(self.book_id)
        print(self.url)
        print(self.extra)

    # format : string
    # title : string
    # image : pillow image
    # image_url : string
    # isbn_13 : string
    # description : string
    # series : float
    # vol_number : float
    # subtitle : subtitle
    # authors : array 
    # book_id : string 
    # site_slug : string 
    # parse_status : FULLY_PARSED or UNSUCCESSFUL 
    # url : string 
    # content : string 
    # ready_for_sale : boolean 
    # extra : dictionary
