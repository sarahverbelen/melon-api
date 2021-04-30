import flask
import json
from bson import ObjectId
from bs4 import Tag

import dataFunctions
import mongo
import record

from errors import NoEmailException

app = flask.Flask(__name__)
app.config["DEBUG"] = True

class JSONEncoder(json.JSONEncoder): # found here https://stackoverflow.com/questions/16586180/typeerror-objectid-is-not-json-serializable
    def default(self, o):
        if isinstance(o, ObjectId) or isinstance(o, Tag):
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

app.run()