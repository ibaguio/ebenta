#!/usr/bin/env python
from pagehandlers.PageHandler import *

class LoginHandler(PageHandler):
    def get(self):
        self.render('login.html')
        
    def post(self):
        val = self.getLogin()
        
        #check if valid user pass combination
        if valid_username(val.get('user')) and valid_password(val.get('pass')):
            user = User.all().filter('username',val.get('user').lower()).get()  #fetch the user from db
            if  user and user.correctPass(val.get('pass')):
                expire=""   #set expire to empty, default cookie,deletes after session
                if val['rem']:  #user has checkd remember box, set expire to 2014
                    expire = "Expires=Thu, 01-Jan-2014 00:00:00 GMT;"

                #login the user
                cookie = generateCookie(val.get('user'))    #dictionary
                self.setCookies(cookie,expire = expire)
                self.redirect('/home')
                return
                
        #username or password form is empty, show error
        self.render('login.html',err="Invalid Username and/or Password")
                
    #fetches data from login form
    def getLogin(self):
        x = {'user': self.request.get("uname"),
            'pass': self.request.get("password"),
            'rem':  self.request.get("remember")}
        logging.error(x)
        return x

class LogoutHandler(PageHandler):
    def get(self):
        self.logout()
        self.redirect("/")
