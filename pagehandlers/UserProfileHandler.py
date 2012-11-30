#!/usr/bin/env python
from pagehandlers.PageHandler import *
from database.privacy import *

class UserProfile(PageHandler):
    #only show profile if user is admin
    def get(self):
        me = self.getUser()
        if not me.admin:
            self.redirect("/home#profile")
            return

        usr = self.request.get("user")  #gets the username of user from url
        try:
            uid = User.get_by_key_name(usr).key().id()

        except:
            uid = None
        
        if uid:        #show profile of given uid
            user = User.get_by_id(uid)
        elif usr:      #show profile of given user
            user = User.get_by_key_name(usr)
        else:        #show logged in user's profile
            self.showProfile(me,me)
            return
        self.showProfile(user,me)

    #show the profile of the 'user'
    #me is the dbmodel of the current(loggedin) user
    def showProfile(self,user,me):
        if user:
            if me and me.key() == user.key():
                user = me
            self.render_noUser('profile.html',user=user,me=me)
        else:
            logging.error("Profile or User does not exist")
            self.render_noUser('profile.html',fail=True,me=me)

class UserSettings(PageHandler):
    """ User's settings """
    def get(self):
        self.redirect("/user")

    def post(self):
        user = self.getUser()
        kind = self.request.get("submit")

        if not user:
            self.render("error.html")
            return
        if kind == "settings":
            self.updatePrivacy(user)
        elif kind == "profile":
            self.updateProfile(user)
        else:
            self.render("error.html")

    def updateProfile(self,user):
        info = {'first':self.request.get("first"),
                'last':self.request.get("last"),
                'num':self.request.get("num"),
                'email':self.request.get("email"),
                'college':self.request.get("college"),
                'degree':self.request.get("degree"),
                'dormitory':self.request.get("dormitory")}

        error = []
        if info['first']:
            user.firstName = info['first']
        if info['last']:
            user.lastName = info['last']
        if info['num']:
            if valid_contactNum(info["num"]):
                user.contactNum = info['num']
            else:
                error.append("Invalid Contact Number")
        if info['email']:
            if valid_email(info["email"]):
                user.email = info['email']
            else:
                error.append("Invalid Email")
        if info['college']:
            user.college = info['college']
        if info['degree']:
            user.degree = info['degree']
        if info['dormitory'] and info['dormitory'] in strings.dormitory:
            user.dormitory = info['dormitory']

        if len(error)>0:
            self.response.status_int = 400;
            res = ""
            for e in error:
                res += e +"\n"
            self.write(res)
        else:
            user.put()
            pass #no errors, response with http 200

class UserConsigned(PageHandler):
    """gets the list of consigned books for the user"""
    def post(self):
        if not self.isLogged().admin:
            self.response.status_int = 400
            return

        u = self.request.get("u") #get username
        user = User.get_by_key_name(u)
        if not user:
            self.response.status_int = 400
            return
        consigned = user.consigned_books
        req_consign = user.request_to_consign

        ret = {}
        ret["c"] = []#consigned
        ret["rtc"] = []#request to consign
        for book in consigned:
            ret["c"].append(book.toDict(book_info=True))
        for book in req_consign:
            ret["rtc"].append(book.toDict())

        self.write(json.dumps(ret))

#returns the user's listed requests
class UserRequests(PageHandler):
    def post(self):
        if not self.isLogged().admin:
            self.response.status_int = 400
            return
        
        u = self.request.get("u") #get username
        user = User.get_by_key_name(u)
        if not user:
            self.response.status_int = 400
            return

        requests = user.requested_books
        if requests.count()==0:
            return            
        ret = []
        for req in requests:
            ret.append(req.toDict())

        self.write(json.dumps(ret))