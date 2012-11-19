#!/usr/bin/env python
import logging
import math
import json
from pagehandlers.PageHandler import *
from pagehandlers.BlogPostHandler import *
from pagehandlers.UserBookOrders import *
from pagehandlers.RegisterHandler import *
from pagehandlers.log_in_out import *
from pagehandlers.UserProfileHandler import *
from pagehandlers.HomePage import *
from pagehandlers.SendMessage import *
from pagehandlers.BookInfoHandler import *
from pagehandlers.AdminHandler import *
from pagehandlers.ConsigneeHandler import *
from pagehandlers.SearchHandler import *
from pagehandlers.ImageHandler import *
from pagehandlers.BrowseHandler import *

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
        if not self.isLogged():
            self.render("loggedout.html")
            return
        bid = self.request.get("book")
        try:
            book = Library.get_by_id(long(bid))
            if not book: raise
        except:
            self.render("book_request.html")
            return
        self.render("book_request.html",book=book,data_date=self.getDataDate())

    def getDataDate(self):
        date_now = datetime.date.today() + datetime.timedelta(days=7)
        return str(date_now.strftime("%d/%m/%Y"))

    def post(self):
        bid = self.request.get("bid")
        if not bid:
            title = self.request.get("title")
            author = self.request.get("author")
            isbn = self.request.get("isbn")

            if not title:#title must be required
              self.render("book_request.html",showErr=True)
              return


        user = self.isLogged()
        if bid:
          book = Library.get_by_id(long(bid))
          if not book:
              logging.info("bid not found")
              self.response.status_int = 400
              return
        else:
          new_unlisted_book = UnlistedLibrary(title=title,author=author,isbn=isbn)
          new_unlisted_book.put()
          book = new_unlisted_book

        needed = self.request.get("needed")
        request = self.request.get("requests")
        if self.request.get("copy_kind") == "used":
            max_price = self.request.get("maxprice")
            min_rating = long(self.request.get("condition"))
            new_request = RequestedBook(book,user=user,max_price=max_price,min_rating=min_rating,\
                requests=request,date_needed=needed)
            new_request.put()
        else:
            new_request = RequestedBook(book,user=user,requests=request,date_needed=needed,brand_new=True)
            new_request.put()
        self.render("request_ok.html")

class ConsignBookHandler(PageHandler):
    def get(self):
      if not self.isLogged():
          self.render("loggedout.html")
          return
      book=None
      try:
        bid = self.request.get("book")
        book = Library.get_by_id(int(bid))
      except:
        pass
      self.render("book_consign.html",book=book)

    def post(self):
      user = self.isLogged()
      bid = self.request.get("bid")
      if bid:
          book = Library.get_by_id(int(bid))
      else:
          title = self.request.get("title")
          author = self.request.get("author")
          isbn = self.request.get("isbn")
          if not title:
              self.render("book_consign.html",showErr=True)
              return

          book = UnlistedLibrary(title=title,author=author,isbn=isbn)
          book.put()

      consign_request = ConsignRequest(book=book,user=user)
      consign_request.put()
      self.render("consign_ok.html")

class ConsignBuyHandler(PageHandler):
    def post(self):
      user = self.getUser()
      bid = int(self.request.get("bid"))
      cid = int(self.request.get("cid"))
      needed = self.request.get("needed")

      if not user or not cid or not bid:
        self.response.status_int = 400
        return
      
      parent = Library.get_by_id(bid)
      consigned = ConsignedBook.get_by_id(cid,parent=parent)
      buyConsigned = BuyConsigned(item=consigned,buyer=user,date_needed=needed)
      buyConsigned.put()
      tid = {"tid": buyConsigned.key().id()}
      self.write(json.dumps(tid))

class BookError(PageHandler):
    def get(self):
        self.render("book_error.html")

class TestDb(PageHandler):
    def get(self,pid):
        if pid == '0':
            generalTest()
        elif pid == '1':
            logging.info("Creating initial dummy db")
            generalTest()
        elif pid == '2':
            logging.info("Generating more sell Order")
            generateMoreSellOrder()
        elif pid == '3':
            loadOtherBooks()
        self.redirect("/")

app = webapp2.WSGIApplication([(r'/', HomePage),
                               (r'/register/?',RegisterHandler),
                               (r'/home/?',UserHome),
                               (r'/logout/?',LogoutHandler),
                               (r'/login/?',LoginHandler),
                               (r'/suggest/?',CommentHandler),
                               (r'/search/?',SearchHandler),
                               (r'/testdb/(\d+)/?',TestDb),
                               (r'/user/update/?',UserSettings),
                               (r'/user/orders/?',UserBookOrders),
                               (r'/user/?',UserProfile),
                               (r'/user/consiged/?',UserConsigned),
                               (r'/user/requests/?',UserRequests),
                               (r'/book/info/?',BookInfoHandler),
                               #(r'/book/add/?',AddBookHandler),
                               (r'/book/request/?',RequestBookHandler),
                               (r'/book/consign/?',ConsignBookHandler),
                               (r'/book/consign/buy/?',ConsignBuyHandler),
                               (r'/book/error/?',BookError),
                               (r'/browse/?',BrowseAdsHandler),
                               (r'/about/?',AboutHandler),
                               (r'/about/(\w+)/?',About2Handler),
                               (r'/help/?',HelpHandler),
                               (r'/help/(\w+)/?',Help2Handler),
                               (r'/admin/?',AdminHandler),
                               (r'/admin/blogpost/?',BlogPostHandler),
                               (r'/admin/add/consigned/?',AddConsigneeHandler),
                               (r'/admin/addbook/?',AdminAddBookHandler),
                               (r'/admin/user/search/?',UserSearchHandler),
                               (r'/admin/user/getlist/?',UserListHandler),
                               (r'/admin/getallreqs/?',AllUserRequests),
                               (r'/admin/getallrtc/?',AllUserRTC),
                               (r'/image/(\d+)(\.jpe?g|\.png|\.gif|\.bmp)?/?',ImageServeHandler),
                              ],debug=False)