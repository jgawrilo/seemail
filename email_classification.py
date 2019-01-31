###############################################################################
# Run some simple classification models on the JPL Abuse dataset to get an 
# initial look at what baseline performance is. 
#
# Some code shamelessly based off of 
# https://www.kdnuggets.com/2017/03/email-spam-filtering-an-implementation-with-python-and-scikit-learn.html
###############################################################################

import json
import argparse
import re
import os
import numpy as np
from collections import Counter
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.svm import SVC, NuSVC, LinearSVC

def featurize_email(email_json, word_list):
    n_subsections = len(email_json["body"])
    jpl_addresses = []
    outside_addresses = []
    while i < n_subsections:
        try:
            email_addresses = email_json["body"][i]["email"]
        except:
            i += 1
    if email_addresses == []:
        print("No email addresses found")
    # Divide email addresses into JPL and non-JPL
    for address in email_addresses:
        if re.search("nasa.gov", address) is not None:
            jpl_addresses.append(address)
        # I don't think we want to count intermediate apache routing things
        elif re.search("apache", address) is not None:
            outside_addresses.append(address)
    n_jpl = len(jpl_addresses)
    n_outside = len(outside_addresses)

    content = email_json["body"][i]["content"]
    subject = content.split("Subject: ")[-1].split("\n")[0]
    subj_chars = len(subject)
    subj_words = len(subject.split(" "))

    content_type = email_json["body"][0]["content_type"]

    # See if there are links
    n_links = 0
    for item in email_json["body"]:
        if "uri" in item:
            n_links += len(item["uri"])

    if "attachments" in email_json:
        n_attachments = len(email_json["attachments"])
    else:
        n_attachments = 0

    # Make a one-hot variable for attachment extensions? Need to find out what the set of extensions is.
    extensions = ['jpg', 'png', 'p7m', 'none', 'txt', 'htm', 'pdf', 'docx', 
                  'ics', 'gif', 'bmp', 'pptx', 'doc', 'zip', 'xls', 'xlsx', 
                  'html', 'aspx', 'xml', 'jar', 'rar', 'tiff', '05', 'jpeg', 
                  'ace', 'wav', 'm4a', 'vcf', '3gp', 'avi']
    extension_indices = {}
    # Build index reference dictionary
    for i in range(0, len(extensions)):
        extension_indices[extensions[i]] = i
    # Might make this a numpy array...
    att_extensions = [0] * len(extensions)
    att_sizes = []
    if len(n_attachments) > 0:
        for attachment in email_json["attachments"]:
            if "extension" not in attachment:
                att_extensions[extension_indices["none"]] += 1
            else:
                att_extensions[extension_indices[attachment["extension"]]] += 1

    return att_extensions + [n_extensions, n_jpl, n_outside, subj_chars, subj_words, n_links]

# I'll probably end up being able to consolidate a lot of the training/testing code
# but for now I'm keeping the models separate in case there are differences

def run_svm(train_matrix, train_labels):
    model = LInearSVC()
    model.fit(train_matrix, train_labels)
    return model

def run_naive_bayes(train_matrix, train_labels):
    model = MultinomialNB()
    model.fit(train_matrix, train_labels)
    return model

def run_knn():
    pass

def run_random_forest():
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", type = str, default = "SVM",
                        help = "Model to use for classification")
    parser.add_argument("-w", "--ords", type = str, help = "Word dictionary (well, list) json file")
    args = parser.parse_args()

    function_key = {"SVM": run_svm,
                    "NB": run_naive_bayes,
                    "KNN": run_knn,
                    "RF": run_random_forest}

    # Note: I'm putting the Credential Phishing and Phishing Training emails both under Phishing
    type_labels = {"Not Spam": 0,
                   "Malware": 1,
                   "Phishing": 2,
                   "Propaganda": 3,
                   "Recon": 4,
                   "Social Engineering": 5,
                   "Spam": 6}

    # Get filenames from database
    conn = sql.connect("/home/user-data/mail/jpl_emails.sqlite")
    cur = conn.cursor()
    filenames = []
    res = cur.execute("select * from abuse").fetchall()
    for row in res:
        filenames.append(row[2])

    # Load list of words for word frequency features
    if args.words:
        with open(args.words, "r") as f:
            word_list = json.load(f)
        # Might be (probably) a list of (word, count) pairs. Take just the words
        if type(word_list[0]) == list:
            word_list = [x[0] for x in word_list]
        print("Loaded word dictionary of {} words".format(len(word_list)))

    # Parse all the emails to create training/test matrices and labels
    for fname in filenames:
        str_label = fname.split("/")[-2]
        if str_label == "Unknown":
            continue
        elif re.search("Phishing", input_label) is not None:
            input_label = "Phishing"
        with open(fname, "r") as f:
            email_json = json.load(f)
        features = featurize_email(email_json, word_list)
        int_label = type_labels[str_label] 

    # Train the chosen model
    model = function_key[args.model](train_matrix, train_labels)

    # Run test on the trained model to check performance
    res = model.predict(test_matrix)

