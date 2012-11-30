from pagehandlers.PageHandler import *
from database.dbModels import *
import time, math

class BrowseHandler(PageHandler):
    def get(self,filtr=""):
        try:
            page = int(self.request.GET["page"])
        except Exception,e:
            page = 1
            pass

        items_per_page = 14.0
        if not page: page = 1
        offset = int((page-1) * items_per_page)

        books,con,tot_count = self.getLibListings(offset=offset,category=filtr)
        total_pages = int(math.ceil(tot_count/items_per_page))
        if page !=1 and total_pages < page:
            self.render("browse.html",filter=filtr,total_pages=-1)
            return

        data = {"books":books, "consigned":con}
        
        self.render("browse.html",data=data,
            browse_active="active",total_pages=total_pages,
            filter=filtr,page=page,)

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
    def getLibListings(self,offset=0,order="title",category=""):
        lib,count = Library.getListings(count=True,limit=14,offset=offset,category=category)
        con = []
        for book in lib:
            con.append(ConsignedBook.getListings(book,count=True,listings=False))
        return lib,con,count