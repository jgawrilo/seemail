import argparse
import re
import sqlite3 as sql
import json
import smtplib
from datetime import datetime, timedelta
from time import sleep
import requests

# Split a string after a To: or From: to a User object
def parse_to_user(in_str):
    user_dict = {}
    # Are there any cases where there are multiple To recipients listed?
    split_str = in_str.split(" ")
    if len(split_str) > 1:
        user_dict["email_address"] = split_str[-1].replace("<", "").replace(">","")
        # If it looks like we have a first and last name, use them
        if len(split_str) == 3:
            user_dict["first_name"] = split_str[0]
            user_dict["last_name"] = split_str[1]
        # Otherwise put the non-address text into the first name field
        else:
            user_dict["first_name"] = " ".join(split_str[0:-1])
    else:
        user_dict["email_address"] = split_str[0].replace("<", "").replace(">","")

    # Change the email address to the chunkman version
    user_dict["email_address"] = user_dict["email_address"].replace("@","-at-") + "@chunkman.com"

    return user_dict

def send_email(row):
    email_ids = row[0]
    filename  = row[2]
    print("parsing {}".format(filename))
    # Load email json
    with open(filename, 'r') as f:
        email_json = json.load(f)

    #print(email_json)
    n_subsections = len(email_json["body"])
    i = 0
    email_addresses = []
    from_email = ''
    jpl_addresses = []
    while i < n_subsections:
        try:
            email_addresses = email_json["body"][i]["email"]
            print("breaking...")
            break
        except:
            i += 1
    if email_addresses == []:
        i = 0
    print("Using body section {}".format(i))

    for j in range(0, len(email_addresses)):
        # Some addresses are just nasa.gov rather than jpl.nasa.gov, want to catch those
        if re.search("nasa.gov", email_addresses[j]) is not None:
            jpl_addresses.append(email_addresses[j])
        elif re.search("apache", email_addresses[j]) is not None:
            continue
        else:
            if from_email == '' or len(email_addresses[j]) < len(from_email):
                from_email = email_addresses[j]

    content = email_json["body"][i]["content"]

    # See if the "begin forwarded message" string is there, if so split
    if re.search("Begin forwarded message:", content) is not None:
        content = content.split("Begin forwarded message:")[1]

    subject = content.split("Subject: ")[-1].split("\n")[0]
    content_type = email_json["body"][0]["content_type"]
    # Upon further testing, it looks like these two don't always hold up.
    # Might need to use the body:email list, which unfortunately isn't ordered
    from_str = content.split("From: ")[-1].split("\n")[0]
    to_str = content.split("To: ")[-1].split("\n")[0]

    to_email = email_json["header"]["from"] # JPL user that forwarded the email
    to_users = [{"email_address": to_email.replace("@","-at-") + "@chunkman.com"}]
    from_user = {"email_address": from_email.replace("@","-at-") + "@chunkman.com"}
    #to_users = parse_to_user(to_str)
    #from_user = parse_to_user(from_str)

    body = "\n".join(content.split("Subject: ")[-1].split("\n")[1:])

    print("Subject: {}".format(subject))
    print("From: {}".format(from_user))
    print("To: {}".format(to_users))
    print("Content Type: {}".format(content_type))
    print("Body: {}".format(body))

    # Stop here temporarily for testing
    return from_user["email_address"], to_users[0]["email_address"]

    attachments = []

    # Parse the email content to build the email object
    email = {
         "sent_from": from_user,
         "sent_to": to_users,
         "sent_cc": [],
         "sent_bcc": [],
         "body": "",
         "subject": "",
         "attachments": attachments,
         "reply_to_id": "",
         "forward_id": "",
         "headers": []
         }

    print(json.dumps(email, indent=2))

    # Send the email via the swagger API
    res = requests.post("https://box.chunkman.com:8080/requestSendMail", json=email)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    # Load credentials for JPL email address duplicates
    with open("/home/rosteen/seemail/jplcr.json") as f:
        creds = json.load(f)

    # Connect to database
    conn1 = sql.connect("/home/user-data/mail/jpl_emails.sqlite")
    cur1 = conn1.cursor()

    #start_dt = (datetime.now() - datetime(1970,1,1)).total_seconds()
    # For testing, fake starting at Feb 1
    #start_dt = 1549022400
    start_dt = 1549030200
    while True:
        end_dt = start_dt + 60
        # Get the emails to send this minute and send them
        stmt = "select * from abuse where replay_timestamp > {} and replay_timestamp <= {}".format(start_dt, end_dt)
        print(stmt)
        cur1.execute(stmt)
        res = cur1.fetchall()

        # Send the emails
        with open('replay_test.txt', 'a') as f:
            for row in res:
                from_email, to_emails = send_email(row)
                f.write("{}, {}\n".format(from_email, to_emails))

        # Set the start time to the next minute and sleep for the rest of this minute
        # Should probably make sure email sends didn't take longer than expected
        # and put us into the next time period
        start_dt = end_dt
        now = (datetime.now() - datetime(1970,1,1)).total_seconds()
        sleep_time = end_dt - now
        #sleep(sleep_time)
        # Shorter time for testing
        sleep(2)
