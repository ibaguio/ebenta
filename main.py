#!/usr/bin/env python
import webapp2, os
import logging
import jinja2
import math
from math import ceil
from utils.crypto import *
from utils.regex import *
from utils.search import *
from database.dbModels import *
from database.test import *
from pagehandlers.PageHandler import *
from pagehandlers.BuyHandler import *
from pagehandlers.SellHandler import *
from pagehandlers.log_in_out import *
from pagehandlers.UserProfileHandler import *
from pagehandlers.HomePage import *
from pagehandlers.SendMessage import *
from pagehandlers.StatsHandler import *
#version/upload number
vs = 4

class ItemInfoHandler(PageHandler):
    def get(self):
        bid = self.request.get("book")
        book = Library.get_by_id(int(bid))

        if book:
            self.render("book.html",book=book)

    #handles ajax request to update listings
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
        logging.info(response)
        self.write(response)

    def getPage(self,offset,limit):
        return (offset/limit) +1

class AboutHandler(PageHandler):
    def get(self):
        self.render("/about/about.html")

class About2Handler(PageHandler):
    def get(self,param):
        if param == "faq":
            self.render("/about/faq.html")
        elif param == "contact":
            self.render("/about/contact.html")
        elif param == "developers":
            self.render("/about/developers.html")
        elif param == "copyrights":
            self.render("/about/copyrights.html")
        elif param == "terms":
            self.render("/about/terms.html")
        else:
            self.redirect("/about")

class HelpHandler(PageHandler):
    def get(self):
        self.render("/help/consign.html")

class Help2Handler(PageHandler):
    def get(self,param):
        if param=="consign":
            self.redirect("/help")
            
class BrowseAdsHandler(PageHandler):
    def get(self,category="",*a):
        m = self.request.get("m")
        if category == "":
            category = "library"
        
        if category == "library":
            lib,buySell,count = self.getLibListings()
            self.render("browse.html",show=lib,info=buySell,lenS=len(lib),q="lib",browse_active="active")
        elif category == "buying":
            lib,buySell = self.getSellListings()
            self.render("browse.html",show=lib,info=buySell,lenS=len(lib),q="sell",sell_active="active")
        elif category == "for-sale":
            lib,buySell = self.getBuyListings()
            self.render("browse.html",show=lib,info=buySell,lenS=len(lib),q="buy",buy_active="active")

    def post(self):
        limit = 14
        page = self.request.get("page")
        try:
            page = int(page)
            assert page > 0
        except:
            page = 1

        lib,buySell,count = self.getLibListings()
        books = []
        for book in lib:
            books.append(book.toJson(image=True))

        response_data ={"books": json.dumps(books),
                        "buySell":json.dumps(buySell),
                        "page": page,
                        "pages": math.ceil(count/limit)}
        logging.info("")
        logging.info(response_data)
        self.write(json.dumps(response_data))

    #cache this funtion!!!
    #gets limit books starting from offset, arrange by order
    def getLibListings(self,offset=0,order="title"):
        lib,count = Library.getListings(count=True,limit=14)
        buySell = []
        for book in lib:
            buy = BuyBook.getListings(book,count_only=True)
            sell = SellBook.getListings(book,count_only=True)
            buySell.append([buy,sell])
        return lib,buySell,count
    
    #returns books with unexpired sale listings
    def getSellListings(self,limit=30,offset=0,order="title"):
        lib = Library.all().order(order).fetch(limit=limit,offset=offset)
        show = []
        buySell = []    #info for book listing count
        for book in lib:
            sell = SellBook.getListings(book,count_only=True)
            if (sell>0):
                buy = BuyBook.getListings(book,count_only=True)
                show.append(book)
                buySell.append([buy,sell])
        return show,buySell
    
    #returns books with unexpired buying listings
    def getBuyListings(self,limit=30,offset=0,order="title"):
        lib = Library.all().order(order).fetch(limit=limit,offset=offset)
        show = []
        buySell = []
        for book in lib:
            buy = BuyBook.getListings(book,count_only=True)
            if (buy>0):
                sell = SellBook.getListings(book,count_only=True)
                show.append(book)
                buySell.append([buy,sell])
        return show,buySell
        
class Register(PageHandler):
    def get(self):
        self.redirect("/")
    def post(self):
        self.redirect("/")

