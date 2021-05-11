import re

from errors import NoEmailException, InvalidEmailException, NoPasswordException

emailRegex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

def checkEmail(user):
	# TODO: check if email is unique
	if 'email' in user:
		if re.search(emailRegex, user['email']):
			return True
		else:
		 	raise InvalidEmailException
	else:
		raise NoEmailException

def checkPassword(user):
	# TODO: check if password is long enough etc
	if 'password' in user:
		return True
	else: 
		raise NoPasswordException