- This is Documentation for Antares Deployer

- Antares Core

1. Make sure root on antares server can execute command on remote server without password
command: ssh-copy-id root@<private ip>

2. Register Server
command: antares.py -rs <public ip> <private ip> <server codename>
NB : If not have Public IP just replace with dash '-', DO NOT LET IT EMPTY!

3. Register Application
command: antares.py -ra <app name> <app domain> <app repo> <app directory> <app host>
NB : App Host MUST fill with registered server, use antares.py -sl to check server detail

4. Register Database
command: antares.py -rd <db host> <db name> <db user>
NB : password for "db user" is generated automatically 

- LET THE PLEASURE BEGIN

 by: root@inzpire-devops
 contact:
 	root@inzpire-devops# cat /root/contact.txt

 "Focus on your code, not the Infrastructure" - AWS
