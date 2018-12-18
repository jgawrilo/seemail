import sys
import time
import logging
import email
import json
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
import imbox

class Watcher(FileSystemEventHandler):
    def on_created(self,event):
        if "new" in event.src_path:
            print(event.src_path)
            mail = "".join(open(event.src_path).readlines())
            mail_dict = imbox.parser.parse_email(mail)
            transformed = transform_email(mail_dict)
            print(json.dumps(transformed,indent=2))

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


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '/var/archive/mail/'
    event_handler = Watcher()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
