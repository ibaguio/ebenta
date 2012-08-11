#!/usr/bin/env python
from pagehandlers.PageHandler import *
from database.privacy import *

class UserProfile(PageHandler):
    def get(self):
        usr = self.request.get("usr")   #gets the username of user from url
        try:
            uid = int(usr)
        except:
            uid = None
            pass
        me = self.isLogged()
        if me:  #user is logged in
            me = User.all().filter('username',me).get() #gets my username
        else:
            me = None
        if uid:        #show profile of given uid
            user = User.get_by_id(int(uid))
        elif usr:      #show profile of given user
            user = User.all().filter('username',usr).get()
        else:        #show logged in user's profile
            self.showProfile(me,me)
            return
        self.showProfile(user,me)

    #show the profile of the 'user'
    #me is the dbmodel of the current(loggedin) user
    def showProfile(self,user,me):
        if user:
            if me and me.key().id() == user.key().id():
                user = me
            self.render_noUser('profile.html',user=user,me=me)
        else:
            logging.error("Profile or User does not exist")
            self.render_noUser('profile.html',fail=True,me=me)

class UserSettings(PageHandler):
    def get(self):
        self.redirect("/user")

    def post(self):
        user = self.getUser()
        kind = self.request.get("submit")
        logging.error("kind:"+str(kind))
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
                'college':self.request.get("colelge"),
                'degree':self.request.get("degree")}
        logging.error("info:"+str(info))
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

        if len(error)>0:
            self.response.status_int = 400;
            res = ""
            for e in error:
                res += e +"\n"
            self.write(res)
        else:
            user.put()
            pass #no errors, response with http 200

    def updatePrivacy(self,user):
        info = {'old':self.request.get("old"),
                'new':self.request.get("new"),
                'new2':self.request.get("new2"),
                'priv_college':self.request.get("privacy-college"),
                'priv_contact':self.request.get("privacy-contact")}
        error = []
        logging.error("info:"+str(info))
        change = False  #marker for update db
        if info['old']:
            #check if all input passwords are valid
            if valid_password(info['old']) and valid_password(info['new']) and valid_password(info['new2']):
                if user.correctPass(info['old']):   #user password is correct
                    if info['new'] == info['new2']: #new passwords match
                        user.password = pwHash(user.username,info['new'])
                        change = True   #marker that a change has been made
                    else: error.append("New password does not match")
                else: error.append("Invalid Password Inner")
            else: error.append("Invalid Password Outer")
        logging.error("old:"+str(info["old"]))
        if (info['priv_college'] and info['priv_contact']) not in ["admin","user","guest"]:
            logging.error("Privacy not in list")
            error.append("Privacy not in list")
            return  #error

        #if a change in privacy has been done
        if info['priv_college'] != user.privacy.showCollege or info['priv_contact'] != user.privacy.showContact:
            privacy = getPrivacy(str(info['priv_contact']),str(info['priv_college']))
            user.privacy = privacy
            change = True

        if error:
            self.response.status_int = 401
            logging.error("error:"+str(error))
        elif change:
            user.put()
            self.write("")
            logging.error("response sent")

class UserOrder(PageHandler):
    def post(self):
        username = self.request.get("user")
        rtype = self.request.get("type")

        error = False
        user = User.get_by_key_name(username)
        if not user or rtype not in ["sell","buy"]:
            pass #error
            return
        if rtype == "sell":
            orders = SellBook.all().filter("user",user).order("-posted").fetch(15)
        else:
            orders = BuyBook.all().filter("user",user).order("-posted").fetch(15)

        list_order = []
        for order in orders:
            list_order.append(order.toJson())
        ret = json.dumps(list_order)
        self.write(ret)
        logging.info("order:"+ret)
