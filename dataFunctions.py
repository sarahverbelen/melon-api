from bson.objectid import ObjectId
from datetime import datetime

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
		records.append(saveRecord(post, source))

	return records


def saveRecord(html, source):
	newRecord = {
		'sentiment': record.analyse(html),
		'keywords': record.analyseKeywords(html),
		'emotion': record.analyseEmotion(html),
		'source': source,
		'userId': '608fb0824832f22bdd3542f1', # TODO: get this from authentication...
		'createdAt': datetime.now()
	}
	mongo.db.records.insert_one(newRecord)
	return newRecord

def getUserRecords(id, filter):
	records = filterRecords(id, filter)

	return countRecords(records)

def filterRecords(id, filter):
	resultSet = []

	for record in mongo.db.records.find({'userId': id}):
		year, week, day_of_week = record['createdAt'].date().isocalendar()
		thisYear, thisWeek, thisDay_of_week =  datetime.today().date().isocalendar()

		if filter == 'today' and record['createdAt'].date() == datetime.today().date():
			resultSet.append(record)
		if filter == 'week' and week == thisWeek:
			resultSet.append(record)
		if filter == 'year' and year == thisYear:
			resultSet.append(record)
		if filter == 'all':
			resultSet.append(record)
		# TODO: filters for previous weeks / years / days / months + month filter

	return resultSet

def countRecords(records):
	result = {
		# absolute numbers
		'positiveCount': 0,
		'negativeCount': 0,
		'neutralCount': 0,
		'emotionsCount': {
			'happy': 0,
			'angry': 0
		},
		# numbers per keyword
		'keywordCount': {},
		#numbers per website
		'websiteCount': {
			'facebook': {
				'positive': 0,
				'neutral': 0,
				'negative': 0
			},
			'reddit': {
				'positive': 0,
				'neutral': 0,
				'negative': 0
			},
			'twitter': {
				'positive': 0,
				'neutral': 0,
				'negative': 0
			}
		}
	}

	for record in records:
		# SENTIMENT
		if record['sentiment'] == 0:
			result['neutralCount'] += 1
		if record['sentiment'] == -1:
			result['negativeCount'] += 1
		if record['sentiment'] == 1:
			result['positiveCount'] += 1

		# EMOTION
		result['emotionsCount'][record['emotion']] += 1

		# KEYWORDS
		for word in record['keywords']:
			if word not in result['keywordCount']:
				result['keywordCount'][word] = {
					'count': 0,
					'negativeCount': 0,
					'positiveCount': 0,
					'neutralCount': 0
				}
			result['keywordCount'][word]['count'] += 1
			if record['sentiment'] == 0:
				result['keywordCount'][word]['neutralCount'] += 1
			if record['sentiment'] == -1:
				result['keywordCount'][word]['negativeCount'] += 1
			if record['sentiment'] == 1:
				result['keywordCount'][word]['positiveCount'] += 1

		# WEBSITES
		if record['sentiment'] == 0:
			result['websiteCount'][record['source']]['neutral'] += 1
		if record['sentiment'] == -1:
			result['websiteCount'][record['source']]['negative'] += 1
		if record['sentiment'] == 1:
			result['websiteCount'][record['source']]['positive'] += 1
		
			
	return result