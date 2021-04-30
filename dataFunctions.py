import re

import mongo
from errors import NoEmailException, InvalidEmailException

emailRegex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

def saveUser(object):
	user = object.to_dict()
	print(checkEmail(user))

def checkEmail(user):
	if 'email' in user:
		if re.search(emailRegex, user['email']):
		 	# mongo.db.users.insert_one(user)
			return 'email ok'
		else:
		 	raise InvalidEmailException
	else:
		raise NoEmailException