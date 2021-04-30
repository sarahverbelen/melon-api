from bson.objectid import ObjectId

import mongo
import validation
import record
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

def saveRecords(object):
	html = object.to_dict()['html']
	source = object.to_dict()['source']

	records = []
	for post in record.split(html):
		print(post)
		records.append(saveRecord(post, source))

	return records


def saveRecord(html, source):
	newRecord = { # TODO: add userId, createdAt
		'sentiment': record.analyse(html),
		'keywords': record.analyseKeywords(html),
		'emotion': record.analyseEmotion(html),
		'source': source
	}
	mongo.db.records.insert_one(newRecord)
	return newRecord
