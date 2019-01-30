###############################################################################
# Run some simple classification models on the JPL Abuse dataset to get an 
# initial look at what baseline performance is. 
###############################################################################

import json
import argparse
import os
import numpy as np
from collections import Counter
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.svm import SVC, NuSVC, LinearSVC

def featurize_email(email_json):
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

    if "attachments" in email_json:
        n_attachments = len(email_json["attachments"])
    else:
        n_attachments = 0

    # Make a one-hot variable for attachment extensions? Need to find out what the set of extensions is.

def run_svm():
    pass

def run_naive_bayes():
    pass

def run_knn():
    pass

def run_random_forest():
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", type = str, default = "SVM",
                        help = "Model to use for classification")
    
    args = parser.parse_args()

    function_key = {"SVM": run_svm,
                    "NB": run_naive_bayes}

    res = function_key[args.model]()
