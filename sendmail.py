#!/usr/bin/python

import smtplib

sender = 'lol@far.com'
receivers = ['juddy.g@gmail.com']

message = """From: Justin <lol@far.com>
To: Justin G <juddy.g@gmail.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

try:
   smtpObj = smtplib.SMTP('localhost')
   smtpObj.sendmail(sender, receivers, message)         
   print "Successfully sent email"
except SMTPException:
   print "Error: unable to send email"
