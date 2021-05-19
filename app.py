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
app.config['CORS_HEADERS'] = 'Content-Type'
bcrypt = Bcrypt(app)
app.config["DEBUG"] = True

def crossdomain(origin=None, methods=None, headers=None, # found here: https://stackoverflow.com/questions/26980713/solve-cross-origin-resource-sharing-with-flask
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

class JSONEncoder(json.JSONEncoder): # found here https://stackoverflow.com/questions/16586180/typeerror-objectid-is-not-json-serializable
    def default(self, o):
        if isinstance(o, ObjectId) or isinstance(o, Tag) or isinstance(o, datetime):
            return str(o)

        return json.JSONEncoder.default(self, o)

@app.route('/', methods=['GET'])
@crossdomain(origin="*")
def home():
    return "<h1>Melon API</h1>"

@app.route('/test', methods=['GET'])
@crossdomain(origin="*")
def test():
	return json.dumps(mongo.db.users.find_one(), cls=JSONEncoder)

# REGISTER
@app.route('/register', methods=['POST'])
@crossdomain(origin="*")
def save():
    return auth.register(flask.request.form, bcrypt)

# LOGIN
@app.route('/login', methods=['POST'])
@crossdomain(origin="*")
def login():
    return auth.login(flask.request.form, bcrypt)

# GET USER BY ID
@app.route('/user/<id>', methods=['GET'])
@crossdomain(origin="*")
def getUserById(id):
    return json.dumps(auth.getUserById(id),  cls=JSONEncoder)

# SAVE RECORDS
@app.route('/record', methods=['POST'])
@crossdomain(origin="*")
def saveRecord():
    auth_header = flask.request.headers.get('Authorization')
    # TODO: only when logged in
    return json.dumps(dataFunctions.saveRecords(flask.request.form, auth_header),  cls=JSONEncoder)

# GET THE RECORDS OF A USER WITH FILTER (from querystring)
@app.route('/record/', methods=['GET'])
@crossdomain(origin="*")
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

# CHANGE THE SETTINGS
@app.route('/settings', methods=['POST'])
@crossdomain(origin="*")
def changeSettings():
    auth_header = flask.request.headers.get('Authorization')
    return auth.editSettings(flask.request.form, auth_header)

# GET THE CURRENT USER
@app.route('/me', methods=['GET'])
@crossdomain(origin="*")
def getMe():
    auth_header = flask.request.headers.get('Authorization')
    return auth.getMe(auth_header)

# DELETE THE CURRENT USER
@app.route('/me/delete', methods=['GET'])
@crossdomain(origin="*")
def deleteMe():
    auth_header = flask.request.headers.get('Authorization')
    return auth.deleteUser(auth_header)

if __name__ == '__main__':
    app.run()