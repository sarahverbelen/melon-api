import mongo
import validation

def saveUser(object):
	user = object.to_dict()
	if validation.checkName(user) and validation.checkEmail(user):
		mongo.db.users.insert_one(user)
	

