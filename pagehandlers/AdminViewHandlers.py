from pagehandlers.PageHandler import *
from google.appengine.ext.db import GqlQuery

""" Admin View Handlers 
    Serves requests to view database"""

def get_tmp(req,cat):
    if cat == "book":
        return req.parent().title
    elif cat == "user":
        return req.user.username
    elif cat == "status":
        return req.status.title()
    else:
        return req.posted.strftime("%B %d, %Y")

class ViewRequestsHandler(PageHandler):
    """Handles displaying of all book requests"""
    def get(self):
        if not self.isAdmin:
            return
        
        try:
            cat = self.request.GET["cat"]
            if cat not in ["date","user","book","date","status"]: raise
        except:
            cat = "date"

        all_req = RequestedBook.all().fetch(1000)
        sorted_ = {}
        ref_ = []
        tmp = None    
        
        for req in all_req:
            tmp = get_tmp(req,cat)
            if tmp not in sorted_:
                sorted_[tmp] = []
                ref_.append(tmp)
            sorted_[tmp].append(req)

        self.render("admin/view_requests.html",requests=sorted_,group=cat,reference=ref_)

class ViewRTCHandler(PageHandler):
    """Handles displaying of all Request to 
        Consign (RTC) requests"""
    def get(self):
        if not self.isAdmin():
            return

        try:
            cat = self.request.GET["cat"]
            if cat not in ["date","user","book","date","status"]: raise
        except:
            cat = "date"

        all_rtc = ConsignRequest.all().fetch(1000)
        sorted_ = {}
        ref_ = []
        tmp = None    
        
        for req in all_rtc:
            tmp = get_tmp(req,cat)
            if tmp not in sorted_:
                sorted_[tmp] = []
                ref_.append(tmp)
            sorted_[tmp].append(req)

        self.render("admin/view_rtc.html",all_rtc=sorted_,group=cat,reference=ref_)


class ViewUsersHandler(PageHandler):
    """Handles displaying list all registered users"""
    def get(self):
        if not self.isAdmin():
            return
        s = None
        try:
            q = self.request.GET["search"]
            if q:
                self.user_search(q)
                return
        except:
            pass

        sort_dict ={"user":"username",
                    "last":"lastName",
                    "first":"firstName",
                    "email":"email",
                    "date":"joined"}

        try:
            s = self.request.GET["sort"]
            if not s:raise
        except: 
            s = "user"

        sort = sort_dict[s]

        q = User.all().order(sort)
        count = q.count()
        all_users = q.fetch(1000)

        self.render("admin/view_users.html",all_users=all_users,count=count,sort=s)
    
    #searches for a user or users
    def user_search(self,query):
        qlist = []
        if query == "all":
            self.redirect("/admin/view/users")
            return 
        for q in query.strip().split():
            try:
                r = User.get_by_key_name(q)
                if r:
                    qlist.append(r)
                    break
                qlist.extend(GqlQuery('SELECT * FROM User WHERE firstName = :1',q).fetch(40))
                qlist.extend(GqlQuery('SELECT * FROM User WHERE lastName = :1',q).fetch(40))
            except Exception, e:
                pass
        self.render("admin/view_users.html",all_users=qlist,count=len(qlist),query=query)