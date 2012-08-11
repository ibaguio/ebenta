#!/usr/bin/env python
from database.dbModels import *

def createDefault():
	privacy = PrivacySetting(key_name="default",showContact="admin",showCollege="admin")
	privacy.put()
	return privacy

def getPrivacy(showContact="admin",showCollege="admin"):
	key = showContact[:2]+showCollege[:2]
	if key == "adad": key="default"
	privacy = PrivacySetting.get_by_key_name(key)
	if not privacy:
		privacy = createPrivacy(key,showContact,showCollege)
	return privacy

def createPrivacy(key,showContact,showCollege,force=False):
	if force:
		p = PrivacySetting.get_by_key_name(key)
		if p: return p
	privacy = PrivacySetting(key_name=key,showContact=showContact,showCollege=showCollege)
	privacy.put()
	return privacy
