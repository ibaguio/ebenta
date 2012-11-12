from pagehandlers.PageHandler import *

class BlogPostHandler(PageHandler):
    def post(self):
        user = self.getUser()
        title = self.request.get("title")
        content = self.request.get("content")

        if user and title and content:
            new_post = BlogPost(title=title,added_by=user,content=content)
            new_post.put()
            self.write("OK POSTED")
        else:
            self.write("NOT POSTED")