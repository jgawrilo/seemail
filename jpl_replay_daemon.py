import argparse
import sqlite3 as sql
import json
import smtplib
from datetime import datetime, timedelta()
from time import sleep

def main():
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    # Load credentials for JPL email address duplicates
    with open("/home/user/rosteen/seemail/server_code/jplcr.json") as f:
        creds = json.load(f)

    # Connect to database
    conn1 = sql.connect("/home/user-data/mail/jpl_emails.sqlite")
    cur1 = conn1.cursor()


    start_dt = datetime.now()
    while true:
        end_dt = start_dt + timedelta(seconds = 60)
        # Get the emails to send this minute and send them
        stmt = "select * from "


        # Set the start time to the next minute and sleep for the rest of this minute
        # Should probably make sure email sends didn't take longer than expected 
        # and put us into the next time period
        start_dt = end_dt
        now = datetime.now()
        sleep_time = (end_dt - now).total_seconds()
        sleep(sleep_time)
