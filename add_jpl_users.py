import json
import argparse
from glob import glob
from datetime import datetime, timedelta
import sqlite3 as sql

def parse_email(fname):
    with open(fname, 'r') as f:
        email_json = json.load(f)

    # Parse out from and to addresses for the original email
    # Look in body section 0 1 or 2 for "email" keyword, then take the first one that
    # isn't the JPL address
    jpl_email = email_json["header"]["from"] # "from" because we're seeing the forward
    for i in email_json["body"]:
        if "email" not in email_json["body"][i]:
            continue
        for j in email_json["body"][i]["email"]:
            attacker_email = email_json["body"][i]["email"][j]
            if attacker_email != jpl_email:
                break

    # Strip out things we don't want from the email addresses
    attacker_email = attacker_email.replace("smtp.mailfrom=", "")

    print("From: {}, To: {}".format(attacker_email, jpl_email))

    # Record datetime of email send. Unfortunately it appears that we only have the
    # datetime of the forward, not the original email. DT originally in local time with
    # difference from UTC appended.
    email_tz = int(email_json["header"]["to"]["date"][-6:-3])
    email_dt = "-".join(email_json["header"]["to"]["date"].split("-")[0:-1])
    email_dt = datetime.strptime(email_json["header"]["to"]["date"], "%Y-%m-%dT%H%M%%S")
    email_dt = email_dt - timedelta(hours=email_tz)
    timestamp = email_dt - datetime(1970,1,1)).total_seconds()

    return jpl_email, attacker_email, timestamp

def main(user_file):
    # Get all email filenames
    with open(args) as f:
        if args.folder:
            all_files = glob("{}/*/*.json".format(args.folder))

    conn = sql.connect("/home/user-data/mail/jpl_emails.sqlite")
    cur = conn.cursor()

    # Read email json data
    for email_file in all_files:
        jpl, attacker, utc_timestamp = parse_email(email_file)
        # Add the information I want to track to the database
	stmt = "insert into jpl_addresses (address) values ({})".format(jpl)
        cur.execute(stmt)

        stmt = "insert into attacker_addresses (address) values ({})".format(attacker)
        cur.execute(stmt)

        stmt = "select id from jpl_addresses where address = {}".format(jpl)
        jpl_id = cur.execute(stmt).fetchone()[0]
        print(jpl_id)

        stmt = "select id from attacker_addresses where address = {}".format(attacker)
        attacker_id = cur.execute(stmt).fetchone()[0]
        print(attacker_id)

        stmt = '''insert into abuse_emails (jpl_email_id, attacker_email_id, timestamp, 
               filename) values ({}, {}, {}, {})'''.format(jpl_id, attacker_id, email_dt, utc_timestamp)
        cur.execute(stmt)
        conn.commit()

    cur.close()
    conn.close()

#########################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--ldap_file", type=str, help="File with JPL user information")
    parser.add_argument("-f", "--folder", type=str, help="Folder with json email type subdirectories")
    args = parser.parse_args()
    main(args)
