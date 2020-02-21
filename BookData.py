from PIL import Image

class BookData:

    def __init__(self):
        self._format = "Digital"

    def __str__(self):
        print("Relative infomation about the book")

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
