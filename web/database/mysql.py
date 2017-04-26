from pymongo import MongoClient

mongo = MongoClient()
dbMongo = mongo['antares']

class Mysql(object):
	DB_HOST = 'db_host'
	DB_NAME = 'db_name'
	DB_PASS = 'db_pass'
	DB_USER = 'db_user'
	ID = '_id'
	def find_one(self,*dict):
		return dbMongo.antares_db.find_one(*dict)
	def find(self,*dict):
		return dbMongo.antares_db.find(*dict)
	def insert_one(self, *dict):
		return dbMongo.antares_db.insert_one(*dict).inserted_id
	def delete_one(self, *dict):
		return dbMongo.antares_db.delete_one(*dict)