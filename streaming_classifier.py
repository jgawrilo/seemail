import kafka
import json
import argparse
import email_classification as ec
import sqlite3 as sql
import joblib
import networkx as nx

def main(topic, model_file, graph_file, word_file, model_type):

    # Load current network graph
    G = nx.read_pickle(graph_file)

    # Connect to sqlite database with information about emails
    conn = sql.connect("/home/rosteen/Work/seemail/jpl_emails.sqlite")
    cur = conn.cursor()

    # Load file with common words from training data
    with open(args.words, "r") as f:
        word_list = json.load(f)
    # Might be (probably) a list of (word, count) pairs. Take just the words
    if type(word_list[0]) == list:
        word_list = [x[0] for x in word_list]
    for i in range(0, len(word_list)):
        word_indices[word_list[i]] = i

    # Load the trained email classifier model
    M = joblib.load(model_file)

    # This will constantly poll for new items coming off the topic
    consumer = kafka.KafkaConsumer(topic)
    # Featurize each email coming off the queue and make a classification
    for message in consumer:
        print("{}:{}:{}: key={} value=".format(message.topic, message.partition,
                                          message.offset, message.key))
        email_json = json.loads(message.value.decode('utf-8'))

        email_features = ec.featurize_email(email_json, word_indices, cur, G)
        prediction = M.predict(email_features)
        # Where do we want to send the prediction? Just print it out for now
        print("Model prediction: {}".format(prediction))

        # Also need to update the network graph and database

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("topic", type = str, default="email", 
            help="Kafka topic to pull from")
    parser.add_argument("model", type = str, help = "Path to saved sklearn model")
    parser.add_argument("graph", type = str, 
            help = "Path to pickled networkx graph file of email users")
    parser.add_argument("words", type = str, 
            help = "File with most common words from training corpus")
    parser.add_argument("-t", "--model_type", type = str, default = "binary",
            help = "Type of model (binary or specific classification). Default=binary")
    args = parser.parse_args()
    main(args.topic, args.model, args.graph, args.words, args.model_type)
