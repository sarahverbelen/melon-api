from pymongo import MongoClient

client = MongoClient("mongodb://admin:prototypeAdmin@melon-shard-00-00.igxsj.mongodb.net:27017,melon-shard-00-01.igxsj.mongodb.net:27017,melon-shard-00-02.igxsj.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-7ytrzl-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.melon