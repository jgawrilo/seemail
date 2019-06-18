import connexion
import six
import redis

from swagger_server.models.email import Email  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.multipart_email import MultipartEmail # noqa: E501
from swagger_server import util

import imbox
import random
import string
import re
import json
import os
from glob import glob
from datetime import datetime
import logging
import sqlite3 as sql
import base64

from kafka import KafkaProducer

import email
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# mailinabox management functions
import sys
sys.path.append('/home/andrew/mailinabox/management/')
import utils
import mailconfig

def generate_password(length = 18):
    return ''.join([random.choice(string.ascii_letters + string.digits ) for n in range(length)])

def parse_attach(x):
    if 'content' in x:
        #print(type(x["content"]))
        x["content"] = str(x["content"].getvalue())
    return x

def fix_body(x):
    try:
        return str(x.decode("utf-8"))
    except:
        return x

def transform_email(message, request_key = None):
    email_json = {}
    if request_key is not None:
        email_json["request_key"] = request_key
    email_json["sent_from"] = message.sent_from
    email_json["sent_to"] = list(message.sent_to)
    email_json["cc"] = list(message.cc)
    email_json["bcc"] = list(message.bcc)
    email_json["message_id"] = message.message_id
    email_json["parsed_date"] = message.parsed_date.isoformat()

    #email_json["flags"] = list(map(lambda x: str(x.decode("utf-8")),message.flags))
    email_json["date"] = message.date
    email_json["body"] = {}
    email_json["body"]["plain"] = list(map(fix_body,message.body["plain"]))
    email_json["body"]["html"] = list(map(fix_body,message.body["html"]))
    email_json["subject"] = message.subject
    email_json["headers"] = message.headers
    email_json["raw_email"] = message.raw_email
    email_json["attachments"] = list(map(parse_attach,message.attachments))

    # headers, body, attacments, raw_email
    email_json["other"] = {}

    ee = email.message_from_string(email_json["raw_email"])
    for i,j in ee.items():
        email_json["other"][i] = ee.get_all(i)

    return email_json

def check_email_for_addresses(transformed, addresses):
    send_to_kafka = False
    for field in ["sent_from", "sent_to", "cc"]:
        for recipient in transformed[field]:
            if recipient['email'] in addresses:
                send_to_kafka = True
                break
        # Don't need to check other fields if we already have a match
        if send_to_kafka:
            break
    # Search "Received" field for BCC'd users if we're not already sending
    if not send_to_kafka:
        for item in transformed["other"]["Received"]:
            for email in addresses:
                if re.search(email, item) is not None:
                    send_to_kafka = True
                    break
                if send_to_kafka:
                    break
    return send_to_kafka

def create_bot_account_post(user):  # noqa: E501
    """Create a bot email account to send/receive messages from.

     # noqa: E501

    :param user: The bot user to send/receive messages from.
    :type user: dict | bytes

    :rtype: bool
    """
    bots_r = redis.StrictRedis(host='localhost', port=6379, db=2)
    deactivated_bots_r = redis.StrictRedis(host='localhost', port=6379, db=3)
    reactivating = False
    if connexion.request.is_json:
        user = User.from_dict(connexion.request.get_json())  # noqa: E501

    # Load mailinabox env variables
    env = utils.load_environment()

    # If we're reactivating a deactivated bot account, delete it from the deactivated list
    if user.email_address.encode('utf-8') in deactivated_bots_r.scan_iter():
        deactivated_bots_r.delete(user.email_address)
        reactivating = True

    # Load bot credentials file
    with open('/home/andrew/seemail/seemail/server_code/bcr.json', 'r') as f:
        creds = json.load(f)

    # Generate a password and create the actual email account
    if user.email_address in creds:
        pwd = creds[user.email_address]
    else:
        pwd = generate_password()
        creds[user.email_address] = pwd
        with open('/home/andrew/seemail/seemail/server_code/bcr.json', 'w') as f:
            json.dump(creds, f)

    # Add mailbox for bot
    res = mailconfig.add_mail_user(user.email_address, pwd, "", env)

    # Add to our Redis bot account db
    res = bots_r.set(user.email_address, 1)

    # Add first and last names to names sqlite db (separate from the mailinabox
    # db file to avoid messing up any of their management services)
    conn1 = sql.connect('/home/user-data/mail/users.sqlite')
    conn2 = sql.connect('/home/user-data/mail/user_names.sqlite')
    cur1 = conn1.cursor()
    cur2 = conn2.cursor()
    user_id = cur1.execute('select id from users where email="{}"'.format(user.email_address)).fetchone()[0]
    try:
        cur2.execute('insert into names values  ({}, "{}", "{}", "{}")'.format(user_id,
            user.first_name, user.last_name, user.email_address))
    except sql.IntegrityError:
        pass # User already in the names DB, might hit this when reactivating an existing bot
    conn2.commit()
    cur1.close()
    cur2.close()
    conn1.close()
    conn2.close()

    if reactivating is False:
        logging.info("Added bot account {}".format(user.email_address))
    else:
        logging.info("Reactivated bot account {}".format(user.email_address))

    return res


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
    # Decode from bytes to string for JSON encoding
    decoded_users = [User(email_address = x.decode('utf-8')) for x in users]
    # Get first and last names
    conn = sql.connect("/home/user-data/mail/user_names.sqlite")
    cur = conn.cursor()
    for i in range(0, len(decoded_users)):
        try:
            decoded_users[i].first_name = cur.execute("select first_name from names where email = {}".format(decoded_users[i].email_address)).fetchone()[0]
            decoded_users[i].last_name = cur.execute("select last_name from names where email = {}".format(decoded_users[i].email_address)).fetchone()[0]
        except:
            logging.warning("No first or last name found for {}".format(decoded_users[i].email_address))
    cur.close()
    conn.close()

    logging.info("Returned list of users")

    return decoded_users

