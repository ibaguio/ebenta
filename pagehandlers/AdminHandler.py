#!/usr/bin/env python
from pagehandlers.PageHandler import *
from google.appengine.api import images
from utils.image import *
import logging, json

class AdminAddBookHandler(PageHandler):
    def post(self):
        title= self.request.get("title")
        author=self.request.get("author")
        isbn=self.request.get("isbn")
        desc=self.request.get("desc")
        p = self.request.get("brandprice",default_value=-1.0)
        sk = self.request.get("sk").split()
        
        try:
            if not p: raise
            else: price = float(p)
        except:
            price = -1.0
        
        if not title or not author:
            return

        newBook = Library(title=title,author=author,isbn=isbn,description=desc,brandNewPrice=price)
        newBook.generateSk()
        if sk:
            for s in sk:
                newBook.addSk(s)
        newBook.put()

        res = """<html><body><pre>
                OK ADDED
                Title:          %(title)s
                Author:         %(author)s
                ISBN:           %(isbn)s
                Description:    %(desc)s
                Brandnew Price: %(bnew)f
                Search Keys:    %(sk)s

                WILL REDIRECT BACK IN ABOUT 3 seconds... 
                <a href='/home#addbook'>click here to go back</a>
                Note: if brand new price is, -1.0. that means there is No Data

                </pre></body></html>
                <script>window.onload=(function() {
                    setTimeout("location.pathname='/home'", 3000);});</script>
                """

        sss = ",".join(newBook.searchKeys)
        self.write(res%{"title":title,"author":author,"isbn":isbn,"desc":desc,"bnew":price,"sk":sss})

class AdminHandler(PageHandler):
    def get(self):
        user = self.getUser()
        if not user.admin:
            self.redirect("/")
            return
        self.render("admin.html",user=user,admin_active="active")

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

class AddConsigneeHandler(PageHandler):
    def post(self):
        try:
            user = User.get_by_key_name(self.request.get("uname"))
            ask_price = float(self.request.get("ask-price"))
            sell_price = float(self.request.get("price"))
            rating = int(self.request.get("rating"))
            added_by = User.get_by_key_name(self.request.get("adder"))
            book = Library.get_by_id(int(self.request.get("bid")))

            if not user or not ask_price or not sell_price or not rating or not book or not added_by:
                raise

            new_consigned_book = ConsignedBook(parent=book,consignee=user,added_by=added_by,\
                ask_price=ask_price,rating=rating,price=sell_price)
            new_consigned_book.put()

            #add the image
            img = self.request.get("img")
            ftype = getImageFormat(img)
            if img:
                new_image = Image(ref=new_consigned_book,image=db.Blob(img),ftype=ftype)
                new_image.put()
            self.write("OK added")
        except:
            self.write("NOT ADDED")

class UserListHandler(PageHandler):
    def post(self):
        user = self.isLogged()
        if not user.admin:
            self.response.status_int = 400
            return

        ret = []
        all_users = User.all().order("username").fetch(100)
        for u in all_users:
            ret.append(u.toDict())
        self.write(json.dumps(ret))

class AllUserRequests(PageHandler):
    def post(self):
        if not self.isLogged().admin:
            return

        all_req = RequestedBook.all().order("-posted")

        ret = []
        for req in all_req.fetch(100):
            ret.append(req.toDict())

        self.write(json.dumps(ret))

class AllUserRTC(PageHandler):
    def post(self):
        if not self.isLogged().admin:
            self.response.status_int = 400
            return

        all_rtc = ConsignRequest.all().order("-posted").fetch(100)
        ret = []
        for rtc in all_rtc:
            ret.append(rtc.toDict())
        self.write(json.dumps(ret))
