import flask
import json
from bson import ObjectId

import dataFunctions
import mongo

from errors import NoEmailException

app = flask.Flask(__name__)
app.config["DEBUG"] = True



class JSONEncoder(json.JSONEncoder): # found here https://stackoverflow.com/questions/16586180/typeerror-objectid-is-not-json-serializable
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)

        return json.JSONEncoder.default(self, o)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Melon API</h1>"

@app.route('/test', methods=['GET'])
def test():
	return json.dumps(mongo.db.users.find_one(), cls=JSONEncoder)

# SAVE USER ROUTE
@app.route('/user', methods=['POST'])
def save():
    dataFunctions.saveUser(flask.request.form)
    return flask.request.form

app.run()