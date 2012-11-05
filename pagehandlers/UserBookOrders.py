from pagehandlers.PageHandler import *

class UserBookOrders(PageHandler):
    """ Responds to ajax request that asks for the 
        user's consigned/requested books"""

    def post(self):
        me = self.getUser()
        logging.info("user: "+me.username)
        if not me:
            self.response.status_int = 401
            return
        req = self.request.get("req")
        if req == "consign":
            self.getConsigned(me)
        elif req == "request":
            self.getRequest(me)

    def getConsigned(self,user):
        raw_books = user.consigned_books
        if raw_books.count()==0:
            self.response.status_int = 400
            return
        books = []
        for book in raw_books:
            books.append(book.toJson())

    def getRequest(self,user):
        raw_books = user.requested_books
        logging.info("a")
        if raw_books.count()==0:
            logging.info("b")
            self.response.status_int = 400
            return
        logging.info("a")
        books = []
        for book in raw_books:
            books.append(book.toJson())
        
