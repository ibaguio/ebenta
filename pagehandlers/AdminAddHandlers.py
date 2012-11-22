from pagehandlers.PageHandler import *

""" Admin Add Handlers 
    Adds new information posted by admins to database"""

class AddConsigneeHandler(PageHandler):
    """Post request from book_info page"""
    def post(self):
        if not self.isAdmin:
            return
        try:
            user = User.get_by_key_name(self.request.get("uname"))
            ask_price = float(self.request.get("ask-price"))
            sell_price = float(self.request.get("price"))
            rating = int(self.request.get("rating"))
            added_by = User.get_by_key_name(self.request.get("adder"))
            book = Library.get_by_id(int(self.request.get("bid")))

            if not user or not ask_price or not sell_price or not rating or not book or not added_by:
                raise

            new_consigned_book = ConsignedBook(parent=book,consignee=user,added_by=added_by,\
                ask_price=ask_price,rating=rating,price=sell_price)
            new_consigned_book.put()

            #add the image
            img = self.request.get("img")
            ftype = getImageFormat(img)
            if img:
                new_image = Image(ref=new_consigned_book,image=db.Blob(img),ftype=ftype)
                new_image.put()
            self.write("OK added")
        except:
            self.write("NOT ADDED")

class AddBookHandler(PageHandler):
    def get(self):
        if not self.isAdmin:
            return
        self.render("admin/add_book.html")

    def post(self):
        if not self.isAdmin:
            return

        title= self.request.get("title")
        author=self.request.get("author")
        isbn=self.request.get("isbn")
        desc=self.request.get("desc")
        p = self.request.get("brandprice",default_value=-1.0)
        sk = self.request.get("sk").split(',')
        
        try:
            if not p: raise
            else: price = float(p)
        except:
            price = -1.0
        
        if not title or not author:
            return

        newBook = Library(title=title,author=author,isbn=isbn,description=desc,brandNewPrice=price)
        newBook.generateSk()
        if sk:
            for s in sk:
                newBook.addSk(s)
        newBook.put()

        res = """<html><body><pre>
                OK ADDED
                Title:          %(title)s
                Author:         %(author)s
                ISBN:           %(isbn)s
                Description:    %(desc)s
                Brandnew Price: %(bnew)f
                Search Keys:    %(sk)s

                WILL REDIRECT BACK IN ABOUT 3 seconds... 
                <a href='/admin/add/book'>click here to go back</a>
                Note: if brand new price is, -1.0. that means there is No Data

                </pre></body></html>
                <script>window.onload=(function() {
                    setTimeout("location.pathname='/admin/add/book'", 2500);});</script>
                """
        search_keys = ",".join(newBook.searchKeys)
        self.write(res%{"title":title,"author":author,"isbn":isbn,"desc":desc,"bnew":price,"sk":search_keys})

class AddPostHandler(PageHandler):
    def get(self):
        if not self.isAdmin():
            return
        self.render("admin/add_post.html")

    def post(self):
        if not self.isAdmin():
            return
        user = self.getUser()
        title = self.request.get("title")
        content = self.request.get("content")

        if user and title and content:
            new_post = BlogPost(title=title,added_by=user,content=content)
            new_post.put()
            self.redirect("/home")
        else:
            self.write("NOT POSTED")