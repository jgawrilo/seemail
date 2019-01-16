import sys
sys.path.append('/home/rosteen/seemail/client_stub/')
import swagger_client
import time
import logging
import json
import requests
import redis
import random
import sqlite3 as sql
from datetime import datetime
from nltk.corpus import gutenberg

def clean_sentences(sentences):
  return sentences.replace(" ,", "").replace(" ' ", "'").replace(" .", ".").replace(" ?", "?").replace(" :", ":")

def send_email():
    bots_r = redis.StrictRedis(host='localhost', port=6379, db=2)
    active_bots = []
    for b in bots_r.scan_iter():
        active_bots.append(b.decode('utf-8'))
    random.shuffle(active_bots)

    # Get first and last names
    names = {}
    conn = sql.connect('/home/user-data/mail/user_names.sqlite')
    cur = conn.cursor()
    cur.execute("select * from names")
    rows = cur.fetchall()
    print(rows)
    for row in rows:
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
        with open('Sombrero_PROMPT.png', "rb") as f:
            attachments.append({"name": 'Sombrero_PROMPT.png', "base64_string": base64.b64encode(f.read()).decode('ascii')})

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

    conf = swagger_client.configuration.Configuration()
    conf.host = "https://box.chunkman.com:8080"
    api_instance = swagger_client.DefaultApi(swagger_client.ApiClient(conf))
    res = api_instance.request_send_mail_post(email)
    logging.info("Sent email from {} to {}".format(sender, receivers))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', 
                        filename = '/var/log/emailSpooferDaemon.log')
    while True:
        # Check to see if it's daytime
        hour = int(datetime.now().strftime('%H'))
        if hour >= 9 and hour <= 18:
            send_email()
            time_to_sleep = random.randint(2400, 3600)
            logging.info("Sending next email in {} minutes".format(time_to_sleep/60))
        else:
            time_to_sleep = 3600
        time.sleep(time_to_sleep)
