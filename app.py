import flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask import make_response

import json
from bson import ObjectId
from bs4 import Tag
from datetime import datetime

import dataFunctions
import mongo
import auth

app = flask.Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://melonproject.be"}})
app.config['CORS_HEADERS'] = 'Content-Type'
bcrypt = Bcrypt(app)
app.config["DEBUG"] = True

class JSONEncoder(json.JSONEncoder): # found here https://stackoverflow.com/questions/16586180/typeerror-objectid-is-not-json-serializable
    def default(self, o):
        if isinstance(o, ObjectId) or isinstance(o, Tag) or isinstance(o, datetime):
            return str(o)

        return json.JSONEncoder.default(self, o)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Melon API</h1>", 200

# REGISTER
@app.route('/register', methods=['POST'])
def save():
    res = make_response(auth.register(flask.request.form, bcrypt))
    res.headers.add('Access-Control-Allow-Origin', 'http://melonproject.be')
    return res, 200

# LOGIN
@app.route('/login', methods=['POST'])
def login():
    res = make_response(auth.login(flask.request.form, bcrypt))
    res.headers.add('Access-Control-Allow-Origin', 'http://melonproject.be')
    return res, 200

# GET USER BY ID
@app.route('/user/<id>', methods=['GET'])
def getUserById(id):
    res = make_response(json.dumps(auth.getUserById(id),  cls=JSONEncoder))
    res.headers.add('Access-Control-Allow-Origin', 'http://melonproject.be')
    return res, 200

# SAVE RECORDS
@app.route('/record', methods=['POST'])
def saveRecord():
    auth_header = flask.request.headers.get('Authorization')
    res = make_response(json.dumps(dataFunctions.saveRecords(flask.request.form, auth_header),  cls=JSONEncoder))
    res.headers.add('Access-Control-Allow-Origin', 'http://melonproject.be')
    return res, 200

# GET THE RECORDS OF A USER WITH FILTER (from querystring)
@app.route('/record/', methods=['GET'])
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
    res = make_response(json.dumps(dataFunctions.getUserRecords(filter, auth_header),  cls=JSONEncoder))
    res.headers.add('Access-Control-Allow-Origin', 'http://melonproject.be')
    return res, 200

# CHANGE THE SETTINGS
@app.route('/settings', methods=['POST'])
def changeSettings():
    auth_header = flask.request.headers.get('Authorization')
    res = make_response(auth.editSettings(flask.request.form, auth_header))
    res.headers.add('Access-Control-Allow-Origin', 'http://melonproject.be')
    return res, 200

# GET THE CURRENT USER
@app.route('/me', methods=['GET'])
def getMe():
    auth_header = flask.request.headers.get('Authorization')
    res = make_response(auth.getMe(auth_header))
    res.headers.add('Access-Control-Allow-Origin', 'http://melonproject.be')
    return res, 200

# DELETE THE CURRENT USER
@app.route('/me/delete', methods=['GET'])
def deleteMe():
    auth_header = flask.request.headers.get('Authorization')
    res = make_response(auth.deleteUser(auth_header))
    res.headers.add('Access-Control-Allow-Origin', 'http://melonproject.be')
    return res, 200

if __name__ == '__main__':
    app.run()