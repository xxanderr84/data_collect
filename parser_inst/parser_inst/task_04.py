from pymongo import MongoClient
client = MongoClient('localhost', 27017)
data_base = client.instagram
collection = data_base.followers
query = {"user_id": "4548286806"}
docs = collection.find(query)
for x in docs:
    print(x)
