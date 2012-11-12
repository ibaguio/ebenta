#!/usr/bin/env python
import json,datetime
import re,logging

from google.appengine.ext import db
from utils.crypto import *
from utils import strings

# DATABASE MODELS
class User(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True,indexed=False)
    firstName = db.StringProperty(required = True)
    lastName = db.StringProperty(required = True)
    contactNum = db.StringProperty()
    email = db.StringProperty()
    studentNum = db.StringProperty()
    joined = db.DateProperty(auto_now_add = True)
    dormitory = db.StringProperty(required=True,\
        choices=set(strings.dormitory),default="None")
    college= db.StringProperty(default="")
    degree= db.StringProperty(default="")
    admin = db.BooleanProperty(default=False)

    #0 - guest  1 - user  3 - admin (AND YES ITS 3)
    def toJson(self,_all=False,viewer=0):
        d ={"username": self.username,
            "image": self.getImage(),
            "score": self.score,
            "firstName":self.firstName,
            "lastName":self.lastName,
            "admin":self.admin,
            "consignee":self.consignee,
            "contactNum":self.contactNum,
            "email":self.email,
            "college":self.college,
            "degree":self.degree}
        return json.dumps(d)
    
    def completeName(self):
        return self.lastName +", "+self.firstName

    def correctPass(self,raw_pass):
        return valid_pw(self.username, raw_pass, self.password)#check crypto.py

    #returns current profile pic
    def getImage(self):
        return "/static/images/no_profile_pic.jpg"

class Image(db.Model):
    ref = db.ReferenceProperty(required=True,collection_name="images")
    image = db.BlobProperty(required=True)
    ftype = db.StringProperty(required=True,indexed=False)
    comment = db.StringProperty(default=None,indexed=False)
    posted = db.DateTimeProperty(auto_now_add=True)

    def getUrl(self):
        return "/image/"+str(self.key().id())+"."+ftype


class Author(db.Model):
    name = db.StringProperty(required=True)

class Library(db.Model):
    """ The Library is a 'table' that stores all the books i call
    it Library because somehow it contains the (list of) books """
    title = db.StringProperty(required = True)
    #author_ = db.ReferenceProperty(Author,collection_name="books")
    author = db.StringProperty()
    isbn = db.StringProperty(default="")
    searchKeys = db.StringListProperty()
    description = db.StringProperty(default="",indexed=False)
    brandNewPrice = db.FloatProperty(default=-1.0,indexed=False);

    #returns a json representation of a specific book
    #title, author, key, + attributes specified in kwargs
    def toJson(self,**kwargs):
        d ={"title":self.title,
            "author":self.author,
            "key":self.key().id()}
        if kwargs['image']:
            d['image'] = self.getImage()
        for args in kwargs:
            try:
                att = getattr(self,args)
            except: continue
            if att:
                d[args] = att
        return json.dumps(d)

    #generates a list of Search keys for book
    def generateSk(self):
        try:
            k = re.split('\W+',self.title.lower()) + re.split('\W+',self.author.lower())
            self.searchKeys = k
        except BaseException as e:
            pass
        
    def addSk(self, *keys):
        for k in keys:
            self.searchKeys.append(k)

    def getImage(self):
        img = self.images.get()
        if not img: return
        return "/image/"+str(img.key().id())+'.'+str(img.ftype)

    @classmethod
    def getListings(cls,limit=15,offset=0,order="title",count_only=False,count=False):
        q = cls.all()
        q.order(order)
        if count_only:
            return q.count()
        ret = q.fetch(limit=limit,offset=offset)
        if count:
            return ret, q.count()
        return ret

    #returns a dict containing the stats of the book
    def getStats(self):
        stats = {}
        stats["newPrice"] = self.brandNewPrice
        if stats["newPrice"] <= 0:
            stats["newPrice"] = "No Data"

        tsold = ConsignedBook.all().ancestor(self).filter("completed=",True).count()
        if tsold == 0:
            stats["totalSold"] = "None yet"
        elif tsold == 1:
            stats["totalSold"] = "1 copy"
        elif tsold > 1:
            stats["totalSold"] = str(tsold) + " copies"

        #get the listed consigned books
        listed = ConsignedBook.all().ancestor(self).filter("completed",False)
        sum_ = 0.0
        count = 0
        books_listed = listed.fetch(50)
        #get the average price for the last 50 listed books
        if listed.count() > 0:
            for book_posted in books_listed:
                count+=1
                sum_ += book_posted.price
            ave = sum_/count
            stats["avePrice"] = str(round(ave,2))
        else:
            stats["avePrice"] = "No Data"

        stats["listed"] = listed.count()
        return stats

