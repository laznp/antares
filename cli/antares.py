#!/usr/bin/env python
import sys
from os import system
from fabric.api import *
import fabtools
from fabric.colors import red, yellow, green
from datetime import datetime
from optparse import OptionParser

from models import models
from deploy import devops
from mail import mail
from tabulate import tabulate

class antares(object):
	def __init__(self):
		super(antares, self).__init__()
		self.model = models()
		self.devops = devops()
		self.email = mail()
		# self.dateLog = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

	def server_list(self):
		# response = {'status':200,'result':'OK'}
		# self.log_writer('list_server',response)
		return self.model.get_server_list({'method':'find_all'})

	# def server_register(self, public, private, alias, srvpass):
	def server_register(self, public, private, alias):
		self.model.register_server(public, private, alias)
		# self.devops.register_server(srvpass, private)
		return green("%s %s, successfully added" %(u'\u2713',alias.title()))

	def app_list(self):
		# response = {'status':200,'result':'OK'}
		# self.log_writer('list_application',response)
		return self.model.get_app_list({'method':'find_all'})

	def app_register(self, appName, appDom, appRepo, appEnv, appHost):
		appDir = '/var/www/html/' + appRepo.split('git@gitlab.com:inzpire/')[1].split('.git')[0]
		try:
			saveApp = self.model.register_app({
				'app_name':appName,
				'app_domain':appDom,
				'app_repo':appRepo,
				'app_env':appEnv,
				'app_dir':appDir,
				'app_host':appHost.title(),
			})
			if saveApp == None:
				return red("%s Host %s not found" %(u'\u2716', appHost.title()))
			elif saveApp == False:
				return red("%s App %s Exist!" %(u'\u2716', appName))
			elif saveApp == True:
				# deployApp = self.devops.register_app({
				# 	'app_domain':appDom,
				# 	'app_dir':appDir,
				# 	'app_env':appEnv,
				# 	'app_repo':appRepo,
				# 	'app_host':appHost.title()
				# })
				return green("%s %s, successfully added\n" %(u'\u2713', appName)) + yellow("%s Web Hook : http://antares.inzpire.co.id/%s" %(u'\u203A',appName))
		except:
			return None

	def db_list(self):
		# response = {'status':200,'result':'OK'}
		# self.log_writer('list_database',response)
		return self.model.get_db_list({'method':'find_all'})

	def db_register(self, dbHost, dbName, dbUser, userEmail):
		try:
			dbPass = self.model.register_db({
				'db_host':dbHost,
				'db_name':dbName,
				'db_user':dbUser,
			})
			self.devops.add_database_user({
				'db_host':dbHost,
				'db_name':dbName,
				'db_user':dbUser,
				'db_pass':dbPass,
			})
			# mailBody = "DB Host : %s\nDB Name : %s\nDB User : %s\nDB Pass : %s\n" %(dbHost, dbName, dbUser, dbPass)
			# email.send_mail(userEmail, mailBody)
			return yellow(dbPass)
		except:
			return None

	def domain_pointing(self, docRoot, appHost, domain):
		dictPointing = self.devops.domain_pointing(docRoot, appHost,domain)
		# self.log_writer('domain_pointing',dictPointing)
		return dictPointing

	def version_puller(self, appName):
		dictPuller = self.devops.version_puller(appName)
		# self.log_writer('version_puller',dictPuller)
		return dictPuller

if __name__ == '__main__':
	antares = antares()
	if sys.argv[1] == '-al':
		print tabulate(
			antares.app_list(),
			headers="keys",
			tablefmt="psql"
		)
		
	elif sys.argv[1] == '-aa':
		appName = sys.argv[2]
		appDomain = sys.argv[3]
		appRepo = sys.argv[4]
		appEnv = sys.argv[5]
		appHost = sys.argv[6]
		print antares.app_register(appName, appDomain, appRepo, appEnv, appHost)

	elif sys.argv[1] == '-dl':
		print tabulate(
			antares.db_list(), 
			headers="keys", 
			tablefmt="psql"
		)

	elif sys.argv[1] == '-ad':
		dbHost = sys.argv[2]
		dbName = sys.argv[3]
		dbUser = sys.argv[4]
		userEmail = sys.argv[5]
		print antares.db_register(dbHost, dbName, dbUser, userEmail)

	elif sys.argv[1] == '-sl':
		# tableHeader = ['DB PASSWORD','DB NAME','DB ID','DB HOST','DB USER']
		print tabulate(
			antares.server_list(), 
			headers="keys", 
			tablefmt="psql"
		)
	elif sys.argv[1] == '-as':
		public = sys.argv[2]
		private = sys.argv[3]
		alias = sys.argv[4]
		print antares.server_register(public, private, alias)
