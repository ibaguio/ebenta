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
            stats = self.getBookStats(book)
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
            listings_json.append(listing.toJson())

        page = self.getPage(offset,limit)

        response_data ={"books": listings_json,
                        "order": qOrder,
                        "limit": len(listings_json),
                        "offset": offset,
                        "total": total_count,
                        "page": page}

        if page > total_count:
            self.response.status_int = 400  #invalid page
            return

        response = json.dumps(response_data)
        #logging.info(response)
        self.write(response)

    def getPage(self,offset,limit):
        return (offset/limit) +1

    #returns a dict containing the stats of the book
    def getBookStats(self,book):
        stats = {}
        stats["newPrice"] = book.brandNewPrice
        if stats["newPrice"] <= 0:
            stats["newPrice"] = "No Data"

        tsold = Transaction.all().ancestor(book).count()
        if tsold == 0:
            stats["totalSold"] = "None yet"
        elif tsold == 1:
            stats["totalSold"] = "1 copy"
        elif tsold > 1:
            stats["totalSold"] = str(Transaction.all().ancestor(book).count()) + " copies"

        #get the listed books
        listed = SellBook.all().filter("expire >", datetime.now()).filter("transaction = ",None).ancestor(book)
        sum_ = 0.0
        count = 0
        books_listed = listed.fetch(50)
        #get the average price for the last 50 listed books
        if listed.count() > 0:
            for book_posted in books_listed:
                count+=1
                sum_ += book_posted.price
            ave = sum_/count
            stats["avePrice"] = str(round(ave,2))
        else:
            stats["avePrice"] = "No Data"

        
        stats["listed"] = listed.count()
        return stats