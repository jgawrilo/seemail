import sys
sys.path.append('/home/rosteen/seemail/client_stub/')
import swagger_client
import time
import logging
import json
import requests
import redis
import random
from datetime import datetime
from nltk.corpus import gutenberg

def clean_sentences(sentences):
  return sentences.replace(" ,", "").replace(" ' ", "'").replace(" .", "").replace(" ?", "?").replace(" :", ":")

def send_email():
    bots_r = redis.StrictRedis(host='localhost', port=6379, db=2)
    active_bots = []
    for b in bots_r.scan_iter():
        active_bots.append(b.decode('utf-8'))
    random.shuffle(active_bots)
    print(active_bots)
    sender = {"email_address": active_bots[0]}
    receivers = [{"email_address": active_bots[1]},]

    all_sents = gutenberg.sents('milton-paradise.txt')
    start = random.randint(0, len(all_sents)-10)
    subj = clean_sentences(" ".join(all_sents[start]))
    body = ''
    for i in range(start+1, random.randint(3,10)):
        body += " ".join(all_sents[i])
    body = clean_sentences(body)

    # Decide whether to cc anyone
    if random.random() < 0.8:
        cc = []
    else:
        cc = [{"email_address": active_bots[2]},]

    attachments = []

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
        send_email()
        time_to_sleep = random.randint(1200,2400)
        logging.info("Sending next email in {} minutes".format(time_to_sleep/60))
        time.sleep(time_to_sleep)
