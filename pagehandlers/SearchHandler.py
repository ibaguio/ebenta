from pagehandlers.PageHandler import *

class SearchHandler(PageHandler):
    def get(self):
        query = self.getQuery().strip() #remove trailing whitespaces
        if "user" in query and self.isAdmin():
            q = re.split("\W+",query)
            q.pop(q.index("user"))
            logging.info(q)
            self.redirect("/admin/view/users?search="+"+".join(q))
        if not query:
            self.render("search.html")
        if type(query) == unicode:
            self.basicSearch(query)
        elif type(query) == dict:
            self.advanceSearch(query)
        else:
            self.response.status_int = 404

    def basicSearch(self,query):
        user =  self.isLogged()
        if query == "":
            self.redirect(self.request.referer)
            return

        book = self.getBookKey(query)
        #directly redirects to book info page if query matches entire book title
        if book:
            self.redirect("/book/info?book="+str(book.id()))
            return

        results,time = searchBooks(query.lower())
        self.render('search_result.html',
                        results=results,
                        time=self.getTime(time),
                        query=query,
                        resLen=len(results))

    def advanceSearch(self,query):
        pass

    def getTime(self,time):
        if time > 1:
            ret = "<b>" + str(time)[:4] + "</b> seconds"
        else:
            postfix = ["milli","nano"]
            for i in range(len(postfix)):
                ntime = time*1000
                if ntime > 1:
                    ret = "<b>" + str(ntime)[:6] + "</b> "+postfix[i]+"seconds"
                    break
        return ret

    #checks if the query matches a book, returns the key only
    def getBookKey(self,query):
        return Library.all().filter("title",query).get(keys_only=True)

    def getQuery(self):
        qtype = self.request.get("query-type")
        if qtype != "advanced":
            return self.request.get("q").lower()
        else:
            return {"sub-category":self.request.get("sub-category"),
                    "title":self.request.get("title"),
                    "author":self.request.get("author"),
                    "isbn":self.request.get("isbn")}