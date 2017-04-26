#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, session, jsonify, url_for, Response, abort
from collections import namedtuple
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util
from fabric.api import env, run, local
from fabric.contrib import files as contribfiles
from StringIO import StringIO
from hashlib import sha1
from time import strftime, gmtime
import hmac
import httplib2
import re
import hashlib
import logging
import datetime
import dnsmadeeasy
import json
import os
import sys
#from flask_socketio import SocketIO, emit
import subprocess, io
import thread, copy, fabtools, fabric

########################################
sys.path.insert(0,'.')
from cli import antares as cliantares
Cliantares = cliantares.antares()

from database import user as databaseuser
User = databaseuser.User()

from database import server as databaseserver
Server = databaseserver.Server()

from database import app as databaseapp
App = databaseapp.app()

from database import mysql as databasemysql
Mysql = databasemysql.Mysql()

from database import spekserver as databasespekserver
Spekserver = databasespekserver.spekserver()

from database import domain as databasedomain
Domain = databasedomain.domain()

from dnsmadeeasy import dnsmadeeasy
Dnsmadeeasy = dnsmadeeasy()
########################################

from log import Log
from model import models
from deploy import devops
model = models()
Devops = devops()
antares = Flask(__name__, template_folder='template', static_folder='static')
antares.secret_key = "rahasia"
sessionvalue = 'ObjectId'

env.user = 'root'
#env.key_filename = '/home/wahyudiansyah/.ssh/id_rsa'
env.key_filename = '/var/www/.ssh/id_rsa'
env.host_string = 'localhost'

# will be deleted
# @antares.route('/', methods=['GET','POST'])
# def index():
# 	# if 'ObjectId' in session:
# 	# 	return render_template("panel/panel.html")
# 	# return render_template("login/login.html")
# 	return render_template("index.html")
###################################################################
@antares.route('/1', methods=['GET'])
def index1():
	# print request.remote_addr
	if sessionvalue in session:
		return render_template("panel/panel.html")
	return render_template("login/login.html")
@antares.route('/login1', methods=['POST'])
def login1():
	username = request.form['username']
	password = request.form['password']
	match = User.find_one({"username":username,"password":password})
	if match != None:
		_id = match.get('_id')
		username = match.get('username')
		session['ObjectId'] = str(_id)
	return redirect(url_for('index1'))
@antares.route('/logout1')
def logout1():
	session.pop(sessionvalue, None)
	return redirect(url_for('index1'))
###################################################################
# will be deleted
# @antares.route('/login')
# def login():
# 	return render_template("login.html")
# will be deleted
# @antares.route('/login-process', methods=['POST'])
# def login_process():
# 	uname = request.form['uname']
# 	upass = request.form['upass']
# 	data = model.getUserLogin({'username':uname})
# 	if data == None:
# 		return redirect('/login')
# 	else:
# 		if uname == data['username'] and upass == data['password']:
# 			session['uid'] = data['uid']
# 			return redirect('/server')
# 		else:
# 			return redirect('/login')

#----- SERVER -----#
# will be deleted
# @antares.route('/server')
# def server():
# 	if 'uid' in session:
# 		data = model.get_server_list()
# 		user = User.find_one({"_id":ObjectId(session['uid'])})['username']
# 		return render_template('server.html', data=data, user=user )
# 	else:
# 		return redirect('/login')

@antares.route('/server1')
def server1():
	if sessionvalue not in session:
		return redirect(url_for('index1'))
	return json.dumps(list(Server.find({})),default=json_util.default)
#----- SERVER -----#

#----- DATABASE -----#
# will be deleted
# @antares.route('/database')
# def database():
# 	if 'uid' in session:
# 		data = model.get_db_list()
# 		return render_template('database.html', data=data)
# 	else:
# 		return redirect('/login')

@antares.route('/database1')
def database1():
	if sessionvalue not in session:
		return redirect(url_for('index1'))
	return json.dumps(list(Mysql.find({})),default=json_util.default)
#----- DATABASE -----#

#----- APPLICATION -----#
# will be deleted
# @antares.route('/app')
# def app():
# 	if 'uid' in session:
# 		data = model.get_app_list()
# 		return render_template('app.html', data=data)
# 	else:
# 		return redirect('/login')

