import random, string
from pymongo import MongoClient
from bson.objectid import ObjectId

mongo = MongoClient()
dbMongo = mongo['antares']

class spekserver(object):
	_ID = '_id'
	NAME_PC = 'name_pc'
	PROCESSOR = 'processor'
	RAM = 'ram'
	STORAGE = 'storage'
	DEPENDENCY = 'dependency'
	SERVER_ID = 'serverid'
	def find_one(self,*dict):
		return dbMongo.antares_spekserver.find_one(*dict)
	def find(self,*dict):
		return dbMongo.antares_spekserver.find(*dict)
	def insert_one(self,*dict):
		return dbMongo.antares_spekserver.insert_one(*dict)
	def update(self,*dict):
		return dbMongo.antares_spekserver.update(*dict)