#!/usr/bin/env python
from pagehandlers.PageHandler import *
import datetime

#similar proccess with BuyHandler, check BuyHandler docu #tamad
class SellHandler(PageHandler):
    def get(self,step=""):
        user =  self.isLogged()
        if not user:
            self.render_noUser("loggedout.html")
            return
        if step == "":
            self.redirect("/sell/step1")
        elif step[-1] == '1':
            self.render("sell_step.html", step=1,sell_active="active")
        elif step[-1] == '2':
            self.render("sell_step.html", step=2,sell_active="active")
        elif step[-1] == '3':
            bid = self.request.get("book")
            if not bid:
                self.redirect('/sell/step1')
                return
            book = [getBook(bid)]
            self.render("sell_step.html", step=3, book=book,sell_active="active")
        elif step[-1] == '4':
            bid = self.request.get("book")
            book=[]
            if bid:
                book = getBook(bid)
            self.render("sell_step.html", step=4,book=book,sell_active="active")
        else:
            self.redirect('/sell')
    
    #new sell order
    def post(self):
        comments = self.request.get("comment")
        price = self.request.get("price")
        try:
            bid = int(self.request.get("bid"))
            rating = int(self.request.get("rating"))
            book = Library.get_by_id(bid)
            user = self.getUser()
            if not book or not user: 

                raise
        except:
            self.redirect('/sell/error')
            return

        errors=[]
        if rating not in range(1,6):
            errors.append("Invalid Rating Score")
            
        if not valid_price(price):
            errors.append("Price must be of the format: xxxxx.xx")
        
        if len(errors)>0:
            self.render("sell_step.html",step=3,book=[book],errors=errors,rating=rating)
        else:
            new_ad = SellBook(user = user,
                          price = float(price),
                          rating= rating,
                          parent = book,
                          expiry_date = datetime.datetime.now() + datetime.timedelta(days=def_exp_days))
            if comments:
                new_ad.comment=comments
            new_ad.put()

            #get images
            images = []
            img = self.request.get("img1")
            if img: images.append(img)
            img = self.request.get("img2")
            if img: images.append(img)
            img = self.request.get("img3")
            if img: images.append(img)
            
            logging.info("images len:"+str(len(images)))
            for image in images:
                ftype = self.getImageFormat(image)
                logging.info("image type:"+str())
                new_image = Image(image=db.Blob(image),ref=new_ad,ftype=ftype)
                new_image.put()
            
            self.redirect('/sell/step4?book='+str(bid))

    #returns the image format
    def getImageFormat(self, image):
        if image[1:4] == 'PNG': return 'image/png'
        if image[0:3] == 'GIF': return 'image/gif'
        if image[6:10] == 'JFIF': return 'image/jpeg'
        return None