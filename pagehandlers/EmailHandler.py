from google.appengine.api import mail
from pagehandlers.PageHandler import *

class EmailHandler():
    @classmethod
    def welcomeUser(cls,user):
        sender = "eBenta.com.ph Admin <admin@ebenta.com.ph>"
        subject = "Welcome to eBenta!"
        body = """
Hi %(full_name)s!

Welcome to eBenta.com.ph! Our goal here at eBenta.com.ph is to provide you (and other scholars) a platform where you could purchase and consign(sell) books. We also plan on expanding to other academic materials such as readings. As of now we offer the following services:

Purchasing of used or second hand quality books:
    Purchase books previously used and owned by scholars like yourself, at LOWER prices! Save up to 50%% on you book allowance!!
    Items will be checked by us to ensure quality and your satisfaction.

Purchasing of Brand New Books:
    If you prefer to purchase new books than used ones, well why not? Just request for a brand new copy on the books information page.

Consigning of used books:
    If you are not familiar with the word, consigning is very much like selling, but better. The formal definition of consigning is <i>placing any material in the hand of another, but retaining ownership until the goods are sold or person is transferred.</i> In other words, eBenta.com.ph sells your books for you! Hassle free isn't it? You just 

    How consignment works:
        1. Fill-up the request to consign form in ebenta.com.ph/consign.
        2. Wait for an administrator to contact you regarding your request.
        3. Agree on a price you would like your book to be sold.
        4. Wait for your book to be sold.
        5. Once your book has been sold, you will be notified thru email and/or SMS.
        6. Get your profit from eBenta.com.ph. Yay!
    Note: You may withdraw your consigned item from us anytime.

<font size="-1" style="color:red">This is an autogenerated message. You may reply to this email address to contact our administrators.</font>
""" %{"full_name":user.completeName()}

        mail.send_mail(sender,user.email,subject,body)

