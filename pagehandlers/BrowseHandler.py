from pagehandlers.PageHandler import *
from database.dbModels import *
import time
class BrowseAdsHandler(PageHandler):
    def get(self,category="",*a):
        m = self.request.get("m")
        if category == "":
            category = "library"
        
        if category == "library":
            lib,con,count = self.getLibListings()
            self.render("browse.html",show=lib,info=con,lenS=len(lib),q="lib",browse_active="active")

    def post(self):
        limit = 14
        page = self.request.get("page")
        try:
            page = int(page)
            assert page > 0
        except:
            page = 1

        lib,con,count = self.getLibListings(offset=(page-1)*limit)
        books = []
        for book in lib:
            books.append(book.toJson(image=True))

        response_data ={"books": json.dumps(books),
                        "con":json.dumps(con),
                        "page": page,
                        "items":len(con),#number of returned items
                        "total":count,
                        "pages": int(math.ceil(count/limit))}
        self.write(json.dumps(response_data))

    #cache this funtion!!!
    #gets limit books starting from offset, arrange by order
    def getLibListings(self,offset=0,order="title"):
        lib,count = Library.getListings(count=True,limit=14,offset=offset)
        con = []
        for book in lib:
            con.append(ConsignedBook.getListings(book,count=True,listings=False))
        return lib,con,count