@antares.route('/application1')
def application1():
	if sessionvalue not in session:
		return redirect(url_for('index1'))
	return json.dumps(list(App.find({})),default=json_util.default)

#----- APPLICATION -----#

#----- DOMAIN -----#
def dme_connect(resource="", method="", data="",):
	domainList = []
	baseurl = "https://api.dnsmadeeasy.com/V2.0/dns/managed/"
	apikey = "c8d704bf-5c4d-465c-8d6c-eea33a3e4127"
	secret = "654b814b-9745-44dd-9b60-994982661168"
	dateNow = strftime('%a, %d %b %Y %H:%M:%S +0000', gmtime())
	hashed = hmac.new(secret, dateNow, sha1)
	header = { 'x-dnsme-apiKey': apikey, 'x-dnsme-requestDate':dateNow, 'x-dnsme-hmac':hashed.hexdigest() }
	http = httplib2.Http()

	response, content = http.request(baseurl + resource, method, body=data, headers=header)
	if response['status'] == "200" or  response['status'] == "201" :
		if content:
			try:
				jsonresponse = json.loads(content.decode('utf-8'))
				for domain in jsonresponse['data']:
					domainList.append({'dom_name':domain['name'],'dom_id':domain['id']})
				return domainList
			except:
				jsonresponse = json.loads(content.decode('utf-8'))
				return jsonresponse
		else:
			print(response)
	else:
		print(content)
		raise Exception("Error talking to dnsmadeeasy: " + response['status'])


# !important
@antares.route('/datauser')
def datauser():
	if sessionvalue not in session:
		abort(404)
	return jsonify( User.find_one({User._ID:ObjectId(session[sessionvalue])},{"_id":False}))
#----- DOMAIN -----#

# will be deleted
#----- GITLAB REPOSITORY -----#
# def gitlab_connect(resource="", method="", data="",):
# 	domainList = []
# 	baseurl = "https://gitlab.com/api/v3/projects"
# 	priv_token = "3qCdeNwwer6nfGa2nUDd"
# 	header = { 'PRIVATE-TOKEN': priv_token }
# 	http = httplib2.Http()
#
# 	response, content = http.request(baseurl + resource, method, body=data, headers=header)
# 	if response['status'] == "200" or  response['status'] == "201" :
# 		if content:
# 			try:
# 				jsonresponse = json.loads(content.decode('utf-8'))
# 				for domain in jsonresponse['data']:
# 					domainList.append({'dom_name':domain['name'],'dom_id':domain['id']})
# 				return domainList
# 			except:
# 				jsonresponse = json.loads(content.decode('utf-8'))
# 				return jsonresponse
# 		else:
# 			print response
# 	else:
# 		print(content)
# 		raise Exception("Error talking to dnsmadeeasy: " + response['status'])
#----- GITLAB REPOSITORY -----#
# will be deleted
# @antares.route('/logout')
# def logout():
# 	session.pop('uid', None)
# 	return redirect('/login')


# will be deleted
# @antares.route('/hook/<server>/<product>/<status>')
# def hook(server, product, status):
# 	if status == 'success':
# 		cond = 'Has Been Successfully Updated'
# 	elif status == 'failed':
# 		cond = 'Failed to Update'
# 	data = {
# 		'server':server,
# 		'product':product,
# 		'status':cond,
# 	}
# 	return render_template('hook.html', data=data)
#will be deleted
@antares.route('/pull/<server>/<product>/<branch>/', methods=['GET','POST'])
def git_puller(server, product, branch):
	app = Server.find_one({'alias':server.title()})
	appHost = app['private_ip']
	app = App.find_one({'app_name':product})
	appDir = app['app_dir']

	env.host_string = str(appHost)
	env.user = "root"
	env.key_filename = "/var/www/.ssh/id_rsa"
	try:
		run('cd %s; git pull origin %s' %(appDir, branch))
		run('chown -Rf www-data.www-data %s' %(appDir))
		status = 'success'
	except Exception, e:
		status = 'failed'
	return redirect('/hook/%s/%s/%s' %(server.title(), product, status))

@antares.route('/pull/<product>/', methods=['GET','POST'])
def git_puller1(product):
	Cliantares.version_puller(product)
	# return redirect('/hook/%s/%s/%s' %(server.title(), product, status))

