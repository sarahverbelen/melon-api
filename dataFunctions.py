import re

import mongo
from errors import NoEmailException

def saveUser(object):
	user = object.to_dict()

	if hasattr(user, 'email'):
	# todo: check if email is valid
		mongo.db.users.insert_one(user)
	else:
		raise NoEmailException
	