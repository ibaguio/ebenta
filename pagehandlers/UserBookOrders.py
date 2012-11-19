from pagehandlers.PageHandler import *
import json

class UserBookOrders(PageHandler):
    """ Responds to ajax request that asks for the 
        user's consigned/requested books"""

    def post(self):
        me = self.isLogged()
        if not me:
            self.response.status_int = 401
            return
        req = self.request.get("req")
        if req == "consign":
            self.getConsigned(me)
        elif req == "request":
            self.getRequest(me)
        else:
            self.response.status_int = 401

    def getConsigned(self,user):
        consigned_books = user.consigned_books
        consigned_request = user.request_to_consign
        if consigned_books.count()==0 and consigned_request.count()==0:
            self.response.status_int = 400
            return
        books = []
        for cbook in consigned_books:
            books.append(cbook.toDict(book_info=True))
        req = []
        for rbook in consigned_request:
            req.append(rbook.toDict())

        d = {"books":books,
            "req":req}

        self.write(json.dumps(d))

    def getRequest(self,user):
        raw_books = user.requested_books
        if raw_books.count()==0:
            self.response.status_int = 400
            return
        books = []
        for book in raw_books:
            books.append(book.toDict())
        self.write(json.dumps(books))