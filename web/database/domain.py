import random, string
from pymongo import MongoClient
from bson.objectid import ObjectId

mongo = MongoClient()
dbMongo = mongo['antares']

class domain(object):
	ID = '_id'
	DOMAIN = 'name'

	def find_one(self,*dict):
		return dbMongo.domain.find_one(*dict)

	def find(self, *dict):
		return dbMongo.domain.find(*dict)

	def update(self,*dict):
		return dbMongo.domain.update(*dict)