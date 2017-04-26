#!/usr/bin/env python

from os import system
import random, string
from pymongo import MongoClient
from bson.objectid import ObjectId

mongo = MongoClient()
dbMongo = mongo['antares']

class models(object):
	def __init__(self):
		super(models, self).__init__()

	def getUserLogin(self, params):
		user = {}
		if dbMongo.antares_user.find({'username':params['username']}).count() != 0:
			for x in dbMongo.antares_user.find({'username':params['username']}):
				user.update({
					'username':x['username'],
					'password':x['password'],
					'uid':str(x['_id']),
				})
			return user
		else:
			return None

	def make_password(self):
		randomPass = ''.join(random.choice(string.lowercase + string.uppercase + string.digits) for i in range(16))
		return dict({'password':randomPass})

	#-------------------- SERVER --------------------#
	def get_server_list(self):
		server = []
		for srv in dbMongo.antares_server.find():
			server.append({
				'srv_id':str(srv['_id']),
				'alias':srv['alias'],
				'private_ip':srv['private_ip'],
				'public_ip':srv['public_ip'],
			})
		return server

	def register_server(self, public, private, alias):
		dbMongo.antares_server.insert({
			'public_ip':public,
			'private_ip':private,
			'alias':alias,
		})

	def get_server_detail(self, srv_id):
		server = []
		try:
			for srv in dbMongo.antares_server.find({'_id':ObjectId(srv_id)}):
				server.append({
					'srv_id':str(srv['_id']),
					'alias':srv['alias'],
					'private_ip':srv['private_ip'],
					'public_ip':srv['public_ip'],
				})
		except:
			for srv in dbMongo.antares_server.find({'alias':srv_id}):
				server.append({
					'private_ip':srv['private_ip'],
				})
		return server

	def edit_server(self, srvID, newPublic, newPrivate, newAlias):
		dbMongo.antares_server.update({
			'_id':ObjectId(srvID)
		},{
			'public_ip':newPublic,
			'alias':newAlias,
			'private_ip':newPrivate,
		})

	def delete_server(self, params):
		dbMongo.antares_server.remove({
			'_id':ObjectId(params)
		})

	#-------------------- DATABASE --------------------#
	def get_db_list(self):
		dbList = []
		for db in dbMongo.antares_db.find():
			dbList.append({
				'db_id':str(db['_id']),
				'db_host':db['db_host'],
				'db_pass':db['db_pass'],
				'db_name':db['db_name'],
				'db_user':db['db_user'],
			})
		return dbList

	def get_db_detail(self, db_id):
		dbList = []
		for db in dbMongo.antares_db.find({'_id':ObjectId(db_id)}):
			dbList.append({
				'db_id':str(db['_id']),
				'db_host':db['db_host'],
				'db_pass':db['db_pass'],
				'db_name':db['db_name'],
				'db_user':db['db_user'],
			})
		return dbList

	def register_db(self, dbHost, dbName, dbUser):
		dbPass = self.make_password()['password']
		for srv in dbMongo.antares_server.find({'private_ip':dbHost}):
			dbHost = srv['alias']

		dbMongo.antares_db.insert({
			'db_host':dbHost,
			'db_name':dbName,
			'db_user':dbUser,
			'db_pass':dbPass,
		})

		return dbPass

	def delete_db(self, dbId):
		dbList = []
		for db in dbMongo.antares_db.find({'_id':ObjectId(dbId)}):
			dbList.append({
				'db_host':db['db_host'],
				'db_name':db['db_name'],
				'db_user':db['db_user'],
				'db_pass':db['db_pass'],
			})
		dbMongo.antares_db.remove({
			'_id':ObjectId(dbId)
		})
		return dbList

	#-------------------- APPLICATION --------------------#
	def get_app_list(self):
		appList = []
		for app in dbMongo.antares_app.find():
			appList.append({
				'app_id':str(app['_id']),
				'app_name':app['app_name'],
				'app_domain':app['app_domain'],
				'app_repo':app['app_repo'],
				'app_dir':app['app_dir'],
				'app_host':app['app_host'],
			})
		return appList

	def get_app_detail(self, app_id):
		appList = []
		for app in dbMongo.antares_app.find({'_id':ObjectId(app_id)}):
			appList.append({
				'app_id':str(app['_id']),
				'app_host':app['app_host'],
				'app_name':app['app_name'],
				'app_repo':app['app_repo'],
				'app_dir':app['app_dir'],
				'app_domain':app['app_domain'],
			})
		return appList

	def register_app(self, appName, appDomain, appRepo, appDir, appHost):
		for srv in dbMongo.antares_server.find({'private_ip':appHost}):
			appHost = srv['alias']
		dbMongo.antares_app.insert({
			'app_name':appName,
			'app_domain':appDomain,
			'app_repo':appRepo,
			'app_dir':appDir,
			'app_host':appHost,
		})

	def edit_app(self, appId, appName, appDomain, appRepo, appDir, appHost):
		for srv in dbMongo.antares_server.find({'private_ip':appHost}):
			appHost = srv['alias']

		dbMongo.antares_app.update({
			'_id':ObjectId(appId)
		},{
			'app_name':appName,
			'app_domain':appDomain,
			'app_repo':appRepo,
			'app_dir':appDir,
			'app_host':appHost,
		})

	def delete_app(self, appId):
		appList = []
		for app in dbMongo.antares_app.find({'_id':ObjectId(appId)}):
			appList.append({
				'app_host':app['app_host'],
				'app_name':app['app_name'],
				'app_dir':app['app_dir'],
				'app_domain':app['app_domain'],
			})
		dbMongo.antares_app.remove({
			'_id':ObjectId(appId)
		})
		return appList

if __name__ == '__main__':
	pass
		
