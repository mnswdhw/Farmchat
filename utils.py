from pymongo import MongoClient


connection_string = 'mongodb+srv://sheenu:sheenu@cluster0.7otwo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'


client = pymongo.MongoClient(connection_string)
db = client['your-db-name']
