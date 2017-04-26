#!/usr/bin/env python

from os import system
from fabric.api import *
import fabtools
from models import models

# env.host_string = "localhost"
env.user = "root"
# env.key_filename = "/root/.ssh/id_rsa"
env.key_filename = "/home/lazuardi/.ssh/id_rsa"

class devops(object):
	def __init__(self):
		super(devops, self).__init__()
		self.model = models()
		self.template = '''<VirtualHost *:80>
	ServerAdmin devops@%(url)s
	ServerName %(url)s
	DocumentRoot %(doc_root)s
	<Directory %(doc_root)s>
		Options Indexes FollowSymLinks MultiViews
		AllowOverride All
		Order allow,deny
		allow from all
	</Directory>
	ErrorLog ${APACHE_LOG_DIR}/%(url)s/error.log
	CustomLog ${APACHE_LOG_DIR}/%(url)s/access.log combined
</VirtualHost>
'''
		self.template_https = '''<VirtualHost *:80>
	ServerName %(url)s
	Redirect / https://%(url)s/
</VirtualHost>

<VirtualHost *:443>
	ServerAdmin devops@%(url)s
	ServerName %(url)s
	DocumentRoot %(doc_root)s/
	<Directory %(doc_root)s/>
		Options Indexes FollowSymLinks MultiViews
		AllowOverride All
		Order allow,deny
		allow from all
	</Directory>
	SSLEngine on
	SSLCertificateFile /ssl/aeroaffiliate.com/star.aeroaffiliate.com.crt
	SSLCertificateKeyFile /ssl/aeroaffiliate.com/star.aeroaffiliate.com.key
	SSLCACertificateFile /ssl/aeroaffiliate.com/star.aeroaffiliate.com-intermediate.crt
	ErrorLog ${APACHE_LOG_DIR}/%(url)s/error.log
	CustomLog ${APACHE_LOG_DIR}/%(url)s/access.log combined
</VirtualHost>'''
	
	def register_server(self, srvPass, srvHost):
		local("sshpass -p '%s' ssh-copy-id -o StrictHostKeyChecking=no root@%s -f" %(srvPass, srvHost))

	def add_database_user(self, params):
		try:
			dbHost = self.model.get_server_list({
				'method':'find_one',
				'query':{
					'alias':params['db_host'].title()
				}
			})['private_ip']
		except:
			dbHost = None

		if dbHost != None:
			env.host_string = dbHost
			if not fabtools.mysql.user_exists(params['db_user']):
				fabtools.mysql.create_user(params['db_user'], password=params['db_pass'])

			if not fabtools.mysql.database_exists(params['db_name']):
				fabtools.mysql.create_database(params['db_name'], owner=params['db_user'])
		else:
			return None
			
	def register_app(self, params):
		try:
			docRoot = self.model.get_app_list({
				'method':'find_one',
				'query':{
					'app_repo':params['app_repo'],
					'app_host':params['app_host'].title(),
				}
			})['app_dir']
		except:
			docRoot = None

		try:
			appHost = self.model.get_server_list({
				'method':'find_one',
				'query':{
					'alias':params['app_host'].title()
				}
			})['private_ip']
		except:
			appHost = None
		

		if appHost != None:
			env.host_string = appHost
			if docRoot != None:
				self.domain_pointing(docRoot,appHost,params['app_domain'])
			elif docRoot == None:
				run('git clone %s -b %s %s' %(params['app_repo'], params['app_env'], params['app_dir']))
				run('chown -Rf www-data.www-data %s' %(params['app_dir']))
				self.domain_pointing(params['app_dir'],appHost,params['app_domain'])
		else:
			return None

	def domain_pointing(self, docRoot, domHost, url):
		try:
			env.host_string = domHost
			fabtools.require.files.directory('/var/log/apache2/'+url)
			fabtools.require.apache.site(url,template_contents=self.template, url=url, doc_root=docRoot)
		except:
			return False

	def domain_delete(self,domHost, url):
		try:
			# env.host_string = domHost
			fabtools.require.apache.site_disabled(url)
			fabtools.files.remove('/etc/apache2/sites-available/%s.conf' %(url))
			fabtools.service.restart('apache2')
			return True
		except:
			return False

	def version_puller(self, appName):
		app = self.model.get_app_list({
				'method':'find_one',
				'query':{
					'app_name':appName
				}
			})

		try:
			appHost = self.model.get_server_list({
					'method':'find_one',
					'query':{
						'alias':str(app['app_host'])
					}
				})['private_ip']
			env.host_string = appHost
			run('cd %s; git pull origin %s' %(app['app_dir'], app['app_env']))
			run('chown -Rf www-data.www-data %s' %(app['app_dir']))
			return True
		except:
			return False

if __name__ == '__main__':
	pass
	# devops = devops()
	# print devops.version_puller('DevAntares')
		
