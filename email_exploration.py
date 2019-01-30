import sqlite3 as sql
import json
import re
import csv

def parse_attachments(email_json):
    temp_row = []
    if "attachment" in email_json:
        for attachment in email_json["attachment"]:
            if "extension" in attachment:
                temp_row.append([attachment["filename"], attachment["size"], attachment["extension"]])
            else:
                temp_row.append([attachment["filename"], attachment["size"], "none"])
    return temp_row

def count_jpl_emails(email_json):
   
    n_subsections = len(email_json["body"])
    i = 0
    n_jpl = 0
    email_addresses = []
    while i < n_subsections:
        try:
            email_addresses = email_json["body"][i]["email"]
            break
        except:
            i += 1

    for address in email_addresses:
        # Some addresses are just nasa.gov rather than jpl.nasa.gov, want to catch those
        if re.search("nasa.gov", address) is not None:
            n_jpl += 1
    
    return n_jpl

if __name__ == "__main__":
    conn = sql.connect("/home/user-data/mail/jpl_emails.sqlite")
    cur = conn.cursor()
    filenames = []
    timestamps = []
    res = cur.execute("select * from abuse").fetchall()
    for row in res:
        filenames.append(row[2])
        timestamps.append(row[1])

    jpl_email_histogram = {}
    jpl_forwarders = {}
    jpl_attachments = []

    for fname in filenames:
        with open(fname, "r") as f:
            email_json = json.load(f)
        # Number of emails with a given number of JPL recipients
        n = count_jpl_emails(email_json)
        if n in jpl_email_histogram:
            jpl_email_histogram[n] += 1
        else:
            jpl_email_histogram[n] = 1
        # Number of emails forwarded by each JPL account
        to_email = email_json["header"]["from"]
        if to_email in jpl_forwarders:
            jpl_forwarders[to_email] += 1
        else:
            jpl_forwarders[to_email] = 1
        jpl_attachments += parse_attachments(email_json)

    with open("jpl_count_histogram.csv", "w") as f:
        for key in jpl_email_histogram:
            f.write("{},{}\n".format(key, jpl_email_histogram[key]))

    with open("jpl_forwarders.csv", "w") as f:
        for key in jpl_forwarders:
            f.write("{},{}\n".format(key, jpl_forwarders[key]))

    with open("jpl_timeline.csv", "w") as f:
        for timestamp in sorted(timestamps):
            f.write("{}\n".format(timestamp))

    with open("jpl_attachments.csv", "w") as f:
        fwriter = csv.writer(f)
        fwriter.writerows(jpl_attachments)
