#!/usr/bin/env python
from pagehandlers.PageHandler import *
from google.appengine.api import images
from utils.image import *
import logging, json

class AdminHandler(PageHandler):
    def post(self):
        if not self.getUser().admin:
            return
        if self.request.get("upload-img"):
            self.imgUpdate()
        elif self.request.get("update-info"):
            self.infoUpdate()
        elif self.request.get("add-consignee"):
            self.addConsignee()
        elif self.request.get("addbook"):
            self.addBook()
        self.redirectBack()

    def addBook(self):
        title= self.request.get("title")
        author=self.request.get("author")
        isbn=self.request.get("isbn")
        desc=self.request.get("desc")
        price=self.request.get("brandprice")
        sk = self.request.get("sk").split()

        if not title or not author:
            return

        newBook = Library(title=title,author=author,isbn=isbn,description=desc,brandNewPrice=brandprice)
        newBook.generateSk()
        if sk:
            newBook.addSk(sk)
        newBook.put()
        self.write("ok added")

    def imgUpdate(self):
        img_raw = self.request.get("img1")
        try:
            book = Library.get_by_id(int(self.request.get("bid")))
            ftype = getImageFormat(img_raw)
            if not ftype or not book: 
                raise
            new_img = Image(image=db.Blob(img_raw),ref=book,ftype=ftype)
            new_img.put()
        except:
            pass

    def infoUpdate(self):
        try:
            book = Library.get_by_id(int(self.request.get("bid")))
            title = self.request.get("new_title")
            author = self.request.get("new_author")
            isbn = self.request.get("new_isbn")
            desc = self.request.get("new_desc")

            change = False
            if book.title != title:
                book.title = title
                change = True
            if book.author != author:
                book.author = author
                change = True
            if book.isbn != isbn:
                book.isbn = isbn
                change = True
            if book.description != desc:
                book.description = desc
                change = True

            if change:
                book.put()
        except:
            pass

    def addConsignee(self):
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

        except:
            pass

class UserSearchHandler(PageHandler):
    def post(self):
        key = self.request.get("key")
        val = self.request.get("val")

        if not key or not val:
            self.response.status_int = 401
            return

        if key == "email":
            user = User.all().filter("email",val).get()
        elif key == "username":
            user = User.get_by_key_name(val)
        #elif key == "name"
        if not user:
            self.response.status_int = 401
            return
        res = {"username":user.username}
        self.write(json.dumps(res))

class AdminBookRemoveHandler(PageHandler):
    def post(self):
        if not self.isAdmin():
            return

        try:
            bid = int(self.request.get("bid"))
            book = Library.get_by_id(bid)
            if book:
                logging.warning("Removing book "+str(bid)+" Title: "+book.title)
                book.delete()
                self.response.status_int = 200
        except Exception,e:
            logging.info("Failed to remove book: "+str(e))
            self.response.status_int = 400