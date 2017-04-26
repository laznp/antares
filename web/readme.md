- This is Documentation for Antares Deployer

- Antares Core

1. Make sure root on antares server can execute command on remote server without password
command: ssh-copy-id -i /root/.ssh/id_rsa.pub root@<remote server>

2. Register Server
command: antares.py -rs <public ip> <private ip> <server alias>
NB : If not have Public IP just replace with dash '-', DO NOT LET IT EMPTY!

3. Register Application
command: antares.py -ra <app name> <app domain> <app env[dev|prod]> <app repo> <app directory> <app host>
NB : App Host MUST fill with registered server, use antares.py -sl to check server detail

4. Register Database
command: antares.py -rd <db host> <db name> <db user>
NB : password for "db user" is generated automatically 

- Antares Webhook

1. Make sure www-data/apache user can execute root on remote server
	- Make public key on /var/www/.ssh
	command: sudo -u www-data ssh-keygen
	- Copy public key to remote server
	command: ssh-copy-id -i /var/www/.ssh/id_rsa.pub root@<remote server>

2. Add webhook to git/svn hosting with url "http://antares.inzpire.co.id/pull/\<server alias\>/\<app name\>"
NB : Use "antares.py -sl" for check server alias, and "antares.py -al" for check app name

- LET THE PLEASURE BEGIN

 by: root@inzpire-devops
 contact:
 	root@inzpire-devops# cat /root/contact.txt

 "Focus on your code, not the Infrastructure" - AWS
