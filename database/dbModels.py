#!/usr/bin/env python
import json,datetime
import re,logging

from google.appengine.ext import db
from utils.crypto import *

#parent definitions
def key(book):
    return db.Key.from_path(book.title,"books")

# DATABASE MODELS

class Unique(db.Model):
  @classmethod
  def check(cls, scope, value):
    def tx(scope, value):
      key_name = "U%s:%s" % (scope, value,)
      ue = Unique.get_by_key_name(key_name)
      if ue:
        raise UniqueConstraintViolation(scope, value)
      ue = Unique(key_name=key_name)
      ue.put()
    db.run_in_transaction(tx, scope, value)
class UniqueConstraintViolation(Exception):
  def __init__(self, scope, value):
    super(UniqueConstraintViolation, self).__init__("Value '%s' is not unique within scope '%s'." % (value, scope, ))


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
    score = db.IntegerProperty(default=0)

    #0 - guest  1 - user  3 - admin (AND YES ITS 3)
    def toJson(self,_all=False,viewer=0):
        logging.info("viewer:"+str(viewer))
        d ={"username": self.username,
            "image": self.getImage(),
            "score": self.score}
        if _all:    #show all info, subject to viewer and privacy
            d.update({"firstName":self.firstName,
                    "lastName":self.lastName,
                    "admin":self.admin,
                    "consignee":self.consignee})
        if (viewer == 0 and self.privacy.showContact == "guest")\
            or (viewer == 1 and self.privacy.showContact in ["user","guest"])\
            or viewer == 3:
                logging.info("here")
                d["contactNum"] = self.contactNum
                d["email"] = self.email
        if (viewer == 0 and self.privacy.showCollege == "guest")\
            or (viewer == 1 and self.privacy.showCollege in ["user","guest"])\
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

    def getConversations(self,limit=10,offset=0,order="-updated",count=False):
        qA = self.conversation_a.order(order)
        qB = self.conversation_b.order(order)

        count = qA.count() + qB.count()

        conA,conB = qA.fetch(10+offset), qB.fetch(10+offset)

        if not conA and not conB:
            return
        elif not conA:
            return conB
        else:
            return conA

        if len(conA) < len(conB):
            conA,conB = conB,conA

        for i in len(conB):
            for v in len(conA):
                if v > limit: continue
                if conB[i].posted > conA[i].posted:
                    conA.insert(v,conB[i])
        return conA[offset:10]

class Image(db.Model):
    ref = db.ReferenceProperty(collection_name="images")
    image = db.BlobProperty(required=True)
    comment = db.StringProperty(default=None)
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
        return None

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

        tsold = Transaction.all().ancestor(self).count()
        if tsold == 0:
            stats["totalSold"] = "None yet"
        elif tsold == 1:
            stats["totalSold"] = "1 copy"
        elif tsold > 1:
            stats["totalSold"] = str(tsold) + " copies"

        #get the listed books
        listed = SellBook.all().filter("expired", False).filter("transaction =",None).ancestor(self)
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
    expired = db.BooleanProperty(default=False)
    expiry_date = db.DateTimeProperty(required=True)
    transaction = db.ReferenceProperty(Transaction, default=None)

    #creates a json representation for the order instance
    def toJson(self, viewer):
        book = self.parent()
        d = {#"title": book.title,
             #"author": book.author,
             #"bid": book.key().id(),
             #"isbn": book.isbn,
             "sellid": self.key().id(),
             "rating": self.rating,
             "price": str(self.price),
             "comment":self.comment,
             "posted": self.posted.strftime("%B %d, %Y")}
        d["user"] = self.user.toJson(viewer=viewer)
        logging.info(str(d))
        return json.dumps(d)

    #returns all of the sell listings for a given book
    @classmethod
    def getListings(cls,book,limit=30,offset=0,order="-posted",count_only=False,count=False,filterExpire=True):
        q = cls.all()
        q.ancestor(book)
        q.order(order)
        if filterExpire:    #if true, do not include in query expired listings
            q.filter("expired",False)
        if count_only:
            return q.count()
        ret = q.fetch(limit=limit,offset=offset)
        if count:    #include count in return, returns a tuple, see comment below
            return (ret, q.count())
        else:
            return ret
    
    #sets the expiry date of the sellorder
    def setExpire(self, days, extend=False):
        if extend:
            base_date = self.expire_date
            self.expired = False
        else:
            base_date = self.posted
        new_exp_date = base_date + datetime.timedelta(days=days)
        self.expire_date = new_exp_date
        self.put()

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

'''if i return a non-tuple, (i.e q.fetch(...),q.count()) 
python would match every item returned in fetch to count 
(i.e item1,q.count, item2,q.count ...) which would return error'''

#docs for all getListings 
""" for BuyBook and SellBook
    book                instance of book from Library
    filterExpire        set yes to fetch only unexpired books
    
    for ALL (including Library)
    limit               maximum number of objects to fetch
    offset              offset to fetch, i.e how many objects to discard before
                        returning the first object
    order               the attribute to be sorted
    count_only          set to true if only get the count of the query
    count               set to true if also return the count of the query"""
