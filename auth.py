from bson.objectid import ObjectId
import jwt
import datetime

import mongo
import validation
from errors import NotFoundException, WrongPasswordException, UnauthorizedException, ExistingUserException

def register(object, bcrypt):
	user = object.to_dict()
	# check validation
	if validation.checkPassword(user) and validation.checkEmail(user):
		# check if the user doesn't already exist
		if(mongo.db.users.find_one({'email': user['email']}) == None):
			# hash the password
			user['password'] = bcrypt.generate_password_hash(user['password'])
			settings = {
				'facebook': True,
				'reddit': True,
				'twitter': True,
				'colorblind': False
			}
			user['settings'] = settings
			# save to database
			userId = mongo.db.users.insert_one(user).inserted_id
			return encodeAuthToken(userId)
		else:
			raise ExistingUserException()

def editSettings(object, auth_header):
	settings = object.to_dict()
	userId = checkAuth(auth_header)
	mongo.db.users.update_one({'_id': ObjectId(userId)}, {
		'$set': {'settings': settings}
	})
	return 'ok'

def getMe(auth_header):
	userId = checkAuth(auth_header)
	user = mongo.db.users.find_one({'_id': ObjectId(userId)})
	if user is None:
		raise NotFoundException()
	else:
		userObject = {
				'settings': user['settings'],
				'email': user['email']
			}
		return userObject


def getUserById(id):
	# TODO: only for admin users (or one specific admin user at least)
	user = mongo.db.users.find_one({'_id': ObjectId(id)})
	if user is None:
		raise NotFoundException()
	else:
		return user

def deleteUser(auth_header):
	userId = checkAuth(auth_header)
	mongo.db.records.delete_many({'userId': userId})
	mongo.db.users.delete_one({'_id': ObjectId(userId)})
	return 'ok'

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
			if passwordMatch:
				return encodeAuthToken(registeredUser['_id'])
			else:
				raise WrongPasswordException()

def encodeAuthToken(id):
	payload = {
		'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
		'iat': datetime.datetime.utcnow(),
		'sub': str(id)
	}
	return jwt.encode(
		payload,
		'Watermeloen is mijn favoriete meloen.',
		algorithm='HS256'
	)

def decodeAuthToken(auth_token):
	try:
		payload = jwt.decode(auth_token, 'Watermeloen is mijn favoriete meloen.')
		return payload['sub']
	except jwt.ExpiredSignatureError:
		raise UnauthorizedException()
	except jwt.InvalidTokenError:
		raise UnauthorizedException()

def checkAuth(auth_header):
	if auth_header:
		userId = decodeAuthToken(auth_header)
		return userId
	else:
		raise UnauthorizedException()