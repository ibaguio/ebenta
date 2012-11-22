from pagehandlers.PageHandler import *

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
            self.render('user_home.html',username = user,news=news)
        else:
            self.redirect("/")

