#
#  Functions for tracking email interactions via a network graph
#  Graph saved/loaded with pickle
#

import argparse
import networkx as nx
import sqlite3 as sql
import json

def email_address_index(cur, email_address):
    stmt = "select rowid from email_addresses where address = '{}'".format(email_address)
    res = cur.execute(stmt).fetchall()
    if len(res) == 0:
        stmt = "insert into email_addresses values ({})".format(email_address)

    return ind

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
        to_ind = email_address_index(cur, email_json["header"]["to"])
        from_ind = email_address_index(cur, email_json["header"]["from"])

    return G

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--graph", type = str,
            help = "File with existing graph structure")
    args = parser.parse_args()

    # Load previously generated graph or create new one
    if args.graph:
        G = nx.read_gpickle(args.graph)
    else:
        G = initialize_graph()
