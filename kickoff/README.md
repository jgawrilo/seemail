# ASED Kickoff IMAP prototype

## THIS IS VERY POC AND NOT TO BE USED IN PROD

## Install

1. Install and run redis (https://redis.io/download)
2. Install and run Kafka (https://kafka.apache.org/quickstart)
3. Create a kafka topic called 'email' (`bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic email`)
3. `pip install flask redis imbox kafka-python`

## Run

This serves the html content and hosts the 'add' service.
`python server.py` 

and 

This checks redis for new accounts every second, sending new messages to the 'email topic'

`python poll_and_send.py`
