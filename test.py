from pymongo import MongoClient

client = MongoClient("localhost", 27017)
database = client['22303']
football_collection = database["rkuzmin-football_data"]
game_collection = database["rkuzmin-rkuzmin-game"]
for i in game_collection.find({"goals": {"$elemMatch": {"position": "3"}}}):
    print(i)