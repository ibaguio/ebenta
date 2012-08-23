#!/usr/bin/env python
from pagehandlers.PageHandler import *

class AdminHandler(PageHandler):
	def get(self):
		user = self.getUser()
		if not user or not user.admin:
			self.redirect("/")
			return

		self.render("admin.html",user=user,admin_active="active")