def monitor_users_get(email_addresses):  # noqa: E501
    """Add users to set to monitor email for (sent to kafka)

     # noqa: E501

    :param email_addresses: The full email addresses of the users to montor
    :type email_addresses: List[str]

    :rtype: List[bool]
    """
    users_r = redis.StrictRedis(host='localhost', port=6379, db=1)
    results = []
    for address in email_addresses:
        res = users_r.set(address, 1)
        results.append(res)

    logging.info("Added list of email addresses to monitor: {}".format(email_addresses))

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
    logging.info("Deactivated list of bot accounts: {}".format(email_addresses))
    return True


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
    res = []
    # Should add a check that the date is in the correct format, if there isn't one higher in the API definition
    in_dt = back_to_iso_date_string.split("T")[0].replace('-', '')
    back_to_unix = int((datetime.strptime(in_dt, '%Y%m%d')-datetime(1970,1,1)).total_seconds())

    producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    try:
        filelist = []
        for folder in ('tmp', 'new', 'cur'):
            filelist += glob('/var/archive/mail/{}/*'.format(folder))
        for filename in filelist:
            # Skip if email timestamp before limit
            ts = int(filename.split('/')[-1].split('.')[0])
            if ts < back_to_unix:
                continue
            mail = "".join(open(filename).readlines())
            mail_dict = imbox.parser.parse_email(mail)
            transformed = transform_email(mail_dict, request_key)
            if check_email_for_addresses(transformed, email_addresses):
                producer.send("history", transformed)
                producer.flush()
        res.append(True)
        logging.info("Sent email history for {}".format(email_addresses))
    except Exception as e:
        raise
        res.append(False)
        logging.error("Error sending email history for {}:\n    {}".format(email_addresses, e))
    return res


def request_send_mail_post(email):  # noqa: E501
    """Send the email.

     # noqa: E501

    :param email: The email to send.
    :type email: dict | bytes

    :rtype: bool
    """
    if connexion.request.is_json:
        email = Email.from_dict(connexion.request.get_json())  # noqa: E501

    s = smtplib.SMTP("localhost:587")
    # Build MIME email from email object? Need to double check input format
    msg = MIMEMultipart()
    recipients = []
    for field in (email.sent_to, email.sent_cc, email.sent_bcc):
    	recipients += [x.email_address for x in field]
    msg['To'] = ', '.join([x.email_address for x in email.sent_to])
    msg['CC'] = ', '.join([x.email_address for x in email.sent_cc])
    msg['From'] = "{} {} <{}>".format(email.sent_from.first_name,
        email.sent_from.last_name, email.sent_from.email_address)
    if email.reply_to_id != '':
        msg['In-Reply-To'] = email.reply_to_id
        msg['References'] = email.reply_to_id
    elif email.forward_id != '':
        msg['In-Reply-To'] = email.forward_id
        msg['References'] = email.forward_id
    msg['Subject'] = email.subject

    # Add additional headers
    for header in email.headers:
        if header.key not in msg:
            msg.add_header(header.key, header.value)

    msg.attach(MIMEText(email.body))

    # Handle attachements
    for a in email.attachments:
        part = MIMEApplication(base64.b64decode(a.base64_string), Name = a.name)
        part['Content-Disposition'] = 'attachment; filename="{}"'.format(a.name)
        msg.attach(part)

    # Load bot credentials file
    with open('/home/andrew/seemail/seemail/server_code/bcr.json', 'r') as f:
        creds = json.load(f)
        pwd = creds[email.sent_from.email_address]
    s.connect('localhost:587')
    s.starttls()
    s.login(email.sent_from.email_address, pwd)

    # Send it!
    s.sendmail(email.sent_from.email_address, recipients, msg.as_string())
    s.close()
    logging.info("Sent email from {} to {}".format(email.sent_to, email.sent_from))
    return True


