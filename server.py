import flask
import json
from pymongo import MongoClient
from bson import ObjectId

app = flask.Flask(__name__)
app.config["DEBUG"] = True

client = MongoClient("mongodb://admin:prototypeAdmin@melon-shard-00-00.igxsj.mongodb.net:27017,melon-shard-00-01.igxsj.mongodb.net:27017,melon-shard-00-02.igxsj.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-7ytrzl-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.melon

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
	return json.dumps(db.users.find_one(), cls=JSONEncoder)

app.run()