@antares.route('/spekeditor/<id_server>/', methods=['GET','POST'])
def spekeditor(id_server):
	if sessionvalue not in session:
		return redirect(url_for('index1'))
	name_server = Server.find_one({'_id': ObjectId(id_server)})[Server.ALIAS]
	if request.method == 'GET':
		spekdata = {
			Spekserver.SERVER_ID : "",
			Spekserver.NAME_PC : "",
			Spekserver.PROCESSOR : "",
			Spekserver.RAM : "",
			Spekserver.STORAGE : "",
			Spekserver.DEPENDENCY : ""
		}
		fetch = Spekserver.find_one({Spekserver.SERVER_ID: id_server})
		if fetch != None:
			spekdata.update(fetch)
		return render_template('spekeditor/index.html', name_server=name_server,spekdata=spekdata )
	if request.method == 'POST':
		spekdata = request.form.to_dict()
		spekdata.update({'serverid':id_server})
		spekupdate = Spekserver.update({'serverid':id_server},spekdata,True)
		if spekupdate != None:
			update = True
			return render_template('spekeditor/index.html', name_server=name_server, spekdata=spekdata, update=update)
		else:
			update = False
			return render_template('spekeditor/index.html', name_server=name_server, spekdata=spekdata, update=update)
#
@antares.route('/spekserver/<server>/', methods=['GET','POST'])
def spekserver(server):
	return "OK"

@antares.route('/domain', methods=['GET'])
def domain():
	try:
		L = []
		List = Dnsmadeeasy.get_domain_list()
		for x in List:
			Domain.update({'name':x['dom_name']},{'name':x['dom_name']}, True)
			L.append(x['dom_name'])
		return json.dumps(L)
	except Exception as inst:
		L = []
		dataDomain = Domain.find()
		for x in dataDomain:
			L.append(x['name'])
		return json.dumps(L)

myout = StringIO()
finish = 0
def clone(APP_REPO, APP_DIR,TOPDOMAIN,APP_DOMAIN,SUBDOMAIN,PUBLIC_IP,APP_NAME,APP_ENV,APP_HOST,PRIVATE_IP):
	global finish
	global myout
	global env
	try:
		fabtools.require.files.directory(APP_DIR)
		run('git clone -b %s %s %s' % (APP_ENV, APP_REPO, APP_DIR),stdout=myout)
		fabtools.require.files.directory(APP_DIR,owner='www-data',group='www-data')
	except:
		return json.dumps({'addappfinish': 1,
						   'console': "",
						   'registered': "Internal Server Error"})

	crt = contribfiles.exists('/ssl/' + TOPDOMAIN + '/star.' + TOPDOMAIN + '.crt', )
	key = contribfiles.exists('/ssl/' + TOPDOMAIN + '/star.' + TOPDOMAIN + '.key')
	intermediate = contribfiles.exists('/ssl/' + TOPDOMAIN + '/star.' + TOPDOMAIN + '-intermediate.crt')

	if crt == True and key == True and intermediate == True:
		template = TEMPLATE_CONTENTS_SSL
	else:
		template = TEMPLATE_CONTENTS

	try:
		fabtools.require.files.directory('/var/log/apache2/' + APP_DOMAIN)
		myout.write('create log directory\n')
		fabtools.require.files.directory(APP_DIR)
		myout.write('['+PRIVATE_IP+'] out: create app directory\n')
		fabtools.require.apache.site(APP_DOMAIN, template_contents=template, url=APP_DOMAIN,
									 doc_root=APP_DIR, topdomain=TOPDOMAIN)
		myout.write('['+PRIVATE_IP+'] out: create vhost\n')
	except:
		myout.write('['+PRIVATE_IP+'] out: can\'t create vhost\n')
		return json.dumps({'addappfinish': 1,
						   'console': "",
						   'registered': "Internal Server Error"})

	# domain pointing
	try:
		domain_id = Dnsmadeeasy.get_domain_id(TOPDOMAIN)
		myout.write('['+PRIVATE_IP+'] out: get domain id\n')
	except Exception as inst:
		return json.dumps({'addappfinish': 1,
						   'console': "",
						   'registered': inst.args})

	if domain_id == None:
		return json.dumps({'addappfinish': 1,
						   'console': "",
						   'registered': "Internal Server Error"})
	data = json.dumps({
		"name": SUBDOMAIN,
		"type": "A",
		"value": PUBLIC_IP,
		"gtdLocation": "DEFAULT",
		"ttl": 1800
	}, separators=(',', ':'))

	try:
		Dnsmadeeasy.add_subdomain(domain_id=domain_id, data=data)
		myout.write('['+PRIVATE_IP+'] out: add subdomain\n')
	except Exception as inst:
		return json.dumps({'addappfinish': 1,
						   'console': "",
						   'registered': inst.args})

	##############################################
	##              DATABASE SIDE               ##
	##############################################
	dicti = {
		App.APP_NAME: APP_NAME,
		App.APP_DOMAIN: [APP_DOMAIN],
		App.APP_DIR: APP_DIR,
		App.APP_REPO: APP_REPO,
		App.APP_ENV: APP_ENV,
		App.APP_HOST: APP_HOST
	}
	App.insert_one(dicti)
	myout.write('['+PRIVATE_IP+'] out: insert to database\n')

	finish = 1

