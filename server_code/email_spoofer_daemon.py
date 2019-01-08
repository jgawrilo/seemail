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

def send_email():
    bots_r = redis.StrictRedis(host='localhost', port=6379, db=2)
    active_bots = []
    for b in bots_r.scan_iter():
        active_bots.append(b)
    random.shuffle(active_bots)
    sender = {"email_address": active_bots[0]}
    receiver = {"email_address": active_bots[1]}

    # Decide whether to cc anyone
    

    email = {
         "sent_from": sender,
         "sent_to": [receiver,],
         "sent_cc": [],
         "sent_bcc": [],
         "body": "Hello fellow human! Thought you might enjoy this excellent human content.",
         "subject": "Wow we are so real",
         "attachments": attachments,
         "reply_to_id": "",
         "forward_id": "",
         "headers": []
         }

    swagger_client.request_send_mail_post()
    logging.info("Sent email from {} to {}".format(sender, receiver))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', 
                        filename = '/var/log/emailSpooferDaemon.log'))
    while True:
        # Check to see if it's daytime
        send_email()
        time.sleep(random.randint(1200, 2400))
