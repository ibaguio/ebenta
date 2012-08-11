#!/usr/bin/env python
import string, hashlib, random,hmac

#TOP_SECRET="bFPKSPGpUFVBYrlmUwaBvPDixL"
#PASSWORD HASHING
salt_len = 6;   #DO NOT CHANGE THIS
def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(salt_len))
    
def pwHash(name, pw, salt = ""):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s%s' % (h,salt)

def valid_pw(name, pw, true_pass):
    salt = true_pass[-salt_len:]
    if true_pass == pwHash(name,pw,salt):
        return True
    return False

#COOKIE GENERATION
#Token Based auth
''' Cookie Generation Algorithm:
      hashd = hash_str(userSalt(<username>))
      cookie = generateCookie(hashd)
'''
TOP_SECRET="bFPKSPGpUFVBYrlmUwaBvPDixL"

#returns a dict for cookie
def generateCookie(username):
    h = generateHash(username)
    return {'user':username,'ver':h}

def userSalt(username):
    return username[:6]
    
def hash_str(salt):
    return hmac.new(TOP_SECRET,salt).hexdigest()

def split_str(s,p):
    return [ s[i:i+p] for i in range(0,len(s),p)]

def generateHash(username):
    salt = userSalt(username)
    hashd = hash_str(salt)
    cookie=""
    s = split_str(hashd,6)
    for i in range(0,6):
        cookie += s[i] + salt[i]
    return cookie

def extract_cookie(hashd):
    salt = h = ""
    p = 0
    n = [6,13,20,27,34,37]
    for i in range(6):
        salt+= hashd[n[i]]
        h += hashd[p:n[i]]
        p= n[i] + 1
    return salt, h
    
def validCookie(cookie, username):
    if not cookie or not username:
        return False
    username = username[:6]
    if len(cookie)!= 38:
        return False
    user, h = extract_cookie(cookie)
    return hash_str(username) == h and user==username
