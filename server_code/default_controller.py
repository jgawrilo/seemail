import connexion
import six
import redis

from swagger_server.models.email import Email  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server import util

import imbox
import random
import string
import json
import os
from glob import glob
from kafka import KafkaProducer

import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# mailinabox management functions
import sys
sys.path.append('/root/mailinabox/management/')
import utils
import mailconfig

def generate_password(length = 18):
    return ''.join([random.choice(string.ascii_letters + string.digits ) for n in range(length)])

def create_bot_account_post(user):  # noqa: E501
    """Create a bot email account to send/receive messages from.

     # noqa: E501

    :param user: The bot user to send/receive messages from.
    :type user: dict | bytes

    :rtype: bool
    """
    bots_r = redis.StrictRedis(host='localhost', port=6379, db=2)
    responses = {}
    res_codes = {True: "Success", False: "Failed"}
    if connexion.request.is_json:
        user = User.from_dict(connexion.request.get_json())  # noqa: E501

    # Load mailinabox env variables
    env = utils.load_environment()

    # Generate a password and create the actual email account
    pw = generate_password()

    # Add mailbox for bot
    res = mailconfig.add_mail_user(user, pwd, "", env)
    reponses['mailbox'] = res

    # Add to our Redis bot account db
    res = bots_r.set(user, 1)
    responses['redis'] = res_codes[res]
    
    return responses


def get_all_users():  # noqa: E501
    """Get all users on email server

     # noqa: E501


    :rtype: List[User]
    """
    bots_r = redis.StrictRedis(host='localhost', port=6379, db=2)
    deactivated_bots_r = redis.StrictRedis(host='localhost', port=6379, db=3)
    ## Not sure if this will work on all email implementations. 
    ## Needs location of mailboxes on server, and permission to access that location
    users = []
    domains = os.listdir('/home/user-data/mail/mailboxes')
    for domain in domains:
        temp_users = os.listdir('/home/user-data/mail/mailboxes/{}/'.format(domain))
        for name in temp_users:
            users.append("{}@{}".format(name, domain).encode('utf-8'))
    # Get bots to exclude, we only want to return real users
    bots = []
    for key in bots_r.scan_iter():
        bots.append(key)
    # also exclude deactivated bots
    for key in deactivated_bots_r.scan_iter():
        bots.append(key)
    users = list(set(users) - set(bots))
    return users


def monitor_users_get(email_addresses):  # noqa: E501
    """Add users to set to monitor email for (sent to kafka)

     # noqa: E501

    :param email_addresses: The full email addresses of the users to montor
    :type email_addresses: List[str]

    :rtype: List[bool]
    """
    users_r = redis.StrictRedis(host='localhost', port=6379, db=1)
    res_codes = {True: "Success", False: "Failed"}
    results = []
    for address in email_addresses:
        res = users_r.set(address, 1)
        results.append(res_codes[res])
    return results


def remove_bot_account_get(email_addresses):  # noqa: E501
    """Remove a bot email account to send/receive messages from.

     # noqa: E501

    :param email_addresses: The full email addresses of the bot user to remove
    :type email_addresses: str

    :rtype: bool
    """
    bots_r = redis.StrictRedis(host='localhost', port=6379, db=2)
    deactivated_bots_r = redis.StrictRedis(host='localhost', port=6379, db=3)
    # Delete account from Redis bot account db and add to defunct bots db
    for address in email_addresses:
        res = bots_r.delete(address)
        res2 = deactivated_bots_r.set(address, 1)
    # Actually remove the email account? Or leave it for later analysis?
    return res_codes[res]


def request_mail_history_get(email_addresses, request_key, back_to_iso_date_string):  # noqa: E501
    """Have all email involving users sent to historic kafka topic.

     # noqa: E501

    :param email_addresses: The full email addresses of the users to montor
    :type email_addresses: List[str]
    :param request_key: The provided key from requesting client to tag results with.
    :type request_key: str
    :param back_to_iso_date_string: The date back to retrieve email messages from.
    :type back_to_iso_date_string: str

    :rtype: List[bool]
    """
    producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    for address in email_addresses:
        user = address.split('@')[0]
        domain = address.split('@')[1]
        filelist = glob('/home/user-data/mail/mailboxes/{}/{}/*/*'.format(domain, user))
        for filename in filelist:    
            mail = "".join(open(filename).readlines())
            mail_dict = imbox.parser.parse_email(mail)
            # Need to decide whether to put transform function in this file or other
            transformed = transform_email(mail_dict)
            producer.send("history", transformed)
            producer.flush()
    return 'do some magic!'


def request_send_mail_post(email):  # noqa: E501
    """Send the email.

     # noqa: E501

    :param email: The email to send.
    :type email: dict | bytes

    :rtype: bool
    """
    if connexion.request.is_json:
        email = Email.from_dict(connexion.request.get_json())  # noqa: E501

    s = smtplib.SMTP("localhost:smtp")
    # Build MIME email from email object? Need to double check input format
    msg = MIMEMultipart()
    recipients = email['sent_to'] + email['sent_cc'] + email['sent_bcc']
    msg['To'] = email['sent_to']
    msg['CC'] = email['sent_cc']
    msg['Subject'] = email['subject']
    msg.attach(MIMEText(email['body']))

    # Handle attachements
    for a in email['attachments']:
        with open(a['name'], 'rb') as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(f))
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

from email.mime.multipart import MIMEMultipart
    s.sendmail(email['sent_from'], recipients, msg.as_string())
    s.close()
    return True


def unmonitor_users_get(email_addresses):  # noqa: E501
    """Remove users from set to monitor email for (sent to kafka)

     # noqa: E501

    :param email_addresses: The full email addresses of the users to unmonitor
    :type email_addresses: List[str]

    :rtype: List[bool]
    """
    users_r = redis.StrictRedis(host='localhost', port=6379, db=1)
    res_codes = {1: "Success", 0: "Failed"}
    results = []
    for address in email_addresses:
        res = users_r.delete(address)
        results.append(res_codes[res])
    return results
