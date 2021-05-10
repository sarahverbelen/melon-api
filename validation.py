import re

from errors import NoEmailException, InvalidEmailException, NoPasswordException

emailRegex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

def checkEmail(user):
	if 'email' in user:
		if re.search(emailRegex, user['email']):
			return True
		else:
		 	raise InvalidEmailException
	else:
		raise NoEmailException

def checkPassword(user):
	if 'password' in user:
		return True
	else: 
		raise NoPasswordException