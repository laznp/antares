#!/usr/bin/env python

import smtplib

from email.mime.text import MIMEText
from email.parser import Parser

class antamail(object):
	def __init__(self):
		super(antamail, self).__init__()

	def send_mail(self, receiver="", body=""):
		msg = MIMEText(body)
		msg['Subject']  = "Inzpire Tech DevOps Service"
		msg['From'] = "devops@inzpire.co.id"
		msg['To'] = receiver

		s = smtplib.SMTP('localhost')
		s.sendmail(msg['From'], [msg['To']], msg.as_string())
		s.quit()

if __name__ == '__main__':
	pass