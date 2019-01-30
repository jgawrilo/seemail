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

def run_svm():
    pass

def run_naive_bayes():
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", type = str, default = "SVM",
                        help = "Model to use for classification")
    
    args = parser.parse_args()

    function_key = {"SVM": run_svm,
                    "NB": run_naive_bayes}

