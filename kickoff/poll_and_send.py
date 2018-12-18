import redis

import datetime
import json
import time
from imbox import Imbox
import sys
import datetime
import json
import email

from kafka import KafkaProducer

r = redis.StrictRedis(host='localhost', port=6379, db=0)
producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))

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

def transform_email(message):
    email_json = {}
    email_json["sent_from"] = message.sent_from
    email_json["sent_to"] = list(message.sent_to)
    email_json["cc"] = list(message.cc)
    email_json["bcc"] = list(message.bcc)
    email_json["message_id"] = message.message_id
    email_json["parsed_date"] = message.parsed_date.isoformat()

    email_json["flags"] = list(map(lambda x: str(x.decode("utf-8")),message.flags))
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

now = datetime.date.today()

while True:
    for key in r.scan_iter():
        login = json.loads(key)
        with Imbox(login["server"],
            username=login["user"],
            password=login["password"],
            ssl=True,
            ssl_context=None,
            starttls=False) as imbox:
            inbox_messages_received_after = imbox.messages(date__gt=now)
            for uii, m in inbox_messages_received_after:
                if not r.get(key):
                    r.set(key,int(uii))
                elif int(uii) > int(r.get(key)):
                    r.set(key,int(uii))
                    producer.send("email",transform_email(m))
                    producer.flush()
                

    print("Checked")
    time.sleep(1)