startadd = 0
where = 0
@antares.route('/addapplication', methods=['POST'])
def addapplication():
	if sessionvalue not in session:
		abort(404)
	# global
	global where
	global finish
	global startadd
	global myout

	# variable post
	APP_NAME = request.json['app_name']
	SUBDOMAIN = request.json['subdomain'].lower()
	TOPDOMAIN = request.json['domain'].lower()
	APP_REPO = request.json['app_repo'].lower()
	APP_ENV = request.json['app_env'].lower()
	APP_HOST = request.json['app_host'].title()
	FINISH = request.json['finish']
	APP_DOMAIN = SUBDOMAIN +"."+ TOPDOMAIN
	PUBLIC_IP = Server.find_one({Server.ALIAS: APP_HOST})[Server.PUBLIC_IP]

	#variable fabric
	env.user = "root"
	env.key_filename = "/var/www/.ssh/id_rsa"
	env.host_string = Server.find_one({Server.ALIAS:APP_HOST})[Server.PRIVATE_IP]





	cpmyout = copy.copy(myout)
	if FINISH == 1 :
		finish = 0
		startadd = 0
	if startadd == 0:
		##############################################
		##                 VALIDITY                 ##
		##############################################

		# check if app name exist
		registered = App.find_one({App.APP_NAME: APP_NAME})
		if registered != None:
			return json.dumps({'addappfinish': 1,
							   'console': "",
							   'registered': "this app name already exist please choose another name"})

		# check if domain exist
		try:
			domain_id = Dnsmadeeasy.get_domain_id(topdomain=TOPDOMAIN)
			record_id = Dnsmadeeasy.get_record_id(domain_id=domain_id,subdomain=SUBDOMAIN)
		except Exception as inst:
			return json.dumps({'addappfinish': 1,
							   'console': "",
							   'registered': inst.args})
		if record_id != False:
			return json.dumps({'addappfinish': 1,
							   'console': "",
							   'registered': "this domain already exist please choose another domain"})

		# check if repository and branch and server in App
		registered = App.find_one({App.APP_REPO: APP_REPO, App.APP_ENV: APP_ENV, App.APP_HOST: APP_HOST})
		if registered != None:
			return json.dumps({'addappfinish': 1,
							   'console': "",
							   'registered': "this app already exist"})

		# check if git exist
		try:
			result = run('git ls-remote %s' % APP_REPO)

			# check if branch exist
			branch = None
			for line in result.splitlines()[1:]:
				if line.split('refs/heads/')[1] == APP_ENV:
					branch = True
			if branch == None:
				return json.dumps({'addappfinish': 1,
								   'console': "",
								   'registered': "branch not found"})

		except:
			return json.dumps({'addappfinish': 1,
							   'console': "",
							   'registered': "Internal Server Error"})
		##############################################
		##                SERVER SIDE               ##
		##############################################

		# create docroot
		APP_DIR = '/var/www/html/' + APP_REPO.split('git@gitlab.com:inzpire/')[1].split('.git')[0] + '/' + APP_ENV
		#APP_DIR = '/home/aar/'+ APP_REPO.split('git@gitlab.com:inzpire/')[1].split('.git')[0] + '/' + APP_ENV

		# clone repo
		thread.start_new_thread(clone, (APP_REPO, APP_DIR,TOPDOMAIN,APP_DOMAIN,SUBDOMAIN,PUBLIC_IP,APP_NAME,APP_ENV,APP_HOST,env.host_string))

		startadd = 1
		return json.dumps({'addappfinish':0,'console':""})
	else:
		cpmyout.seek(where)
		line = cpmyout.readline()
		if not line:
			return json.dumps({'addappfinish': finish, 'console': ""})
		else:
			where += len(line)
			return json.dumps({'addappfinish': 0, 'console': line})

