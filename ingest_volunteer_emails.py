import json
import sqlite3 as sql
import eml_parser
import email_classification as ec
import numpy as np

vol_data = {
        1: {"inbox": "chris.a.mattmann@jpl.nasa.gov", "file": "ased-historic-volunteer-1_dump.txt"},
        2: {"inbox": "christine.hillsgrove@jpl.nasa.gov", "file": "ased-historic-volunteer-2_dump.txt"},
        3: {"inbox": "Ian.Colwell@jpl.nasa.gov", "file": "ased-historic-volunteer-3_dump.txt"},
        4: {"inbox": "paul.m.ramirez@jpl.nasa.gov", "file": "ased-historic-volunteer-4_dump.txt"},
        5: {"inbox": "wayne.m.burke@jpl.nasa.gov", "file": "ased-historic-volunteer-5_dump.txt"},
        }

vol_dir = "/mnt/f/Work/ASED/"
db_file = "jpl_emails.sqlite"

def load_word_indices(word_file):
    word_indices = {}
    with open(word_file, "r") as f:
        word_list = json.load(f)
        # Might be (probably) a list of (word, count) pairs. Take just the words
        if type(word_list[0]) == list:
            word_list = [x[0] for x in word_list]
        for i in range(0, len(word_list)):
            word_indices[word_list[i]] = i
        print("Loaded word dictionary of {} words".format(len(word_list)))
        return word_indices

def ingest_volunteer_inbox(vol, word_indices):
    inbox = vol_data[vol]["inbox"]
    fname = vol_dir + vol_data[vol]["file"]
    new_features = []
    new_labels = []
    with open(fname, "r") as f:
        for line in f:
            temp = json.loads(line)
            byte_message = bytes.fromhex(temp["message"])
            email_json = eml_parser.eml_parser.decode_email_b(byte_message,
                         include_raw_body=True, include_attachment_data=True)
            print(email_json["header"]["to"])
            if inbox not in email_json["header"]["to"]:
                email_json["header"]["to"] = [inbox,] + email_json["header"]["to"]
                print(email_json["header"]["to"])
            print(type(email_json["header"]["date"]), str(email_json["header"]["date"]))
            if email_json["body"] == []:
                continue
            try:
                features = ec.featurize_email(email_json, word_indices, db_file)
            except:
                print(email_json["body"])
                raise
            if new_features == []:
                new_features = features
            else:
                try:
                    new_features = np.vstack([new_features, features])
                except:
                    continue
            # I'm assuming these are all non-spam emails
            new_labels.append(0)

    np.save("volunteer_{}_features.npy".format(vol), new_features)
    np.save("volunteer_{}_labels.npy".format(vol), np.array(new_labels))
