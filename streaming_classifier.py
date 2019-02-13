import kafka
import json
import argparse
import email_classification as ec
import sqlite3 as sql
import networkx as nx

def main(topic, graph_file):

    # Load current network graph and connect to sqlite database
    G = nx.read_pickle("")

    # This will constantly poll for new items coming off the topic
    consumer = kafka.KafkaConsumer(topic)
    # Featurize each email coming off the queue and make a classification
    for message in consumer:
        print("{}:{}:{}: key={} value=".format(message.topic, message.partition,
                                          message.offset, message.key))
        email_json = json.loads(message.value.decode('utf-8'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("topic", type=str, default="email", help="Kafka topic to pull from")
    parser.add_argument("-g", "--graph_file", type = str, 
            help = "Path to pickled networkx graph file of email users")
    args = parser.parse_args()
    main(args.topic)
