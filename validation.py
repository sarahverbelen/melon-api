import re

from errors import NoEmailException, InvalidEmailException, NoNameException

emailRegex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

def checkEmail(user):
	if 'email' in user:
		if re.search(emailRegex, user['email']):
			return True
		else:
		 	raise InvalidEmailException
	else:
		raise NoEmailException

def checkName(user):
	if 'name' in user:
		return True
	else: 
		raise NoNameException