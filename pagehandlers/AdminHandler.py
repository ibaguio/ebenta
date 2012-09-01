#!/usr/bin/env python
from pagehandlers.PageHandler import *
from utils.image import *

class AdminHandler(PageHandler):
    def get(self):
        if not self.getUser().admin:
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
        self.redirectBack()

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