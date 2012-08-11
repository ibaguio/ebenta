import re
import logging

# REGEX
USER_RE = re.compile(r"^[a-zA-Z0-9_\.-]{6,15}$")
PASS_RE = re.compile(r"^.{6,20}$")
NAME_RE = re.compile(r"^[a-zA-Z ]+$")
PRICE_RE = re.compile(r"^(\d)+(\.[0-9]{2})?")
CONTACTNO_RE = re.compile(r"^[0-9\ 	]{11,14}$")
EMAIL_RE = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)
#email_re source http://stackoverflow.com/questions/3217682/checking-validity-of-email-in-django-python

def valid_username(username):
    return username and USER_RE.match(username)

def valid_name(name):
    return name and NAME_RE.match(name)

def valid_password(password):
    logging.error("password:"+password+"x:"+str(PASS_RE.match(password)))
    return password and PASS_RE.match(password)

def valid_contactNum(num):
    return num and CONTACTNO_RE.match(num)
    
def valid_price(price):
    return price and PRICE_RE.match(price)

def valid_email(email):
	return email and EMAIL_RE.match(email)