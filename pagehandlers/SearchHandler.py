from pagehandlers.PageHandler import *

class SearchHandler(PageHandler):
    def get(self):
        next = self.request.get("next")
        user =  self.isLogged()
        query = self.request.get("q")
        if query == "" or query == "enter title or author":
            self.redirect("/")
        
        book = self.getBookKey(query)
        #directly redirects to book info page if query matches entire book title
        if book:
            self.redirect("/book/info?book="+str(book.id()))

        results,time = searchBooks(query.lower())
        self.render('search_results.html',
                        results=results,
                        time=self.getTime(time),
                        query=query,
                        resLen=len(results),
                        next=next)

    def getTime(self,time):
        if time > 1:
            ret = "<b>" + str(time)[:4] + "</b> seconds"
        else:
            postfix = ["milli","nano"]
            for i in range(len(postfix)):
                ntime = time*1000
                if ntime > 1:
                    ret = "<b>" + str(ntime)[:6] + "</b> "+postfix[i]+" seconds"
                    break
        return ret

    #checks if the query matches a book
    def getBookKey(self,query):
        return Library.all().filter("title",query).get(keys_only=True)