TEMPLATE_CONTENTS_SSL = '''
<VirtualHost *:80>
	ServerName %(url)s
	Redirect / https://%(url)s/
</VirtualHost>

<VirtualHost *:443>
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
	SSLEngine on
	SSLCertificateFile /ssl/%(topdomain)s/star.%(topdomain)s.crt
	SSLCertificateKeyFile /ssl/%(topdomain)s/star.%(topdomain)s.key
	SSLCACertificateFile /ssl/%(topdomain)s/star.%(topdomain)s-intermediate.crt
	ErrorLog ${APACHE_LOG_DIR}/%(url)s/error.log
	CustomLog ${APACHE_LOG_DIR}/%(url)s/access.log combined
</VirtualHost>
'''

TEMPLATE_CONTENTS='''
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
        ErrorLog ${APACHE_LOG_DIR}/%(url)s/error.log
        CustomLog ${APACHE_LOG_DIR}/%(url)s/access.log combined
</VirtualHost>
'''

@antares.route('/adddatabase', methods=['POST'])
def adddatabase():
	if sessionvalue not in session:
		abort(404)

	# variable post
	DB_NAME = request.json['db_name']
	DB_USER = request.json['db_user']
	DB_PASS = request.json['db_pass']
	DB_HOST = request.json['db_host']

	# set env
	env.host_string = Server.find_one({Server.ALIAS: DB_HOST})[Server.PRIVATE_IP]

	# validity
	exist = Mysql.find_one({Mysql.DB_NAME:DB_NAME,Mysql.DB_HOST:DB_HOST})
	if exist != None:
		return json.dumps({
			'adddatabase': False,
			'registered': "this database name already exist please choose another name"})

	# create user if not exist
	if not fabtools.mysql.user_exists(DB_USER) and not fabtools.mysql.database_exists(DB_NAME):
		fabtools.mysql.create_user(name=DB_USER, password=DB_PASS,host='%')
		fabtools.mysql.create_database(name=DB_NAME, owner=DB_USER)
		try:
			run('mysql -e "GRANT ALL ON '+DB_NAME+".* To '"+DB_USER+"'@'%' IDENTIFIED BY '"+DB_PASS+"' WITH GRANT OPTION;\"")
			run(
				'mysql -e "GRANT ALL ON ' + DB_NAME + ".* To '" + DB_USER + "'@'localhost' IDENTIFIED BY '" + DB_PASS + "' WITH GRANT OPTION;\"")
		except Exception as inst:
			return json.dumps({
				'adddatabase': False,
				'registered': inst.args})

	else:
		return json.dumps({
				'adddatabase': False,
				'registered': "this database or user already exist"})

	# insert database
	Mysql.insert_one({
		Mysql.DB_NAME:DB_NAME,
		Mysql.DB_USER:DB_USER,
		Mysql.DB_PASS:DB_PASS,
		Mysql.DB_HOST:DB_HOST
	})

	return json.dumps({
		'adddatabase': True,
		'registered': "successfully registered"})

# will be deleted
# @antares.route('/deletedatabase', methods=['POST'])
# def deletedatabase():
# 	if sessionvalue not in session:
# 		abort(404)
#
# 	# variable post
# 	OID = request.json['oid']
# 	#
# 	# raw = Mysql.delete_one({Mysql.ID:ObjectId(OID)}).raw_result
# 	return json.dumps({
# 		'deletedatabase': True,
# 		'registered': OID
# 	})

