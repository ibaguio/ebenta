#!/usr/bin/env python
from pagehandlers.PageHandler import *
import hashlib,json

class SendMessage(PageHandler):
	def post(self):
		info = self.getInfo()
		user_to = User.all().filter("username",info["to"]).get()
		user_from = User.all().filter("username",info["from"]).get()

		if not user_from or not user_to:
			self.response.status_int(400)
			return

		conversation = user_to.conversation_a.get_by_key_id(getConversationHash(user_to,user_from))
		if not conversation:	#create new conversation within users
			conversation = Conversation(userA = user_to,userB = user_from,key=getConversationHash(user_to,user_from))
			conversation.put()

		if not info["title"]:	info["title"]=""
		
		message = Message(title=info["title"], message=info["message"],conversation=conversation,read=False,sender=user_from)
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

	def getConversationHash(*users):
		""" returns the MD5 hash when both user's username has been sorted 
			alphabetically then concatenated """
		assert len(users) == 2
		h = hashlib.md5()
		h.update("".join(users.sorted()))
		return h.hexdigest()

#gets the users conversation/messages
class Messages(PageHandler):
	def post(self):
		limit = 10
		me = self.getUser()
		user = User().get_by_key_id(self.request.get("user"))
		if not user or me != user:
			self.response.status_int(400)
			return

		page = self.request.get("page")
		if not page: page = 1
		offset = (page-1) * 10
		convs,count = me.getConversations(offset=offset,count=True)
		convs_json = []
		for con in convs:
			convs_json.append(con.toJson())

		d ={"conv":convs_json,
			"total":count,
			"page":page}

		self.write(d)