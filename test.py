from pymongo import MongoClient

client = MongoClient("localhost", 27017)
database = client['22303']
football_collection = database["rkuzmin-football_data"]
game_collection = database["rkuzmin-game_data"]
football_collection.delete_many({})
game_collection.delete_many({})