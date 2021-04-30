import re

import mongo
from errors import NoEmailException, InvalidEmailException, NoNameException

emailRegex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

def saveUser(object):
	user = object.to_dict()
	checkName(checkEmail(user))

def checkEmail(user):
	if 'email' in user:
		if re.search(emailRegex, user['email']):
			return user
		else:
		 	raise InvalidEmailException
	else:
		raise NoEmailException

def checkName(user):
	if 'name' in user:
		mongo.db.users.insert_one(user)
	else: 
		raise NoNameException