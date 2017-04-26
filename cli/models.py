#!/usr/bin/env python

from os import system
import random, string
from pymongo import MongoClient
from bson.objectid import ObjectId

# mongo = MongoClient('10.10.10.14')
mongo = MongoClient('localhost')
dbMongo = mongo['antares']

class models(object):
	def __init__(self):
		super(models, self).__init__()

	def getUserLogin(self, params):
		user = {}
		for x in dbMongo.antares_user.find({'username':params['username']}):
			user.update({
				'username':x['username'],
				'password':x['password'],
			})
		return user

	def make_password(self):
		randomPass = ''.join(random.choice(string.lowercase + string.uppercase + string.digits) for i in range(16))
		return dict({'password':randomPass})

	#-------------------- SERVER --------------------#
	def get_server_list(self, params):
		server = []
		serverData = {}
		if params['method'] == 'find_all':
			for srv in dbMongo.antares_server.find():
				server.append({
					'srv_id':str(srv['_id']),
					'alias':srv['alias'].title(),
					'private_ip':srv['private_ip'],
					'public_ip':srv['public_ip'],
				})
		elif params['method'] == 'find_one':
			server = dbMongo.antares_server.find_one(params['query'])

		return server

	def register_server(self, public, private, alias):
		dbMongo.antares_server.insert({
			'public_ip':public,
			'private_ip':private,
			'alias':alias.title(),
		})

	#-------------------- DATABASE --------------------#
	def get_db_list(self, params):
		dbList = []
		if params['method'] == 'find_all':
			for db in dbMongo.antares_db.find():
				dbList.append({
					'db_id':str(db['_id']),
					'db_host':db['db_host'],
					'db_pass':db['db_pass'],
					'db_name':db['db_name'],
					'db_user':db['db_user'],
				})
		elif params['method'] == 'find_one':
			dbList = dbMongo.antares_db.find_one(params['query'])
		return dbList

	def register_db(self, params):
		try:
			dbHost = self.get_server_list({
				'method':'find_one',
				'query':{
					'alias':str(params['db_host']).title()
				}
			})
		except:
			dbHost = None

		try:
			dbPass = self.get_db_list({
				'method':'find_one',
				'query':{
					'db_user':params['db_user'],
					'db_host':dbHost['alias'],
				}
			})['db_pass']
		except:
			dbPass = self.make_password()['password']

		if dbHost != None:
			dbMongo.antares_db.insert({
				'db_host':params['db_host'].title(),
				'db_name':params['db_name'],
				'db_user':params['db_user'],
				'db_pass':dbPass,
			})
			return dbPass
		else:
			return None

	#-------------------- APPLICATION --------------------#
	def get_app_list(self, params):
		appList = []
		if params['method'] == 'find_all':
			for app in dbMongo.antares_app.find():
				appList.append({
					'app_id':str(app['_id']),
					'app_name':app['app_name'],
					'app_domain':app['app_domain'],
					'app_repo':app['app_repo'],
					'app_dir':app['app_dir'],
					'app_host':app['app_host'],
				})
		elif params['method'] == 'find_one':
			appList = dbMongo.antares_app.find_one(params['query'])

		return appList

	def register_app(self, params):
		try:
			appHost = self.get_server_list({
				'method':'find_one',
				'query':{
					'alias':params['app_host'].title()
				}
			})
		except:
			appHost = None

		appCheck = self.get_app_list({
			'method':'find_one',
			'query':{
				'app_name':params['app_name']
			}
		})

		if appCheck == None:
			if appHost != None:
				dbMongo.antares_app.insert({
					'app_name':params['app_name'],
					'app_domain':params['app_domain'],
					'app_repo':params['app_repo'],
					'app_env':params['app_env'],
					'app_dir':params['app_dir'],
					'app_host':params['app_host'],
				})
				return True
			else:
				return None
		else:
			return False

if __name__ == '__main__':
	pass
	# model = models()
	# print model.register_app({
	# 	'app_name':'LiveAntares',
	# 	'app_domain':'http://antares.inzpire.co.id',
	# 	'app_repo':'git@gitlab.com:inzpire/antares.git',
	# 	'app_env':'master',
	# 	'app_dir':'/var/www/html/antares',
	# 	'app_host':'Sirius'
	# })
