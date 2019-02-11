#
#  Functions for tracking email interactions via a network graph
#  Graph saved/loaded with pickle
#

import argparse
import networkx as nx
import sqlite3 as sql
import json
from sortedcontainers import SortedList

def email_address_index(cur, email_address):
    stmt = "select rowid from email_addresses where address = '{}'".format(email_address)
    res = cur.execute(stmt).fetchall()
    if len(res) == 0:
        stmt = "insert into email_addresses values ({})".format(email_address)
        cur.execute(stmt)
        stmt = "select rowid from email_addresses where address = '{}'".format(email_address)
        res = cur.execute(stmt).fetchall()

    return res[0][0]

def process_edge(G, from_ind, to_ind, ts):
    if not G.has_edge(from_ind, to_ind)
            G.add_edge(from_ind, to_ind)
            G[from_ind][to_ind]["timestamps"] = sortedlist([ts])
        else:
            G[from_ind][to_ind]["timestamps"].add(ts)
    return G

def initialize_graph():
    conn = sql.connect("/home/user-data/mail/jpl_emails.sqlite")
    cur = conn.cursor()
    filenames = []
    timestamps = []
    res = cur.execute("select * from abuse").fetchall()
    for row in res:
        filenames.append(row[2])
        timestamps.append(row[1])
    G = nx.DiGraph()
    
    for i in range(0, len(filenames)):
        with open(filenames[i], "r") as f:
            email_json = json.load(f)
        # NOTE - this will work when we get original emails, for the
        # current set of forwards getting to/from requires more work.
        # Also need to handle cc/bcc
        to_inds = email_address_index(cur, email_json["header"]["to"])
        from_ind = email_address_index(cur, email_json["header"]["from"])
        # Check to see if there is already a from->to edge in the graph
        # and either add one or add the timestamp to existing edge
        for to_ind in to_inds:
            G = process_edge(G, from_ind, to_ind, timestamps[i])

    return G

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", action = "store_true",
            help = "Flag to create a new graph rather than adding to one")
    parser.add_argument("-g", "--graph", type = str,
            help = "File with existing graph structure")
    args = parser.parse_args()

    # Load previously generated graph or create new one
    if args.create:
        G = initialize_graph()
        nx.write_pickle(G, args.graph)
    else:
        G = nx.read_gpickle(args.graph)