#books that are added by users and would not be shown on browse
class UnlistedLibrary(db.Model):
    title = db.StringProperty(required=True)
    author = db.StringProperty(required=True)
    isbn = db.StringProperty()

class ConsignedBook(db.Model):
    """ consignee - owner of book
        added_by - admin who added the book
        ask_price - amount that the consignee gets when the book is sold
        price - price that the item is sold for
        rating - item quality rating
        expire - consignment expiry
        posted - date posted """
    consignee = db.ReferenceProperty(User,required=True,collection_name="consigned_books")
    added_by = db.ReferenceProperty(User,required=True,collection_name="consigned_books_added")
    status = db.StringProperty(default="posted",choices=set(["posted","processing","tbd","delivered","completed"]))
    ask_price = db.FloatProperty(required=True)
    price = db.FloatProperty(required=True)
    rating = db.RatingProperty(required=True)
    completed = db.BooleanProperty(default=False)
    posted = db.DateTimeProperty(auto_now_add=True)

    def toJson(self,book_info=False,**kwargs):
        return json.dumps(self.toDict(book_info,**kwargs))

    def toDict(self,book_info=False,**kwargs):
        book = self.parent()
        d = {'added_by':self.added_by.username,
             'rating':self.rating,
             'posted':self.posted.strftime("%B %d, %Y"),
             'price':self.price,
             'ask_price':self.ask_price,
             'cid':self.key().id(),
             'status':self.status}
        d.update(kwargs)
        i = Image.all().ancestor(self).get()
        if i:
            d["img_url"] = i.getUrl()
        else:
            d["img_url"] = "/images/noimage"
        if book_info:
            d.update({'title':book.title,'author':book.author,'bid':book.key().id(),})
        return d

    @classmethod
    def getListings(cls,book,limit=30,offset=0,order="-posted",count=False,listings=True):
        q = cls.all().ancestor(book).order(order)
        ret = q.fetch(limit=limit,offset=offset)
        if count and listings:
            return (ret, q.count())
        elif count and not listings:
            return q.count()
        else:
            return ret

class RequestedBook(db.Model):
    user = db.ReferenceProperty(User,required=True,collection_name="requested_books")
    brand_new = db.BooleanProperty(default=True)
    max_price = db.FloatProperty(required=True)
    min_rating = db.RatingProperty(required=True)
    status = db.StringProperty(default="pending",choices=set(["pending","processing","tbd","delivered","completed"]))
    posted = db.DateTimeProperty(auto_now_add=True)
    date_needed = db.StringProperty()
    completed = db.BooleanProperty(required=True,default=False)
    requests = db.StringProperty()

    def toJson(self):
        return json.dumps(self.toDict())

    def toDict(self):
        book = self.parent()
        d = {'title':book.title,
             'author':book.author,
             'bid':book.key().id,
             'max_price':self.max_price,
             'min_rating':self.min_rating,
             'posted':self.posted,
             'completed':self.completed,
             'requests':self.requests}
        return d

    @classmethod
    def getListings(cls,book,limit=30,offset=0,order="=posted",count=False,listings=True):
        q = cls.all().ancestor(book).order(order)
        ret = q.fetch(limit=limit,offset=offset)
        if count and listings:
            return (ret, q.count())
        elif count and not listings:
            return q.count()
        else:
            return ret

class BuyConsigned(db.Model):
    item = db.ReferenceProperty(ConsignedBook, required=True)
    buyer = db.ReferenceProperty(User, required=True, collection_name="buying_book")
    date_needed = db.StringProperty()

class BlogPost(db.Model):
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    added_by = db.ReferenceProperty(User,collection_name="blog_posts")
    posted = db.DateTimeProperty(auto_now_add=True)

#contains messages from 2 users
class Conversation(db.Model):
    userA = db.ReferenceProperty(User,required=True,collection_name="conversation_a") #receiver
    userB = db.ReferenceProperty(User,required=True,collection_name="conversation_b") #sender
    updated = db.DateTimeProperty(auto_now_add=True)

    def getMessages(self):
        messages = self.messages.order("-posted")
        return messages

    def toJson(self):
        data = {"usr1":userA.username,
                "usr2":userB.username,
                "updated":updated}
        return json.dumps(data)

#message from user to user
class Message(db.Model):
    title = db.StringProperty()
    message = db.TextProperty(required=True)
    read = db.BooleanProperty(required=True)
    #the conversation where this message is linked to
    conversation = db.ReferenceProperty(Conversation,collection_name="messages")
    sender = db.ReferenceProperty(User)  #if the sender is logged in, reference him

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