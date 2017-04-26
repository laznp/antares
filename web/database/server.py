import random, string
from pymongo import MongoClient
from bson.objectid import ObjectId

mongo = MongoClient()
dbMongo = mongo['antares']

class Server(object):
    PUBLIC_IP = 'public_ip'
    PRIVATE_IP = 'private_ip'
    ALIAS = 'alias'
    _ID = '_id'
    def find_one(self,*dict):
        return dbMongo.antares_server.find_one(*dict)
    def find(self,*dict):
        return dbMongo.antares_server.find(*dict)