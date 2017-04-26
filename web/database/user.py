import random, string
from pymongo import MongoClient
from bson.objectid import ObjectId

mongo = MongoClient()
dbMongo = mongo['antares']

class User(object):
    _ID = '_id'
    EMAIL = 'email'
    USERNAME = 'username'
    PASSWORD = 'password'
    def find_one(self,*dict):
        return dbMongo.antares_user.find_one(*dict)