#!/usr/bin/env python
from pagehandlers.PageHandler import *

class BuyHandler(PageHandler):
    """ BuyHandler class, responsible for the buying process (i.e posting an add for buying)"""
    def get(self,step=""):
        user = self.getUser()
        if not user:
            self.render_noUser("loggedout.html",err="buy")
            return
        # if url is /buy redirect to step1
        if step == "":
            self.redirect("/buy/step1")
        elif step[-1] == '1':       #buy step1
            self.render("buy_step.html",step=1, buy_active="active")

        elif step[-1] == '2':       #buy step2
            self.render("buy_step.html",step=2,buy_active="active")

        elif step[-1] == '3':       #buy step3
            #get the book id of book to be bought, if no book, redir to step1
            bid = self.request.get("book")
            if not bid:
                self.redirect('/buy/step1')
                return
            book = [getBook(bid)]
            self.render("buy_step.html",step=3, book=book,buy_active="active")
            
        elif step[-1] == '4':
            #show successfull posting of buy add
            bid = self.request.get("book")
            book=[]
            if bid:
                book = getBook(bid)
            self.render("buy_step.html",step=4,book=book,buy_active="active")
        else:
            self.redirect('/buy')
    
    def post(self):
        price = self.request.get("price")
        try:
            bid = int(self.request.get("bid"))
            rating = int(self.request.get("rating"))
        except ValueError:  #if html hidden tags has been tampered, return error
            self.redirect('/buy/error')
            return
        errors=[]
        if rating not in range(1,6):
            errors.append("Invalid Rating Score")
        if not valid_price(price):
            errors.append("Price must be of the format: xxx.xx")

        book = Library.get_by_id(bid)
        user = self.getUser()
        if not book or not user:    #if buying a book that DNE or posting while not loggedin
            self.redirect('/buy/error')
            return

        if len(errors)>0:
            self.render("buy_step.html",step=3,book=[book],errors=errors,rating=rating)
        else:   #add new posted buy add to Book dbmodel
            new_ad = BuyBook(bookId = bid,
                          book = book,
                          user = user,
                          price = float(price),
                          rating = rating,
                          parent = book)
            new_ad.put()
            self.redirect('/buy/step4?book='+str(bid))
