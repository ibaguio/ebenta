from __future__ import with_statement
from pagehandlers.PageHandler import *
from google.appengine.api import files

class UpdateBookList(PageHandler):
    def get(self):
        self.tempUpdaeList()

    def updateList(self):
        books = Library.all().order("title")
        # Create the file
        file_name = files.blobstore.create(mime_type='application/octet-stream')
        # Open the file and write to it
        with files.open(file_name, 'a') as f:
            f.write("[")
            for book in books:
                f.write("\""+book.title+"\",")
            f.write("]")

        # Finalize the file. Do this before attempting to read it.
        files.finalize(file_name)

        # Get the file's blob key
        blob_key = files.blobstore.get_blob_key(file_name)

    def tempUpdaeList(self):
        list_tmp = []
        books = Library.all().order("title")
        logging.info(str(type(books)))
        for b in books:
            logging.info(b.title)
            list_tmp.append(b.title)
        logging.info(list_tmp)
