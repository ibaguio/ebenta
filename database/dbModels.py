#!/usr/bin/env python
import json,datetime
import re,logging,sys

from google.appengine.ext import db
from utils.crypto import *

#parent definitions
def key(book):
    return db.Key.from_path(book.title,"books")

# DATABASE MODELS
class PrivacySetting(db.Model):
    """show details to:
        admin = admin ONLY
        users = admin and registered users
        guest = everyone"""
    showContact = db.StringProperty(required = True,choices=set(['admin','user','guest']))
    showCollege = db.StringProperty(required = True,choices=set(['admin','user','guest']))

class User(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    firstName = db.StringProperty(required = True)
    lastName = db.StringProperty(required = True)
    contactNum = db.StringProperty()
    email = db.StringProperty()
    studentNum = db.StringProperty()
    joined = db.DateProperty(auto_now_add = True)
    college= db.StringProperty(default="")
    degree= db.StringProperty(default="")
    privacy= db.ReferenceProperty(PrivacySetting,required=True)
    admin = db.BooleanProperty(default=False)
    consignee = db.BooleanProperty(default=False)

    #0 - guest
    #1 - user
    #3 - admin
    def toJson(self,_all=False,viewer=0):
        d ={"username": self.username,
            "image": self.getImage()}
        if _all:    #show all info, subject to viewer and privacy
            d.update({"firstName":self.firstName,
                    "lastName":self.lastName,
                    "admin":self.admin,
                    "consignee":self.consignee})
            if (viewer == 0 and self.privacy.showContact == "guest")\
                or (viewer == 1 and self.privacy.showContact in ["user","guest"])\
                or viewer == 3:
                    d["contactNum"] = self.contactNum
                    d["email"] = self.email
            if (viewer == 0 and self.privacy.showContact == "guest")\
                or (viewer == 1 and self.privacy.showContact in ["user","guest"])\
                or viewer == 3:
                    d["college"] = self.college
                    d["degree"] = self.degree
        return json.dumps(d)
    
    def completeName(self):
        return self.lastName +", "+self.firstName

    def correctPass(self,raw_pass):
        return valid_pw(self.username, raw_pass, self.password)#check crypto.py

    #returns current profile pic
    def getImage(self):
        return "/static/images/no_profile_pic.jpg"

class Image(db.Model):
    entity = db.ReferenceProperty(required=True)
    image = db.BlobProperty(required=True)
    comment = db.StringProperty(default="")
    posted = db.DateTimeProperty(auto_now_add=True)

class Library(db.Model):
    """ The Library is a 'table' that stores all the books i call
    it Library because somehow it contains the (list of) books """
    title = db.StringProperty(required = True)
    author = db.StringProperty()
    isbn = db.StringProperty(default="")
    searchKeys = db.StringListProperty()
    description = db.StringProperty(default="")
    brandNewPrice = db.FloatProperty(default=-1.0);

    def generateSk(self):
        try:
            k = re.split('\W+',self.title.lower()) + re.split('\W+',self.author.lower())
            self.searchKeys = k
        except BaseException as e:
            logging.error("generate SK error")
            err = sys.exc_info()
        
    def addSk(self, *keys):
        for k in keys:
            self.searchKeys.append(k)

class Feedback(db.Model):
    comment = db.StringProperty(required=True)
    rating = db.StringProperty(required=True,choices=["positive","neutral","negative"])
    posted = db.DateTimeProperty(auto_now_add=True)

class Transaction(db.Model):
    buyer = db.ReferenceProperty(User,required=True,collection_name="transactions_bought")
    seller = db.ReferenceProperty(User,required=True,collection_name="transactions_sold")
    price = db.FloatProperty(required=True)
    #feedback to seller: i.e buyer's rating of seller
    fback_seller = db.ReferenceProperty(Feedback,collection_name="seller_feedback")
    #feedback to buyer: i.e seller's rating of buyer
    fback_buyer = db.ReferenceProperty(Feedback,collection_name="buyer_feedback")
   
#ads for buying
class BuyBook(db.Model):
    user = db.ReferenceProperty(User,required = True)
    rating = db.RatingProperty(required = True)
    price = db.FloatProperty(required = True)
    comment = db.StringProperty() #Remember 500char limit
    posted = db.DateTimeProperty(auto_now_add = True)
    expire = db.DateTimeProperty()
    transaction = db.ReferenceProperty(Transaction, default=None)

    def toJson(self):
        book = self.parent()
        d = {"title": book.title,
             "author": book.author,
             "bid": book.key().id(),
             "isbn": book.isbn,
             "rating": self.rating,
             "price": self.price,
             "comment":self.comment,
             "posted": self.posted.strftime("%B %d, %Y")}
        return json.dumps(d)

    #returns the unexpired listings
    @classmethod
    def getListings(cls,book,limit=30,offset=0,order="-posted",count_only=False,count=False,filterExpire=True):
        q = cls.all()
        q.ancestor(book)
        q.order("-expire")  #error w/o this
        if filterExpire:
            q.filter("expire >",datetime.datetime.now())
        q.order(order)
        if count_only:
            return q.count()
        if count:   #include count in return, returns a tuple, see comment below
            return (q.fetch(limit=limit,offset=offset), q.count())
        else:
            return q.fetch(limit=limit,offset=offset)

#ads books for sale
class SellBook(db.Model):
    user = db.ReferenceProperty(User,required = True)
    rating = db.RatingProperty(required = True)
    price = db.FloatProperty(required = True)
    comment = db.StringProperty() #Remember 500char limit
    posted = db.DateTimeProperty(auto_now_add = True)
    expire = db.DateTimeProperty()
    transaction = db.ReferenceProperty(Transaction, default=None)

    def toJson(self, userInfo=False):
        book = self.parent()
        d = {"title": book.title,
             "author": book.author,
             "bid": book.key().id(),
             "isbn": book.isbn,
             "rating": self.rating,
             "price": str(self.price),
             "comment":self.comment,
             "posted": self.posted.strftime("%B %d, %Y")}
        d["user"] = self.user.toJson()
        logging.error("user json:"+str(d["user"]))

        return json.dumps(d)

    #returns all of the sell listings for a given book
    @classmethod
    def getListings(cls,book,limit=30,offset=0,order="-posted",count_only=False,count=False,filterExpire=True):
        logging.error("getListings order by: "+order)
        q = cls.all()
        q.ancestor(book)
        q.order(order)
        #q.order("-expire")  #error w/o this
        if filterExpire:
            #q.filter("expire >",datetime.datetime.now())
            pass
        if count_only:
            return q.count()
        if count:    #include count in return, returns a tuple, see comment below
            return (q.fetch(limit=limit,offset=offset), q.count())
        else:
            return q.fetch(limit=limit,offset=offset)
#send message
class Message(db.Model):
    title = db.StringProperty()
    message = db.TextProperty(required=True)
    read = db.BooleanProperty(required=True)
    sent_from = db.ReferenceProperty(User)  #if the sender is logged in, reference him
    sent_from_info = db.StringListProperty()
    posted = db.DateTimeProperty(auto_now_add=True)

    def setSenderInfo(self,name,email,contactNum):
        self.sent_from_info.append(name)
        self.sent_from_info.append(email)
        self.sent_from_info.append(contactNum)

class Comment(db.Model):
    user = db.ReferenceProperty(User, required=True)
    comment = db.TextProperty(required=True)
    posted = db.DateTimeProperty(auto_now_add = True)

class Colleges(db.Model):
    abbr = db.StringProperty(required=True)#abbriviation
    college = db.StringProperty(required=True)

class DegreeCourse(db.Model):
    degree = db.StringProperty(required=True)
    college = db.ReferenceProperty(Colleges,required=True)


'''if i return a non-tuple, (i.e q.fetch(...),q.count()) 
python would match every item returned in fetch to count 
(i.e item1,q.count, item2,q.count ...) which would return error'''