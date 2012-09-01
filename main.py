#!/usr/bin/env python
import logging
import math
from pagehandlers.PageHandler import *
from pagehandlers.BuyHandler import *
from pagehandlers.SellHandler import *
from pagehandlers.log_in_out import *
from pagehandlers.UserProfileHandler import *
from pagehandlers.HomePage import *
from pagehandlers.SendMessage import *
from pagehandlers.BookInfoHandler import *
from pagehandlers.AdminHandler import *
from pagehandlers.ConsigneeHandler import *
from pagehandlers.SearchHandler import *
from pagehandlers.ImageHandler import *
from cron.UpdateBookList import *
from cron.ManageExpiry import *

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

        lib,buySell,count = self.getLibListings(offset=(page-1)*limit)
        books = []
        for book in lib:
            books.append(book.toJson(image=True))

        response_data ={"books": json.dumps(books),
                        "buySell":json.dumps(buySell),
                        "page": page,
                        "items":len(buySell),#number of returned items
                        "total":count,
                        "pages": int(math.ceil(count/limit))}
        self.write(json.dumps(response_data))

    #cache this funtion!!!
    #gets limit books starting from offset, arrange by order
    def getLibListings(self,offset=0,order="title"):
        lib,count = Library.getListings(count=True,limit=14,offset=offset)
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

class RequestBookHandler(PageHandler):
    def get(self):
        bid = self.request.get("book")
        try:
            book = Library.get_by_id(int(bid))
            if not book: raise
        except:
            self.redirect("/book/error")
            return
        self.render("book_request.html",book=book)


class BookError(PageHandler):
    def get(self):
        self.render("book_error.html")

class TestDb(PageHandler):
    def get(self,pid):
        logging.info("pid="+str(pid))
        if pid == '0':
            generalTest()
            generateMoreSellOrder()
            loadOtherBooks()
        elif pid == '1':
            logging.info("Creating initial dummy db")
            generalTest()
        elif pid == '2':
            logging.info("Generating more sell Order")
            generateMoreSellOrder()
        elif pid == '3':
            loadOtherBooks()
        self.redirect("/")

class TestImage(PageHandler):
    def get(self):
        i = Image.get_by_id(int(self.request.get("img")))
        if i.image:
            self.response.headers['Content-Type'] = "image/png"
            self.response.out.write(i.image)
        else:
            self.error(404)

#debug ONLY, remove during production
class ClearDatastore(PageHandler):
    def get(self):
        if self.request.get("do_it") != "true":
            self.write("Unable to process request")
            return

        users = User.all()
        for u in users:
            u.delete()
        lib = Library.all()
        for book in lib:
            book.delete()
        s_ord = SellBook.all()
        for ordd in s_ord:
            ordd.delete()
        b_ord = BuyBook.all()
        for ordd in b_ord:
            ordd.delete()
        col = Colleges.all()
        for c in col:
            c.delete()
        priv = PrivacySetting.all()
        for p in priv:
            p.delete()

        self.write("Datastore Cleared Boss")

app = webapp2.WSGIApplication([(r'/', HomePage),
                               (r'/register/?',RegisterHandler),
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
                               (r'/search/?',SearchHandler),
                               (r'/testdb/(\d+)/?',TestDb),
                               (r'/user/update/?',UserSettings),
                               (r'/user/sendmessage/?',SendMessage),
                               (r'/user/inbox/?',SendMessage),
                               (r'/user/orders/?',UserOrder),
                               (r'/user/?',UserProfile),
                               (r'/book/info/?',BookInfoHandler),
                               (r'/book/add/?',AddBookHandler),
                               (r'/book/request/?',RequestBookHandler),
                               (r'/book/error/?',BookError),
                               (r'/browse/?',BrowseAdsHandler),
                               (r'/browse/((.)+)/?',BrowseAdsHandler),
                               (r'/about/?',AboutHandler),
                               (r'/about/(\w+)/?',About2Handler),
                               (r'/help/?',HelpHandler),
                               (r'/help/(\w+)/?',Help2Handler),
                               (r'/admin/?',AdminHandler),
                               (r'/consignee/?',ConsigneeHandler),
                               (r'/testimage/?',TestImage),
                               (r'/clear/datastore/?',ClearDatastore),
                               (r'/update_list/?',UpdateBookList),
                               (r'/_admin/update_expiry/?',UpdateExpiry),#cron job
                               (r'/image/(\d+)(\.jpe?g|\.png|\.gif|\.bmp)?/?',ImageServeHandler),
                              ],debug=True)