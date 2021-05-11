from bson.objectid import ObjectId

import mongo
import validation
from errors import NotFoundException

def register(object, bcrypt):
	user = object.to_dict()
	# check validation
	if validation.checkPassword(user) and validation.checkEmail(user):
		# hash the password
		user['password'] = bcrypt.generate_password_hash(user['password'])
		# save to database
		mongo.db.users.insert_one(user)
		return 'succes'

def getUserById(id):
	# TODO: only for admin users (or one specific admin user at least)
	user = mongo.db.users.find_one({'_id': ObjectId(id)})
	if user is None:
		raise NotFoundException()
	else:
		return user

def login(user, bcrypt):
	 # check if email and password are valid
	if validation.checkPassword(user) and validation.checkEmail(user):
		# check if email exists in database
		registeredUser = mongo.db.users.find_one({'email': user['email']})
		if registeredUser == None:
			raise NotFoundException()
		else:
			# check if password hash matches saved pashword hash
			passwordMatch = bcrypt.check_password_hash(registeredUser['password'], user['password'])
			print(passwordMatch)
	# TODO: create JWT..
	return 'succes'
