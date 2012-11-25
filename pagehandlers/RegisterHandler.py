from pagehandlers.PageHandler import *
from pagehandlers.EmailHandler import EmailHandler

class RegisterHandler(PageHandler):
    def get(self):
        if self.isLogged():
            self.redirect("/")
            return
        self.render_noUser("register.html",val={},err={})

    #REGISTER form post
    def post(self):
        err,errs,val = self.checkErrors()
        logging.info(val)
        if len(err)>0:
            self.render("register.html",err=err,errs=errs,val=val)
            return

        new = User(key_name=val['user'].lower(),
                   username = val['user'].lower(),
                   password =  pwHash(val['user'],val['pass']),
                   firstName = val['first'].title(),
                   lastName = val['last'].title(),
                   contactNum = val['con'],
                   email=val['email'])
        new.put()
        EmailHandler.welcomeUser(new)
        
        #successfully register, auto login the user and redir to home
        cookie = generateCookie(val.get('user'))    #dictionary
        self.setCookies(cookie)
        self.redirect('/home')
        
    #Returns the errors from registration form
    def checkErrors(self):
        val = self.getRegister()
        err = []
        errs = []
        
        if not valid_username(val.get('user')):
            err.append("Invalid Username")
            errs.append("uname")
        elif User.get_by_key_name(val.get('user')):
            #check if username already in db
            err.append("Username already exists!")
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
        if val.get('dorm') not in self.dorms:
            err.append("Invalid Dormitory")
            errs.append("dorm")
        if val.get('college') not in self.colleges:
            err.append("Invalid College")
            errs.append("college")
        if not val.get("course"):
            err.append("Please enter course")
            errs.append("course")
        return err,errs,val

    dorms = ['None','Centennial','International Center','Ilang-ilang','Ipil',\
            'Kalayaan','Kamagong','Kamia','Molave','Sampaguita','Sanggumay','Yakal']
    
    colleges = ['ait', 'asp', 'arki', 'asian', 'cal', 'cba', 'che', 'chk', 'cmc', 'cs',\
        'cssp', 'cswcd', 'econ', 'educ', 'engg', 'fa', 'iis', 'issi', 'law', 'music', 'ncpag',\
        'slis', 'solair', 'surp', 'stat','other']#, 'tmc', 'upis']

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
                'dorm': self.request.get('dorm'),
                'college':self.request.get("college"),
                'course':self.request.get("course")}