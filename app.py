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
CORS(app, resources={r"/*": {"origins": ["http://melonproject.be", "chrome-extension://fdcoolfboghoepcadhhmggjjehejiaie"]}})
app.config['CORS_HEADERS'] = 'Content-Type'
bcrypt = Bcrypt(app)
app.config["DEBUG"] = True

white = ['http://melonproject.be','chrome-extension://fdcoolfboghoepcadhhmggjjehejiaie', 'https://www.facebook.com', 'https://www.reddit.com', 'https://twitter.com']

def add_cors_headers(request, response): # found here https://stackoverflow.com/questions/42681311/flask-access-control-allow-origin-for-multiple-urls
    r = request.referrer
    if r in white:
        response.headers.add('Access-Control-Allow-Origin', r)
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
        response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
        response.headers.add('Access-Control-Allow-Headers', 'Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    return response

class JSONEncoder(json.JSONEncoder): # found here https://stackoverflow.com/questions/16586180/typeerror-objectid-is-not-json-serializable
    def default(self, o):
        if isinstance(o, ObjectId) or isinstance(o, Tag) or isinstance(o, datetime):
            return str(o)

        return json.JSONEncoder.default(self, o)

@app.route('/', methods=['GET'])
def home():
    res = make_response("<h1>Melon API</h1>")
    res = add_cors_headers(flask.request, res)
    return res, 200

# REGISTER
@app.route('/register', methods=['POST'])
def save():
    res = make_response(auth.register(flask.request.form, bcrypt))
    res = add_cors_headers(flask.request, res)
    # res.headers.add('Access-Control-Allow-Origin', )
    return res, 200

# LOGIN
@app.route('/login', methods=['POST'])
def login():
    res = make_response(auth.login(flask.request.form, bcrypt))
    res = add_cors_headers(flask.request, res)
    # res.headers.add('Access-Control-Allow-Origin', 'http://melonproject.be')
    return res, 200

# GET USER BY ID
@app.route('/user/<id>', methods=['GET'])
def getUserById(id):
    res = make_response(json.dumps(auth.getUserById(id),  cls=JSONEncoder))
    res = add_cors_headers(flask.request, res)
    # res.headers.add('Access-Control-Allow-Origin', 'http://melonproject.be')
    return res, 200

# SAVE RECORDS
@app.route('/record', methods=['POST'])
def saveRecord():
    auth_header = flask.request.headers.get('Authorization')
    res = make_response(json.dumps(dataFunctions.saveRecords(flask.request.form, auth_header),  cls=JSONEncoder))
    res = add_cors_headers(flask.request, res)
    # res.headers.add('Access-Control-Allow-Origin', 'http://melonproject.be')
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
    res = add_cors_headers(flask.request, res)
    # res.headers.add('Access-Control-Allow-Origin', 'http://melonproject.be')
    return res, 200

# CHANGE THE SETTINGS
@app.route('/settings', methods=['POST'])
def changeSettings():
    auth_header = flask.request.headers.get('Authorization')
    res = make_response(auth.editSettings(flask.request.form, auth_header))
    res = add_cors_headers(flask.request, res)
    # res.headers.add('Access-Control-Allow-Origin', 'http://melonproject.be')
    return res, 200

# GET THE CURRENT USER
@app.route('/me', methods=['GET'])
def getMe():
    auth_header = flask.request.headers.get('Authorization')
    res = make_response(auth.getMe(auth_header))
    res = add_cors_headers(flask.request, res)
    # res.headers.add('Access-Control-Allow-Origin', 'http://melonproject.be')
    return res, 200

# DELETE THE CURRENT USER
@app.route('/me/delete', methods=['GET'])
def deleteMe():
    auth_header = flask.request.headers.get('Authorization')
    res = make_response(auth.deleteUser(auth_header))
    res = add_cors_headers(flask.request, res)
    # res.headers.add('Access-Control-Allow-Origin', 'http://melonproject.be')
    return res, 200

if __name__ == '__main__':
    app.run()