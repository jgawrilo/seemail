import kafka
import json
import argparse

def main(topic):
    # This will constantly poll for new items coming off the topic from the remote machine
    consumer = kafka.KafkaConsumer(topic, bootstrap_servers="box.chunkman.com:9092")
    for message in consumer:
        print("{}:{}:{}: key={} value=".format(message.topic, message.partition,
                                          message.offset, message.key))
        print(json.dumps(json.loads(message.value.decode('utf-8')), indent = 4))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("topic", type=str, default="email", help="Kafka topic to pull from")
    args = parser.parse_args()
    main(args.topic)
