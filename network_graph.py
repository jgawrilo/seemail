#
#  Functions for tracking email interactions via a network graph
#  Graph saved/loaded with pickle
#

import argparse
import networkx as nx
import sqlite3 as sql
import json
from sortedcontainers import SortedList
import sys
from email_exploration import parse_from_to

# Get the rowid for the email address, adding it to the database if needed
def email_address_index(cur, conn, email_address):
    email_address = email_address.replace("'", "")
    stmt = "select rowid from email_addresses where address = '{}'".format(email_address)
    res = cur.execute(stmt).fetchall()
    if len(res) == 0:
        stmt = "insert into email_addresses values ('{}')".format(email_address)
        try:
            cur.execute(stmt)
            conn.commit()
        except:
            print(stmt)
            raise
        stmt = "select rowid from email_addresses where address = '{}'".format(email_address)
        res = cur.execute(stmt).fetchall()

    return res[0][0]

# Check if from->to is already an edge and either add it if not,
# or add timestamp to existing edge
def process_edge(G, from_ind, to_ind, ts):
    if not G.has_edge(from_ind, to_ind):
        G.add_edge(from_ind, to_ind)
        G[from_ind][to_ind]["timestamps"] = SortedList([ts])
    else:
        G[from_ind][to_ind]["timestamps"].add(ts)
    return G

# Add information to graph from either email file or json data
def process_email(G, cur, filename = None, email_json = None, timestamp = None,
                    fwd = False):
    if filename is not None and email_json is None:
        with open(filename, "r") as f:
            email_json = json.load(f)
    elif email_json is not None and filename is None:
        pass
    else:
        print("Error: Either email filename OR email json must be provided")
        sys.exit(1)

    # Parse email addresses out of forwarded emails
    if fwd:
        from_address, to_addresses = parse_from_to(email_json["body"])
        # Return without further ado if we couldn't parse a from address
        if from_address is None:
            return G
        from_ind = email_address_index(cur, from_address)
        # If we couldn't parse out recipients, we at least know who at JPL
        # forwarded the email
        if to_addresses is None or len(to_addresses) == 0:
            to_addresses = [email_json["header"]["from"]]
        # Update the graph with the edges
        for to_address in to_addresses:
            to_ind = email_address_index(cur, to_address)
            G = process_edge(G, from_ind, to_ind, timestamp)
    # Or get them more easily if we have the original email parsed to json
    else:
        # Also need to see if cc/bcc show up in to list or separate headers
        from_ind = email_address_index(cur, email_json["header"]["from"])
        # Check to see if there is already a from->to edge in the graph
        # and either add one or add the timestamp to existing edge
        for to_address in email_json["header"]["to"]:
            to_ind = email_address_index(cur, to_address)
            G = process_edge(G, from_ind, to_ind, timestamp)

    return G

# Create a new graph from a set of email files
def initialize_graph(fwd = False):
    conn = sql.connect("/home/rosteen/Work/seemail/jpl_emails.sqlite")
    cur = conn.cursor()
    filenames = []
    timestamps = []
    res = cur.execute("select * from abuse").fetchall()
    for row in res:
        filenames.append(row[2])
        timestamps.append(row[1])
    G = nx.DiGraph()

    for i in range(0, len(filenames)):
        #print(filenames[i])
        G = process_email(G, cur, filename = filenames[i],
                timestamp = timestamps[i], fwd = fwd)

    return G

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", action = "store_true",
            help = "Flag to create a new graph rather than adding to one")
    parser.add_argument("-g", "--graph", type = str,
            help = "File with existing graph structure")
    parser.add_argument("-f", "--forwards", action = "store_true",
            help = "Flag to deal with forwarded emails rather than originals")
    args = parser.parse_args()

    # Load previously generated graph or create new one
    if args.create:
        G = initialize_graph(args.forwards)
        nx.write_gpickle(G, args.graph)
    else:
        G = nx.read_gpickle(args.graph)

