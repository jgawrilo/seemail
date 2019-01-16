import json
import argparse
from glob import glob
from datetime import datetime, timedelta
import sqlite3 as sql
import re

def parse_email(fname):
    with open(fname, 'r') as f:
        email_json = json.load(f)

    # Parse out from and to addresses for the original email
    # Look in body section 0 1 or 2 for "email" keyword, then take the first one that
    # isn't the JPL address
    email_addresses = []
    #jpl_email = email_json["header"]["from"] # "from" because we're seeing the forward
    for section in email_json["body"]:
        if "email" not in section:
            continue
        for address in section["email"]:
            if re.search("_", address) is not None:
                print("Email address {} has an underscore in it".format(address))
            email_addresses.append(address)

    # Record datetime of email send. Unfortunately it appears that we only have the
    # datetime of the forward, not the original email. DT originally in local time with
    # difference from UTC appended.
    email_tz = int(email_json["header"]["date"][-6:-3])
    email_dt = email_json["header"]["date"][0:-6]
    email_dt = datetime.strptime(email_dt, "%Y-%m-%dT%H:%M:%S")
    email_dt = email_dt - timedelta(hours=email_tz)
    timestamp = (email_dt - datetime(1970,1,1)).total_seconds()

    return email_addresses, timestamp

def main(user_file):
    # Get all email filenames
    if args.folder:
        all_files = glob("{}/*/*.json".format(args.folder))

    conn = sql.connect("/home/user-data/mail/jpl_emails.sqlite")
    cur = conn.cursor()

    # Read email json data
    for email_file in all_files:
        print("Processing {}".format(email_file))
        addresses, utc_timestamp = parse_email(email_file)
        address_ids = []

        for address in addresses:
            
            try:
                stmt = "insert into email_addresses (address) values ('{}')".format(address.replace("'", ""))
                cur.execute(stmt)
            except sql.OperationalError:
                print(stmt)
                raise
            except sql.IntegrityError:
                pass

            stmt = "select rowid from email_addresses where address = '{}'".format(address.replace("'", ""))
            address_ids.append(cur.execute(stmt).fetchone()[0])

        try:
            stmt = '''insert into abuse (address_ids, timestamp, filename) values 
                ('{}', {}, '{}')'''.format(address_ids, utc_timestamp, email_file)
            cur.execute(stmt)
            conn.commit()
        except sql.OperationalError:
            raise
        except sql.IntegrityError:
            pass

    cur.close()
    conn.close()

#########################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--ldap_file", type=str, help="File with JPL user information")
    parser.add_argument("-f", "--folder", type=str, help="Folder with json email type subdirectories")
    args = parser.parse_args()
    main(args)