class CommentHandler(PageHandler):
    def post(self):
        user =  self.isLogged()
        if not user:
            self.redirect("/")      #must login to comment
        else:
            comment = self.request.get("comment")
            logging.error("comment: "+comment)
            if not comment:
                self.redirect("/home")
                return
            u = User.all().filter('username',user).get()
            com = Comment(user=u, comment=comment)
            com.put()
            self.redirect('/home?comment=success')
            
class SearchHandler(PageHandler):
    def get(self):
        next = self.request.get("next")
        user =  self.isLogged()
        query = self.request.get("q").lower()
        if query == "" or query == "enter title or author":
            self.redirect("/")
        
        results,time = searchBooks(query)
        self.render('search_results.html',
                        results=results,
                        time=self.getTime(time),
                        query=query,
                        resLen=len(results),
                        next=next)
    def getTime(self,time):
        if time > 1:
            ret = "<b>" + str(time)[:4] + "</b> seconds"
        else:
            postfix = ["milli","nano"]
            for i in range(len(postfix)):
                ntime = time*1000
                if ntime > 1:
                    ret = "<b>" + str(ntime)[:6] + "</b> "+postfix[i]+" seconds"
                    break
        return ret

class AddBookHandler(PageHandler):
    def get(self):
        user = self.isLogged()
        if user:
            self.render("add_book.html")
        else:
            self.render_noUser("add_book.html",error="You must be logged in to view this page")

    def post(self):
        next = self.request.get("next")
        user = self.isLogged()
        if user:
            title=self.request.get("title").title()
            author=self.request.get("author").title()
            
            if not title or not author:
                if next:
                    self.redirect("/"+next+"/step2?err")
                    return
                self.render("add_book.html",err="Please Fill up all fields")
                return
            
            new_book = Library(title=title,author=author)
            new_book.generateSk()
            new_book.put()
            
            if next:
                self.redirect("/"+next+"/step3?book="+str(new_book.key().id()))
                return
            self.redirect("/books?id="+new_book.key().id())
            
class BookInfoHandler(PageHandler):
#            self.render("book.html",book = new_book,msg="Book Successfully Added")
    pass

class TestDb(PageHandler):
    def get(self,pid):
        logging.info("pid="+str(pid))
        if pid == '1':
            logging.info("Creating initial dummy db")
            generalTest()
        elif pid == '2':
            logging.info("Generating more sell Order")
            generateMoreSellOrder()
        elif pid == '3':
            loadOtherBooks()
        self.redirect("/")

class VersionShow(PageHandler):
    def get(self):
        global vs
        self.write("Upload Number "+str(vs))
        self.write("""
        <br/>2. Fixed postings
        <br/>2. Added browsing
        <br/>2. Changed Models
        <br/>3. Updated Profile Page
        <br/>3. Fixed GUI of view privacy
        <br/><h1>VERSION 2</h1>
        twitter bootstrap as frontend
        """)

app = webapp2.WSGIApplication([(r'/', HomePage),
                               (r'/register/?',Register),
                               (r'/home/?',UserHome),
                               (r'/logout/?',LogoutHandler),
                               (r'/login/?',LoginHandler),
                               (r'/sell/?',SellHandler),
                               (r'/sell/(step[1-4])/?',SellHandler),
                               (r'/sell/search/?',SearchHandler),
                               (r'/buy/?',BuyHandler),
                               (r'/buy/(step[1-4])/?',BuyHandler),
                               (r'/buy/search/?',SearchHandler),
                               (r'/suggest/?',CommentHandler),
                               (r'/search',SearchHandler),
                               (r'/testdb/(\d+)',TestDb),
                               (r'/user/update/?',UserSettings),
                               (r'/user/sendmessage',SendMessage),
                               (r'/user/inbox',SendMessage),
                               (r'/user/orders',UserOrder),
                               (r'/user/?',UserProfile),
                               (r'/info/?',ItemInfoHandler),
                               (r'/books/add/?',AddBookHandler),
                               (r'/browse/?',BrowseAdsHandler),
                               (r'/browse/((.)+)/?',BrowseAdsHandler),
                               (r'/about/?',AboutHandler),
                               (r'/about/(\w+)/?',About2Handler),
                               (r'/about/version_check',VersionShow),
                               (r'/help/?',HelpHandler),
                               (r'/help/(\w+)/?',Help2Handler),
                               (r'/item/book/stats/?',BookStatsHandler)
                              ],debug=True)
