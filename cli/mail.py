#!/usr/bin/env python

import smtplib

from email.mime.text import MIMEText
from email.parser import Parser

class mail(object):
	def __init__(self):
		super(mail, self).__init__()

	def send_mail(self, receiver="", body=""):
		msg = MIMEText(body)
		msg['Subject']  = "Inzpire Technology DevOps Service"
		msg['From'] = "InzpireTech DevOps <devops@inzpire.co.id>"
		msg['To'] = receiver

		s = smtplib.SMTP('localhost')
		s.sendmail(msg['From'], [msg['To']], msg.as_string())
		s.quit()

if __name__ == '__main__':
	pass