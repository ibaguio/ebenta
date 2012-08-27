#!/usr/bin/env python
from pagehandlers.PageHandler import *
from datetime import datetime

class BookInfoHandler(PageHandler):
    def get(self):
        bid = self.request.get("book")
        try:
        	book = Library.get_by_id(int(bid))
        except:
        	self.redirect("/book/error")
        	return
        if book:
            stats = book.getStats()
            self.render("book.html",book=book, stats=stats)
            return
        self.redirect("/book/error")

    #handles ajax request to get listings
    #SellOrder
    def post(self):
        sort = self.request.get("sort")
        order = self.request.get("order")
        book_id = self.request.get("bid")
        limit = self.request.get("limit")
        offset = self.request.get("offset")
        try:
            book = Library.get_by_id(int(book_id))
        except:
            pass

        if not limit:   #limit to number of postings to display
            limit = 5
        else: limit = int(limit)
        if not offset:  #offset for search
            offset = 0
        else: offset = int(offset)

        assert offset >= 0
        assert limit >= 0
        
        if not book:
            self.response.status_int = 400   #tell receiver that his post data is invalid
            return
        if order == "asc":
            qOrder = sort
        elif order == "desc":
            qOrder = "-"+sort
        else:
            raise BaseException
        
        logged_user = self.getUser()
        if not logged_user:
            viewer = 0
        elif not logged_user.admin:
            viewer = 1
        elif logged_user.admin:
            viewer = 3

        #gets the result as a tuple
        query = SellBook.getListings(book,order=qOrder,limit=limit,offset=offset,count=True)
        #breaks down the tuple
        listings_raw,total_count = query[0],query[1]

        if total_count == 0:    #tells the client that there is now listings for this book
            self.response.status_int = 401  #change this to something reasonable in http
            logging.info("No sellers for book")
            return

        listings_json = []
        for listing in listings_raw:
            listings_json.append(listing.toJson(viewer=viewer))

        page = self.getPage(offset,limit)

        response_data ={"books": listings_json,
                        "order": qOrder,
                        "limit": len(listings_json),
                        "offset": offset,
                        "total": total_count,
                        "page": page,
                        "bid": book_id}

        if page > total_count:
            self.response.status_int = 400  #invalid page
            return

        response = json.dumps(response_data)
        #logging.info(response)
        self.write(response)

    def getPage(self,offset,limit):
        return (offset/limit) +1