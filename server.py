import flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt

import json
from bson import ObjectId
from bs4 import Tag
from datetime import datetime

import dataFunctions
import mongo
import record
import auth

from errors import NoEmailException

app = flask.Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
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

# REGISTER
@app.route('/register', methods=['POST'])
def save():
    return auth.register(flask.request.form, bcrypt)

# LOGIN
@app.route('/login', methods=['POST'])
def login():
    return auth.login(flask.request.form, bcrypt)

# GET USER BY ID
@app.route('/user/<id>', methods=['GET'])
def getUserById(id):
    return json.dumps(auth.getUserById(id),  cls=JSONEncoder)

# SAVE RECORDS
@app.route('/record', methods=['POST'])
def saveRecord():
    auth_header = flask.request.headers.get('Authorization')
    # TODO: only when logged in
    return json.dumps(dataFunctions.saveRecords(flask.request.form, auth_header),  cls=JSONEncoder)

# GET THE RECORDS OF A USER WITH FILTER (from querystring)
@app.route('/record/')
def getUserRecords():
    auth_header = flask.request.headers.get('Authorization')
    filter = {
        'day': flask.request.args.get('day'),
        'month': flask.request.args.get('month'),
        'year': flask.request.args.get('year'),
        'time': flask.request.args.get('time'),
        'pastweek': flask.request.args.get('pastweek')
    }
    # if the querystring is empty, it will give the results of today by default
    # if only the day is given, it will give the results of that day this month
    # if only the month is given, it will give the results of this month
    # if only the year is given, it will give the results of this year
    # if time is 'week', it will give the results for this week, seperated by day (and in total)
    # if time is 'alltime', it will give the results for alltime
    # the number in 'pastweek' determines how many weeks in the past the api will return
    return json.dumps(dataFunctions.getUserRecords(filter, auth_header),  cls=JSONEncoder)

app.run()