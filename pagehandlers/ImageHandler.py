#!/usr/bin/env python
from pagehandlers.PageHandler import *

class ImageServeHandler(PageHandler):
    def get(self,img_id,img_type):
        img = Image.get_by_id(int(img_id))
        if img and img.image:
            self.response.headers['Content-Type'] = "image/"+img.ftype
            self.response.out.write(img.image)
        else:
            self.response.status_int = 404
            self.write("HTTP 404 Not Found")