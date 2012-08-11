#!/usr/bin/env python
from utils.crypto import *
from database.dbModels import *
from utils.regex import *
from utils.search import *
from database.dbModels import *
from database.test import *

import json
import os
import webapp2
import jinja2

# TEMPLATE
template_dir = os.path.join(os.path.dirname("main.py"),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

# constant globals for jinja
# these are the red * in required fields
jinja_env.globals.update(req = '<font style="color:red">*</font>')
jinja_env.globals.update(req2 = '<label style="color:red;">*<font size="2">Required</font></label>')

# RENDER TEMPLATE
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class PageHandler(webapp2.RequestHandler):
    #shortcut function to write to webpage
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)
    
    #funtions that renders template using given args
    def render(self,template,**kw):
        self.response.out.write(render_str(template,user=self.getUser(),**kw))
    
    def render_noUser(self,template,**kw):
        self.response.out.write(render_str(template,**kw))

    def getCookie(self,biscuit):
      return self.request.cookies.get(biscuit)
    
    def logout(self):
        self.response.headers.add_header("Set-Cookie", "user=; Expires=Thu, 01-Jan-1970 00:00:00 GMT")
        self.response.headers.add_header("Set-Cookie", "ver=; Expires=Thu, 01-Jan-1970 00:00:00 GMT")
    
    #takes a dictionary as input
    def setCookies(self,d, path = "Path=/;", expire=""):
        for (cookie,value) in d.items():
            biscuit = cookie + "=" + value +";"+ path+expire
            self.response.headers.add_header("Set-Cookie", str(biscuit))
        logging.error("bis: "+biscuit)
    
    #returns username if user is logged in
    #Note: does not verify if user is a valid user, or the verification cookie is valid
    def isLogged(self):
        user = self.getCookie('user')
        ver = self.getCookie('ver')
        if not user or not ver:
            return
        if validCookie(ver,user):
            return user
        self.logout()   #invalid cookie, remove cookie
    
    #returns the db.Model of the current user 
    def getUser(self):
        uname = self.getCookie('user')
        if uname:
            return User.all().filter('username',uname).get()