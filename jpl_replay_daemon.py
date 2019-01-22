import argparse
import sqlite3 as sql
import json
import smtplib
from datetime import datetime, timedelta()
from time import sleep
import requests

def send_email(row, s):
    email_ids = row[0]
    filename  = row[2]
    # Load email json
    with open(filename, 'r') as f:
        email_json = json.load(f)
        content = email_json["body"]["content"]
        subject = content.split("Subject: ")[-1].split("\n")[0]
        print("Subject: {}".format(subject))
        from_str = content.split("From: ")[-1].split("\n")[0]
        to_str = content.split("To: ")[-1].split("\n")[0]
        body = ""

    # Get chunkman email addresses that correspond to the JPL email addresses

    attachments = []

    # Parse the email content to build the email object
    email = {
         "sent_from": from_address,
         "sent_to": [],
         "sent_cc": [],
         "sent_bcc": [],
         "body": "",
         "subject": "",
         "attachments": attachments,
         "reply_to_id": "",
         "forward_id": "",
         "headers": []
         }
    
    # Send the email via the swagger API
    res = requests.post("https://box.chunkman.com:8080/requestSendMail", json=email)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    # Load credentials for JPL email address duplicates
    with open("/home/user/rosteen/seemail/server_code/jplcr.json") as f:
        creds = json.load(f)

    # Connect to database
    conn1 = sql.connect("/home/user-data/mail/jpl_emails.sqlite")
    cur1 = conn1.cursor()

    # Connect to the smtp server
    s = smtplib.SMTP("localhost:587")

    start_dt = datetime.now()
    while true:
        end_dt = start_dt + timedelta(seconds = 60)
        # Get the emails to send this minute and send them
        stmt = "select * from abuse where replay_timestamp > {} and replay_timestamp <= {}".format(start_dt, end_dt)
        cur1.execute(stmt)
        res = cur1.fetchall()

        # Send the emails
        for row in res:
            send_email(row)

        # Set the start time to the next minute and sleep for the rest of this minute
        # Should probably make sure email sends didn't take longer than expected 
        # and put us into the next time period
        start_dt = end_dt
        now = datetime.now()
        sleep_time = (end_dt - now).total_seconds()
        sleep(sleep_time)
