import sqlite3 as sql
from datetime import datetime, timedelta
import argparse

def main(start_dt, end_dt):

    start = datetime.strptime(start_dt, "%Y-%m-%dT%H:%M:%S")
    end = datetime.strptime(end_dt, "%Y-%m-%dT%H:%M:%S")

    start_ts = (start - datetime(1970,1,1)).total_seconds()
    end_ts = (end - datetime(1970,1,1)).total_seconds()

    # Connect to the db and get the historical start and end times
    conn = sql.connect("/home/user-data/mail/jpl_emails.sqlite")
    cur = conn.cursor()

    stmt = "select max(timestamp), min(timestamp) from abuse"
    max_orig, min_orig = cur.execute(stmt).fetchone()
    orig_diff = max_orig - min_orig
    new_diff = end_ts - start_ts
    fraction = new_diff / orig_diff
    offset = start_ts - min_orig

    # Add column to abuse table for new times if it isn't already there
    stmt = "alter table abuse add column replay_timestamp int"
    try:
        cur.execute(stmt)
    except sql.IntegrityError:
        pass
    except:
        raise
    
    # Calculate the new timestamp for the compressed timeline
    stmt = "update abuse set replay_timestamp = (timestamp - {})*{} + {}".format(min_orig, fraction, start_ts)
    cur.execute(stmt)

    conn.commit()
    cur.close()
    conn.close()

###############################################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("start_date", type = str, 
        help = "Datetime to start sending email playback, format %Y-%m-%dT%H:%M:%S")
    parser.add_argument("end_date", type = str, 
        help = "Last datetime for email playback, format %Y-%m-%dT%H:%M:%S")
    args = parser.parse_args()

    main(args.start_date, args.end_date)
