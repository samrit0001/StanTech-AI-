# to create connection with mongoDB

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['amrit_db']
product_collection = db['products']
user_collection = db['users']

# Validation check to verify the collections present or not 
if 'products' not in db.list_collection_names():
    db.create_collection('products')

if 'users' not in db.list_collection_names():
    db.create_collection('users')

