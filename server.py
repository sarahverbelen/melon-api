import flask
from flask_cors import CORS
import json
from bson import ObjectId
from bs4 import Tag
from datetime import datetime

import dataFunctions
import mongo
import record

from errors import NoEmailException

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

class JSONEncoder(json.JSONEncoder): # found here https://stackoverflow.com/questions/16586180/typeerror-objectid-is-not-json-serializable
    def default(self, o):
        if isinstance(o, ObjectId) or isinstance(o, Tag) or isinstance(o, datetime):
            return str(o)

        return json.JSONEncoder.default(self, o)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Melon API</h1>"

@app.route('/test', methods=['GET'])
def test():
	return json.dumps(mongo.db.users.find_one(), cls=JSONEncoder)

# SAVE USER
@app.route('/user', methods=['POST'])
def save():
    return json.dumps(dataFunctions.saveUser(flask.request.form), cls=JSONEncoder)

# GET USER BY ID
@app.route('/user/<id>', methods=['GET'])
def getUserById(id):
    return json.dumps(dataFunctions.getUserById(id),  cls=JSONEncoder)

# SAVE RECORDS
@app.route('/record', methods=['POST'])
def saveRecord():
    return json.dumps(dataFunctions.saveRecords(flask.request.form),  cls=JSONEncoder)

# GET THE RECORDS OF A USER WITH FILTER (from querystring)
@app.route('/user/<id>/record/')
def getUserRecords(id):
    filter = {
        'day': flask.request.args.get('day'),
        'month': flask.request.args.get('month'),
        'year': flask.request.args.get('year'),
        'time': flask.request.args.get('time')
    }
    # if the querystring is empty, it will give the results of today by default
    # if only the day is given, it will give the results of that day this month
    # if only the month is given, it will give the results of this month
    # if only the year is given, it will give the results of this year
    # if time is 'week', it will give the results for this week, seperated by day (and in total)
    # if time is 'alltime', it will give the results for alltime
    return json.dumps(dataFunctions.getUserRecords(id, filter),  cls=JSONEncoder)

app.run()