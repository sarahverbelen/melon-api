from bson.objectid import ObjectId
from datetime import datetime, timedelta

import mongo
import validation
import record
from errors import NotFoundException

def saveRecords(object):
	html = object.to_dict()['html']
	source = object.to_dict()['source']

	records = []
	for post in record.split(html, source):
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
	# mongo.db.records.insert_one(newRecord)
	return newRecord

def getUserRecords(id, filter):
	records = filterRecords(id, filter)

	return countRecords(records, filter['time'])

def filterRecords(id, filter):
	resultSet = []

	thisDay = datetime.today().date().day
	thisMonth = datetime.today().date().month
	thisYear = datetime.today().date().year

	if filter['day'] == None and filter['month'] == None and filter['year'] == None:
		# Only give a default day if none of the other filters are set
		filter['day'] = str(thisDay)

	if filter['month'] == None and filter['year'] == None:
		# Give a default month if the year is not set
		filter['month'] = str(thisMonth)
	
	if filter['year'] == None:
		# Always give a default year
		filter['year'] = str(thisYear)

	if filter['time'] == 'alltime':
		for record in mongo.db.records.find({'userId': id}):
			resultSet.append(record)
	elif filter['time'] == 'week':
		amountOfDays = 7
		if filter['pastweek'] != None:
			amountOfDays = (int(filter['pastweek']) * 7) + 7
		dateWeeksAgo = datetime.now() - timedelta(days=amountOfDays)
		dateWeekLater = datetime.now() - timedelta(days=(amountOfDays - 7))
		for record in mongo.db.records.find({'userId': id}):
			if dateWeeksAgo.date() <= record['createdAt'].date() and dateWeekLater.date() >= record['createdAt'].date():
				resultSet.append(record)
	else:
		for record in mongo.db.records.find({'userId': id}):
			day = record['createdAt'].date().day
			month = record['createdAt'].date().month
			year = record['createdAt'].date().year

			if (filter['day'] == str(day) or filter['day'] == None) and (filter['month'] == str(month) or filter['month'] == None) and filter['year'] == str(year):
				resultSet.append(record)

	return resultSet

def countRecords(records, time):
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

	if time == 'week':
		result['perDayCount'] = {}

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

		# WEEK: SEPERATED BY DAY
		if time == 'week':
			date = str(record['createdAt'].date().day) + '/' + str(record['createdAt'].date().month)
			if date not in result['perDayCount']:
				result['perDayCount'][date] = {
					'positive': 0,
					'negative': 0,
					'neutral': 0
				}
			if record['sentiment'] == 0:
				result['perDayCount'][date]['neutral'] += 1
			if record['sentiment'] == -1:
				result['perDayCount'][date]['negative'] += 1
			if record['sentiment'] == 1:
				result['perDayCount'][date]['positive'] += 1
		
			
	return result