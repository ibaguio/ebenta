from utils.regex import *
from utils.search import *
from utils.crypto import *
from database.dbModels import *
from database.test import *
from database.dbModels import *

from google.appengine.ext import db
from google.appengine.api import users

import json
import os
import webapp2
import jinja2
import re
import datetime

#default days before post expires
def_exp_days = 30

# TEMPLATE stuff
template_dir = os.path.join(os.path.dirname("main.py"),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

#jinja custom filters
#returns the url acceptible format for the string
#'The Calculus 7' => 'the-calculus-7'
def toUrl(string):
    if string:
        return "-".join(re.split('\W+',string.strip().lower()))
    else:
        return "other"

def upper_case(string):
    if string:
        return string.upper()
    return ""

jinja_env.filters["upper_case"] = upper_case
jinja_env.filters["toUrl"] = toUrl

# constant globals for jinja
#jinja_env.globals.update(req = '<font style="color:red">*</font>')

# RENDER TEMPLATE
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class PageHandler(webapp2.RequestHandler):
    #shortcut function to write to webpage
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)
    
    #funtions that renders template using given args, sets the user
    def render(self,template,user=None,**kw):
        if not user:
            user = self.getUser()
        self.response.out.write(render_str(template,user=user,**kw))
    
    def render_noUser(self,template,**kw):
        self.response.out.write(render_str(template,**kw))

    def getCookie(self,biscuit):
      return self.request.cookies.get(biscuit)
    
    def logout(self):
        self.response.headers.add_header("Set-Cookie", "user=; Expires=Thu, 01-Jan-1970 00:00:00 GMT")
        self.response.headers.add_header("Set-Cookie", "ver=; Expires=Thu, 01-Jan-1970 00:00:00 GMT")
    
    #takes a dictionary as input and set cookies
    def setCookies(self,d, path = "Path=/;", expire=""):
        for (cookie,value) in d.items():
            biscuit = cookie + "=" + value +";"+ path+expire
            self.response.headers.add_header("Set-Cookie", str(biscuit))
    
    #returns username if user is logged in
    def isLogged(self):
        user = self.getCookie('user')
        ver = self.getCookie('ver')
        if not user or not ver:
            return
        usr = User.get_by_key_name(user)
        if validCookie(ver,user):
            return usr
        self.logout()   #invalid cookie, remove cookie
    
    #returns the db.Model of the current user
    def getUser(self):
        uname = self.getCookie('user')
        if uname:
            return User.all().filter('username',uname).get()
    
    #checks if the user is an admin
    def isAdmin(self):
        u = self.getUser()
        if u: return u.admin

    #redirects back to the referer
    def redirectBack(self):
        self.redirect(self.request.referer)