from pagehandlers.PageHandler import *
import json

class UserBookOrders(PageHandler):
    """ Responds to ajax request that asks for the 
        user's consigned/requested books"""

    def post(self):
        me = self.isLogged()
        logging.info("user: "+me.username)
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
        logging.info(consigned_books.count())
        if consigned_books.count()==0:
            logging.info("No consigned")
            self.response.status_int = 400
            return
        books = []
        for cbook in consigned_books:
            books.append(cbook.toDict(book_info=True))

        logging.info(json.dumps(books))
        self.write(json.dumps(books))

    def getRequest(self,user):
        raw_books = user.requested_books
        logging.info("a")
        if raw_books.count()==0:
            logging.info("b")
            self.response.status_int = 400
            return
        books = []
        for book in raw_books:
            books.append(book.toDict())
        self.write(json.dumps(books))
        
