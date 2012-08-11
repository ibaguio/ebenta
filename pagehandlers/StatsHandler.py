#!/usr/bin/env python
from pagehandlers.PageHandler import *
from datetime import datetime

class BookStatsHandler(PageHandler):
	def post(self):
		bid = self.request.get("book")
		try:
			book = Library.get_by_id(int(bid))
		except:
			pass
		stats = {}
		if book:
			stats["newPrice"] = book.brandNewPrice

		stats["totalSold"] = Transaction.all().ancestor(book).count()
		listed = SellBook.all().filter("expire >", datetime.now()).filter("transaction = ",None).ancestor(book)
		buk = SellBook.all().ancestor( Library.all().get()).get()
		sum_ = 0.0
		count =0
		books_listed = listed.fetch(100)
		if listed.count() > 0:
			for book_posted in books_listed:
				count+=1
				sum_ += book_posted.price
			ave = sum_/count
		else:
			ave = 0.0
		stats["avePrice"] = str(round(ave,2))
		stats["listings"] = listed.count()
		logging.info("stats:"+str(stats))
		response = json.dumps(stats)
		self.write(response)