#!/usr/bin/env python
from pagehandlers.PageHandler import *

class ConsigneeHandler(PageHandler):
	def get(self):
		user = self.getUser()
		if not user or not user.consignee:
			self.redirect("/")
			return

		self.render("consignee.html",user=user,consign_active=True)