def request_send_multipart_mail_post(email):  # noqa: E501
    """Send the multipart-email.

     # noqa: E501

    :param email: The email to send.
    :type multipart_email: dict | bytes

    :rtype: bool
    """
    if connexion.request.is_json:
        email = MultipartEmail.from_dict(connexion.request.get_json())  # noqa: E501

    s = smtplib.SMTP("localhost:587")
    # Build MIME email from email object? Need to double check input format
    msg = MIMEMultipart()
    recipients = []
    for field in (email.sent_to, email.sent_cc, email.sent_bcc):
    	recipients += [x.email_address for x in field]
    msg['To'] = ', '.join([x.email_address for x in email.sent_to])
    msg['CC'] = ', '.join([x.email_address for x in email.sent_cc])
    msg['From'] = "{} {} <{}>".format(email.sent_from.first_name,
        email.sent_from.last_name, email.sent_from.email_address)
    if email.reply_to_id != '':
        msg['In-Reply-To'] = email.reply_to_id
        msg['References'] = email.reply_to_id
    elif email.forward_id != '':
        msg['In-Reply-To'] = email.forward_id
        msg['References'] = email.forward_id
    msg['Subject'] = email.subject

    # Add additional headers
    for header in email.headers:
        if header.key not in msg:
            msg.add_header(header.key, header.value)

    msg, err = parseMultipartEmailBody(msg, email.body)
    if err != "" and err != None:
        logging.error("Error building message body")

    # Load bot credentials file
    with open('/home/andrew/seemail/seemail/server_code/bcr.json', 'r') as f:
        creds = json.load(f)
        pwd = creds[email.sent_from.email_address]
    s.connect('localhost:587')
    s.starttls()
    s.login(email.sent_from.email_address, pwd)

    # Send it!
    s.sendmail(email.sent_from.email_address, recipients, msg.as_string())
    s.close()
    logging.info("Sent email from {} to {}".format(email.sent_to, email.sent_from))
    return True

def unmonitor_users_get(email_addresses):  # noqa: E501
    """Remove users from set to monitor email for (sent to kafka)

     # noqa: E501

    :param email_addresses: The full email addresses of the users to unmonitor
    :type email_addresses: List[str]

    :rtype: List[bool]
    """
    users_r = redis.StrictRedis(host='localhost', port=6379, db=1)
    res_codes = {1: True, 0: False}
    results = []
    for address in email_addresses:
        res = users_r.delete(address)
        results.append(res_codes[res])
    logging.info("Unmonitored list of users: {}".format(email_addresses))
    return results

def parseMultipartEmailBody(msg, body):
    partType = body["partType"]
    if partType == 'multipart/mixed':
        # Throw error - Cannot be an inner type
        return msg, "Message is already of type multipart/mixed, cannot be an inner type"
    elif partType == 'multipart/alternative':
        # Add part multipart/alternative then call parseMultipartEmailBody with array elements
        part = MIMEMultipart('alternative')
        for x in body["bodyArray"]:
            part, err = parseMultipartEmailBody(part, x)
        msg.attach(part)
    elif partType == 'multipart/related':
        # Add part multipart/alternative then call parseMultipartEmailBody with array elements
        part = MIMEMultipart('related')
        for x in body["bodyArray"]:
            part, err = parseMultipartEmailBody(part, x)
        msg.attach(part)
        return msg, err
        # return msg
    elif partType == 'text/plain':
        # Add part text/plain
        part = MIMEText(body["bodyString"], 'plain')
        msg.attach(part)
        # return msg
    elif partType == 'text/html':
        # Add part text/html
        part = MIMEText(body["bodyString"], 'html')
        msg.attach(part)
        # return msg
    elif partType.split('/')[0] == 'image':
        img = MIMEImage(base64.b64decode(body["bodyString"]))
        msg.attach(img)
    elif partType == 'attachment':
        part = MIMEApplication(base64.b64decode(body["bodyString"]), Name = body["name"])
        part['Content-Disposition'] = 'attachment; filename="{}"'.format(body["name"])
        msg.attach(part)
    else:
        # Anything else assume attachment
        # Add part
        part = MIMEApplication(base64.b64decode(body["bodyString"]), Name = body["name"])
        part['Content-Disposition'] = 'attachment; filename="{}"'.format(body["name"])
        msg.attach(part)
        # return msg
    return msg, None
    