@antares.route('/adddomain', methods=['POST'])
def addomain():
	if sessionvalue not in session:
		abort(404)


	# variable post
	APP_DOMAIN = request.json['app_domain']
	APP_ID = request.json['app_id']

	SUBDOMAIN , TOPDOMAIN = APP_DOMAIN.split('.',1)

	server = App.find_one({App.ID: ObjectId(APP_ID)})[App.APP_HOST]

	env.host_string = Server.find_one({Server.ALIAS:server})[Server.PRIVATE_IP]

	# check if domain exist
	exist = Dnsmadeeasy.check_if_domain_exist(domain=APP_DOMAIN)
	if not exist:
		return json.dumps({'status': 403,
						   'result': "this domain already exist please choose another domain"})

	# create virtualhost
	APP_DIR = App.find_one({App.ID:ObjectId(APP_ID)})[App.APP_DIR]

	crt = contribfiles.exists('/ssl/' + TOPDOMAIN + '/star.' + TOPDOMAIN + '.crt', )
	key = contribfiles.exists('/ssl/' + TOPDOMAIN + '/star.' + TOPDOMAIN + '.key')
	intermediate = contribfiles.exists('/ssl/' + TOPDOMAIN + '/star.' + TOPDOMAIN + '-intermediate.crt')

	if crt == True and key == True and intermediate == True:
		template = TEMPLATE_CONTENTS_SSL
	else:
		template = TEMPLATE_CONTENTS

	try:
		fabtools.require.files.directory('/var/log/apache2/' + APP_DOMAIN)
		fabtools.require.files.directory(APP_DIR)
		fabtools.require.apache.site(APP_DOMAIN, template_contents=template, url=APP_DOMAIN,
									 doc_root=APP_DIR, topdomain=TOPDOMAIN)
	except:
		return json.dumps({'status': 407,
						   'result': "cannot create virtual host"})

	# get public ip
	public_ip = Server.find_one({Server.ALIAS:server})[Server.PUBLIC_IP]

	# domain pointing

	data = json.dumps({
		"name": SUBDOMAIN,
		"type": "A",
		"value": public_ip,
		"gtdLocation": "DEFAULT",
		"ttl": 1800
	}, separators=(',', ':'))

	domain_id = Dnsmadeeasy.get_domain_id(TOPDOMAIN)
	try:
		Dnsmadeeasy.add_subdomain(domain_id=domain_id,data=data)
	except Exception as inst:
		return json.dumps({'status':401,'result':inst.args})

	App.update({App.ID:ObjectId(APP_ID)},{'$push':{App.APP_DOMAIN:APP_DOMAIN}})

	return json.dumps({'status': 200, 'result': 'success'})

@antares.route('/deletedomain', methods=['POST'])
def deletedomain():
	if sessionvalue not in session:
		abort(404)

	# variable post
	APP_ID = request.json['app_id']
	APP_DOMAIN = request.json['app_domain']

	SUBDOMAIN, TOPDOMAIN = APP_DOMAIN.split('.',1)

	# get domain_id
	try:
		domain_id = Dnsmadeeasy.get_domain_id(topdomain=TOPDOMAIN)
	except Exception as inst:
		return json.dumps({'status': 417, 'result': inst.args})

	# get record_id
	try:
		record_id = Dnsmadeeasy.get_record_id(domain_id=domain_id,subdomain=SUBDOMAIN)
	except Exception as inst:
		return json.dumps({'status': 417, 'result': inst.args})

	# delete record_id
	try:
		Dnsmadeeasy.delete_record(domain_id=domain_id,record_id=record_id)
	except Exception as inst:
		return json.dumps({'status': 417, 'result': inst.args})

	# delete vhost
	try:
		fabtools.require.apache.site_disabled(APP_DOMAIN)
		fabtools.service.reload('apache2')
		fabtools.files.remove('/etc/apache2/sites-available/%s.conf' % (APP_DOMAIN))
		fabtools.files.remove('/var/log/apache2/' + APP_DOMAIN, recursive=True)

	except Exception as inst:
		return json.dumps({'status': 417, 'result': inst.args})

	App.update({App.ID:ObjectId(APP_ID)},{'$pull':{App.APP_DOMAIN:APP_DOMAIN}})
	return json.dumps({'status': 200, 'result': 'success'})

if __name__ == '__main__':
	antares.run(debug=True)
	#antares.run(debug=False)
