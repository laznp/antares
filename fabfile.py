#!/usr/bin/env python

from fabric.api import *
import fabtools
env.user = 'root'
env.key_filename = "/home/lazuardi/.ssh/id_rsa"
env.host_string = '10.10.4.92'
# env.host_string = '10.42.0.107'
appDir = '/var/www/html/antares'
apacheConfig = """<VirtualHost *:80>
    ServerName %(domain)s
    ServerAdmin lazuardi@inzpiretechnology.com
    WSGIScriptAlias / %(doc_root)s/web/antares.wsgi
    <Directory %(doc_root)s/web/>
        Order deny,allow
        Allow from all
        WSGIScriptReloading On
    </Directory>
    ErrorLog ${APACHE_LOG_DIR}/%(domain)s/error.log
    CustomLog ${APACHE_LOG_DIR}/%(domain)s/access.log combined
</VirtualHost>
"""

def update_code():
	with cd(appDir):
		run('git pull origin master')
	fabtools.service.restart('apache2')

def install_requirement():
	debList = [
		'libapache2-mod-wsgi',
		'build-essential',
		'g++',
		'gcc',
		'python-dev',
		'python-setuptools',
		'python-pip',
		'python-mysqldb',
		'mongodb',
	]

	pipList = [
		'flask',
		'flask-pymongo',
		'fabric',
		'fabtools'
		'httplib2'
		'tabulate'
	]
	# run('apt install libapache2-mod-wsgi')
	# fabtools.require.deb.packages(debList)
	fabtools.python.install(pipList)

def enable_module():
	fabtools.apache.enable_module('wsgi')

def apache_config():
	fabtools.require.files.directory('/var/log/apache2/antares.dev')
	fabtools.require.apache.site('antares.dev',template_contents=apacheConfig, domain='antares.dev', doc_root=appDir)

def deploy():
	update_code()
	# install_requirement()
	# enable_module()
	apache_config()

