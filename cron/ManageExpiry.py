from database.dbModels import *
import webapp2
import logging
import datetime

class UpdateExpiry(webapp2.RequestHandler):
    """Cron job to check for sell orders' expiry date, 
    and marks those who are expired"""
    def get(self):
        logging.info("Updating Expiry Sell Order Expiry")
        query = db.Query(SellBook)
        query.filter("expired",False)
        count = query.count()
        books = query.fetch(count)
        marked = 0
        date_today = datetime.datetime.now()    #get current date
        for book in books:
            if date_today >= book.expiry_date:
                book.expired = True
                book.put()
                marked+=1
        res = "Marked %d orders as expired"%(marked)
        logging.info("EXPIRY UPDATED: "+res)
        self.response.write("Successfully updated expiry index<br/>"+res)
