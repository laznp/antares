#!/usr/bin/env python

from os import system
import random, string
from fabric.api import *
import fabtools
from model import models

env.host_string = "localhost"
env.user = "root"
env.key_filename = "/root/.ssh/id_rsa"

class devops(object):
	def __init__(self):
		super(devops, self).__init__()

	def register_server(self, srvPass, srvHost):
		local("sshpass -p '%s' ssh-copy-id root@%s" %(srvPass, srvHost))

	def add_database_user(self, dbHost, dbName, dbUser, dbPass):
		env.host_string = dbHost
		if not fabtools.mysql.user_exists(str(dbUser)):
			fabtools.mysql.create_user(str(dbUser), password=str(dbPass))

		if not fabtools.mysql.database_exists(str(dbName)):
			fabtools.mysql.create_database(str(dbName), owner=str(dbUser))

	def delete_database_user(self, dbHost, dbName, dbUser):
		env.host_string = dbHost
		if fabtools.mysql.database_exists(str(dbName)):
			fabtools.mysql.query("DROP DATABASE %s" %(dbName))
		if fabtools.mysql.user_exists(str(dbUser)):
			fabtools.mysql.query("DROP USER '%s'@'localhost'" %(dbUser))

	
	def add_application(self, url, doc_root, app_name, repo, host):
		env.host_string = host
		run('git clone %s %s' %(repo, doc_root))
		run('chown -Rf www-data.www-data %s' %(doc_root))
		template = '''
<VirtualHost *:80>
	ServerAdmin devops@%(url)s
	ServerName %(url)s
	ServerAlias www.%(url)s
	DocumentRoot %(doc_root)s
	<Directory %(doc_root)s>
		Options Indexes FollowSymLinks MultiViews
		AllowOverride All
		Order allow,deny
		allow from all
	</Directory>
	ErrorLog ${APACHE_LOG_DIR}/%(app_name)s/error.log
	CustomLog ${APACHE_LOG_DIR}/%(app_name)s/access.log combined
</VirtualHost>
'''
		fabtools.require.directory('/var/log/apache2/%s' %app_name)
		fabtools.require.apache.site(url,template_contents=template, url=url, doc_root=doc_root,app_name=app_name)

if __name__ == '__main__':
	pass
		
