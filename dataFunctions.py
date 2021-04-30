from bson.objectid import ObjectId

import mongo
import validation
from errors import NotFoundException

def saveUser(object):
	user = object.to_dict()
	if validation.checkName(user) and validation.checkEmail(user):
		mongo.db.users.insert_one(user)
		return user
	
def getUserById(id):
	user = mongo.db.users.find_one({'_id': ObjectId(id)})
	if user is None:
		raise NotFoundException()
	else:
		return user
