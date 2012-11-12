from pagehandlers.PageHandler import *
#from database.privacy import *

# hompage for guest users
class HomePage(PageHandler):
    def get(self):
        if not self.isLogged():
            self.render_noUser("new_home.html")
        else:   #user is logged in, redir to home
            self.redirect('/home')
    
class UserHome(PageHandler):
    def get(self):
        user = self.isLogged()
        if user:
            news = BlogPost.all().order("-posted").fetch(5)
            self.render('user_home_new.html',username = user,news=news)
        else:
            self.redirect("/")

class RegisterHandler(PageHandler):
    def get(self):
        if self.isLogged():
            self.redirect("/")
            return
        self.render_noUser("register.html",val={},err={})

    #REGISTER form post
    def post(self):
        err,errs,val = self.checkErrors()
        if len(err) > 4: #accidentally pressed register and no input was placed, redir to home
            self.redirect(val['from'])
            return
        elif len(err)>0:
            if val["from"] == '/register':
                self.render("register.html",err=err,errs=errs,val=val)
            else:
                self.render("homepage.html",err=err,errs=errs,val=val)
            return

        new = User(key_name=val['user'].lower(),
                   username = val['user'].lower(),
                   password =  pwHash(val['user'],val['pass']),
                   firstName = val['first'],
                   lastName = val['last'],
                   contactNum = val['con'],
                   email=val['email'])
        new.put()
        #successfully register, auto login the user and redir to home
        cookie = generateCookie(val.get('user'))    #dictionary
        self.setCookies(cookie)
        self.redirect('/home')
        
    #Returns the errors from registration form
    def checkErrors(self):
        val = self.getRegister()
        err = []
        errs = []
        dorms = ['None','Centennial','International Center','Ilang-ilang','Ipil',\
            'Kalayaan','Kamagong','Kamia','Molave','Sampaguita','Sanggumay','Yakal']
        #check if username already in db
        if User.get_by_key_name(val.get('user')):
            err.append("Username already exists!")
            errs.append("uname")
        elif not valid_username(val.get('user')):
            err.append("Invalid Username")
            errs.append("uname")
        if val.get('pass') != val.get('ver'):
            err.append("Passwords must match")
            errs.append("pass")
        elif not valid_password(val.get('pass')):
            err.append("Invalid Password")
            errs.append("pass")
        if not valid_name(val.get('first')):
            err.append("Invalid First Name")
            errs.append("name")
        if not valid_name(val.get('last')):
            err.append("Invalid Last Name")
            errs.append("name")
        if not valid_contactNum(val.get('con')):
            err.append("Invalid Contact Number")
            errs.append("con")
        if not valid_email(val.get('email')):
            err.append("Invalid Email address")
            errs.append("email")
        if val.get('dorm') not in dorms:
            err.append("Invalid Dormitory")
            errs.append("dorm")
        return err,errs,val
    
    #GETS data from register form    
    def getRegister(self):        
        return {'user': self.request.get("username"),
                'pass': self.request.get("pass"),
                'ver':  self.request.get("verify"),
                'first': self.request.get("firstName"),
                'last': self.request.get("lastName"),
                'con':  self.request.get("contactNo"),
                'email': self.request.get("email"),
                'from': self.request.get("from"),
                'dorm': self.request.get('dorm')}