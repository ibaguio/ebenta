#!/usr/bin/env python
from pagehandlers.PageHandler import *

class SendMessage(PageHandler):
	def post(self):
		info = self.getInfo()
		user_to = User.all().filter("username",info["to"]).get()
		user_from = User.all().filter("username",info["from"]).get()
		if not user_to:	#error
			return
		if not info["title"]:
			info["title"]=""
		
		message = Message(title=info["title"], message=info["message"],read=False)
		if not user_from:
			message.setSenderInfo(info["guest-name"],info["guest-email"],info["guest-contact"])
		else:
			message.sent_from = user_from
		message.put()

	def getInfo(self):
		info = {}
		info["title"] = self.request.get("title")
		info["message"] = self.request.get("message")
		info["from"] = self.request.get("from")
		info["to"] = self.request.get("to")
		if not info["from"]:	#guest sent a message
			info["guest-name"] = self.request.get("guest-name")
			info["guest-contact"] = self.request.get("guest-contact")
			info["guest-email"] = self.request.get("guest-email")
		logging.error("info:"+str(info))
		return info