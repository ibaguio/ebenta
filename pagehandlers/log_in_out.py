#!/usr/bin/env python
from pagehandlers.PageHandler import *

class LoginHandler(PageHandler):
    def get(self):
        if self.getUser():
            self.redirect("/home")
            return
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
                if self.request.referer:
                    self.redirectBack()
                else:
                    self.redirect("/home")
                return
                
        #username or password form is empty, show error
        self.render('login.html',err="Invalid Username and/or Password")
                
    #fetches data from login form
    def getLogin(self):
        x = {'user': self.request.get("uname"),
            'pass': self.request.get("password"),
            'rem':  self.request.get("remember")}
        #logging.info(x)
        return x

class LogoutHandler(PageHandler):
    def get(self):
        if users.get_current_user():
            self.redirect(users.create_logout_url("/"))
            return
        self.logout()
        self.redirect("/")

providers = {
    'Google'   : 'https://www.google.com/accounts/o8/id',
    'Yahoo'    : 'yahoo.com',
    'MySpace'  : 'myspace.com',
    'AOL'      : 'aol.com',
    'MyOpenID' : 'myopenid.com',
    'Twitter' : 'twitter.com'
    # add more here
}

class TestLoginHandler(PageHandler):
    def get(self):
        user = users.get_current_user()
        if user:  # signed in already
            self.response.out.write('Hello <em>%s</em>! [<a href="%s">sign out</a>]' % (
                user.nickname(), users.create_logout_url(self.request.uri)))
        else:     # let user choose authenticator
            self.response.out.write('Hello world! Sign in at: ')
            for name, uri in providers.items():
                self.response.out.write('[<a href="%s">%s</a>]' % (
                    users.create_login_url(federated_identity=uri), name))

class TestGetCredentials(PageHandler):
    def get(self):
        user = users.get_current_user()
        self.write("Username: "+str(user.user_id())+"<br/>Email "+str(user.email())+"<br/>Name: "+str(user.nickname()))

        
'''Login using google/yahoo/twitter
class LoginFederatedHandler(PageHandler):
    def get(self,provider):
        provider=provider.title()
        self.write(provider)
        providers = {
            'Google' : 'https://www.google.com/accounts/o8/id',
            'Yahoo'  : 'yahoo.com',
            'Twtter' : 'twitter.com'
        }
        ver = True#self.request.get("verify")
        if not ver:
            #self.redirect(users.create_login_url("/login/google?verify=True"))
            return
        else:
            user = users.get_current_user()
            if not user:
                self.write(providers[provider])
                self.redirect(users.create_login_url(federated_identity=providers[provider]))
                #self.redirect(users.create_login_url("/login/google?verify=True"))
                return
            else:
                self.write('logged in')
                pass
                #self.write("Username: "+str(user.user_id())+"<br/>Email "+str(user.email())+"<br/>Name: "+str(user.nickname())+"<br/>Admin?"+str(user.is_current_user_admin()))
                #new_user = User(username=user.user_id(),email=user.email(),)
'''