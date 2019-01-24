import sys
import time
import logging
import json
import requests
import redis
import random
import sqlite3 as sql
import base64
from os import path
from datetime import datetime
from nltk.corpus import gutenberg

hostname = "box.chunkman.com"
mail_home = "/home/user-data/mail"

def clean_sentences(sentences):
  return sentences.replace(" ,", "").replace(" ' ", "'").replace(" .", ".").replace(" ?", "?").replace(" :", ":")

def send_email(attachment_fname):
    bots_r = redis.StrictRedis(host='localhost', port=6379, db=2)
    active_bots = []
    for b in bots_r.scan_iter():
        active_bots.append(b.decode('utf-8'))
    random.shuffle(active_bots)

    # Get first and last names for our bots
    names = {}
    conn = sql.connect('{}/user_names.sqlite'.format(mail_home))
    cur = conn.cursor()
    cur.execute("select * from names")
    rows = cur.fetchall()
    for row in rows:
        if row[3] in active_bots:
            names[row[3]] = {"first": row[1], "last": row[2]}

    print(names)
    sender = {"email_address": active_bots[0], 
              "first_name": names[active_bots[0]]["first"],
              "last_name": names[active_bots[0]]["last"]}
    receivers = [
                 {"email_address": active_bots[1],
                  "first_name": names[active_bots[1]]["first"],
                  "last_name": names[active_bots[1]]["last"]
                 },
                ]

    all_sents = gutenberg.sents('milton-paradise.txt')
    start = random.randint(0, len(all_sents)-10)
    subj = clean_sentences(" ".join(all_sents[start]))
    body = []
    for i in range(start+1, random.randint(start+2,start+4)):
        body.append(" ".join(all_sents[i]))
        print(body)
    body = " ".join(body)
    body = clean_sentences(body)
    print(body)

    # Decide whether to cc anyone
    if random.random() > 0.8:
        cc = []
    else:
        cc = [{"email_address": active_bots[2],
               "first_name": names[active_bots[2]]["first"],
               "last_name": names[active_bots[2]]["last"]
              },
             ]

    # Decide whether to attach an image
    attachments = []
    if random.random() > 0.8:
        with open(attachment_fname, "rb") as f:
            attachments.append({"name": path.basename(attachment_fname), "base64_string": base64.b64encode(f.read()).decode('ascii')})

    email = {
         "sent_from": sender,
         "sent_to": receivers,
         "sent_cc": cc,
         "sent_bcc": [],
         "body": body,
         "subject": subj,
         "attachments": attachments,
         "reply_to_id": "",
         "forward_id": "",
         "headers": []
         }

    requests.post("https://{}:8080/requestSendMail".format(hostname), json=email)
    logging.info("Sent email from {} to {}".format(sender, receivers))


if __name__ == "__main__":
    attachment_file = sys.argv[1]
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', 
                        filename = '/var/log/emailSpooferDaemon.log')
    while True:
        # Check to see if it's daytime
        hour = int(datetime.now().strftime('%H'))
        if hour >= 9 and hour <= 18:
            send_email(attachment_file)
            time_to_sleep = random.randint(2400, 3600)
            logging.info("Sending next email in {} minutes".format(time_to_sleep/60))
        else:
            time_to_sleep = 3600
        time.sleep(time_to_sleep)
