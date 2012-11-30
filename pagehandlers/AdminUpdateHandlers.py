from pagehandlers.PageHandler import *
from utils.image import *
import traceback

""" Admin Update Handler
    Handles database updates from admins """

class AdminUpdateInfoHandler(PageHandler):
    def post(self):
        if not self.isAdmin():
            return

        try:
            book = Library.get_by_id(int(self.request.get("bid")))
            title = self.request.get("new_title")
            edition = int(self.request.get("new_edition"))
            author = self.request.get("new_author")
            isbn = self.request.get("new_isbn")
            desc = self.request.get("new_desc")
            keys = re.split('\s*,\s*',self.request.get("skeys"))

            try: nprice = float(self.request.get("new_price"))
            except: nprice = -1.0

            book.title = title
            book.edition = edition
            book.author = author
            book.isbn = isbn
            book.description = desc
            book.brandNewPrice = nprice
            book.searchKeys = keys
            book.put()

            self.redirect(self.request.referer)
        except Exception, e:
            self.write("Error\n"+repr(e)+"\n"+traceback.format_exc())

class AdminAddConsignee(PageHandler):
    def post(self):
        if not self.isAdmin():
            return

        try:
            uid = int(self.request.get("uid"))#uid of consignee
            consignee = User.get_by_id(uid)
            added_by = self.getUser()
            if not consignee.consignee or not added_by.admin: raise

            bid = int(self.request.get("bid"))
            book = Library.get_by_id(bid)
            if not book:
                logging.info("add consignee: book not found")
                return

            ask_price = float(self.request.get("ask-price"))
            price = float(self.request.get("price"))
            rating = int(self.request.get("rating"))

            new_consigned_book = ConsignedBook(parent=book,consignee=consignee,added_by=added_by,ask_price=ask_price,rating=rating)
            new_consigned_book.put()

        except Exception, e:
            logging.info(e)