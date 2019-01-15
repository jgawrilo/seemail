import json
import argparse
from glob import glob

def parse_email(fname):
    with open(fname, 'r') as f:
        email_json = json.load(f)

    # Parse out from and to addresses for the original email
    jpl_email = email_json["header"]["from"] # "from" because we're seeing the forward
    for i in [0,1,2]:
        j = 0
        while True:
            try:
                attacker_email = email_json["body"]["{}".format(i)]["email"]["{}".format(j)]
            except:
                continue
            if attacker_email != jpl_email:
                break
            j += 1

    print("From: {}, To: {}".format(attacker_email, jpl_email))

    # Record datetime of email send. Unfortunately it appears that we only have the
    # datetime of the forward, not the original email.


def main(user_file):
    # Get all email filenames
    with open(args) as f:
        if args.folder:
            all_files = glob("{}/*/*.json".format(args.folder))

    # Read email json data
    for email_file in all_files:
        parse_email(email_file)


#########################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--ldap_file", type=str, help="File with JPL user information")
    parser.add_argument("-f", "--folder", type=str, help="Folder with json email type subdirectories")
    args = parser.parse_args()
    main(args)
