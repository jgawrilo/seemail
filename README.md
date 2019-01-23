# seemail

## Mailinabox setup

Box set up with `curl -s https://mailinabox.email/setup.sh | sudo bash`

More details for Mailinabox setup can be found [here](https://mailinabox.email/guide.html)

### View all mail

```
   11 adduser --system --home /var/archive/mail/ --no-create-home --disabled-password mailarchive
   12  mkdir /var/archive
   13  mkdir /var/archive/mail
   14  adduser --system --home /var/archive/mail/ --no-create-home --disabled-password mailarchive
   15  mkdir -p /var/archive/mail/tmp
   16  mkdir -p /var/archive/mail/cur
   17  mkdir -p /var/archive/mail/new
   18  chown -R nobody:nogroup /var/archive
   19  postconf -e always_bcc=mailarchive@localhost
   20  echo "mailarchive: /var/archive/mail/" >> /etc/aliases
   21  newaliases
   22  /etc/init.d/postfix restart
```

all mail shows up in /var/archive/mail/new

### Web access

Mailinabox web mail access can be accessed at https://box.yourdomain.com/mail/

The Mailinabox admin control panel can be accessed at https://box.yourdomain.com/admin

(This assumes that you have followed the mailinabox recommendation for your machine's hostname)

## Install kafka and redis

The seemail code pipes incoming/outgoing emails into a kafka topic, and uses redis for keeping track of active/inactive bot accounts. Refer to the [kafka](https://kafka.apache.org/quickstart) and [redis](https://kafka.apache.org/quickstart) quickstart instructions.

## Install seemail code and Swagger API

Clone this repo by using `git clone https://github.com/jgawrilo/seemail.git` and make sure required python packages are installed with `pip3 install -r requirements.txt`.

From the [API site](https://app.swaggerhub.com/apis/jataware/seemail/1.0) use the export button in the top right to export the Server Stub (as python-flask). Unzip the resulting python-flask-server-generated.zip file to a location on your machine - I created a server\_stub directory in the seemail directory to use. Change directory to the unzipped folder and make sure the requirements are installed with `pip3 install -r requirements.txt`.

Copy the seemail/server\_code/default\_controller.py file to server\_stub/swagger\_server/controllers/, overwriting the default\_controller.py file that is already there.

## Start background processes

We recommended running each of the following commands in their own Screen (or similar tool) sessions. Commands as written assume the user is in the top level seemail directory.

`python3 server_code/watch.py`

`cd server_stub; python3 -m swagger_server`

Note that the server uses the Mailinabox management packages for some actions, so it needs to be run as a user with permissions to access the Mailinabox directories.

### Set up bot email daemon (optional)

To generate email traffic on the machine (and thus output to the kafka topic), there is a daemon that can be run to have bot email accounts send emails (dummy text and occasionally an attachment) back and forth. This requires creating a few bot email accounts via the createBotAccount API method - for an example of how to use this, see email\_api\_examples.py. 

In addition to the packages in requirements.txt, the bot email daemon requires nltk and the gutenberg corpus. These can be installed/downloaded with `pip3 install nltk; python3 -c 'import nltk; nltk.download('gutenberg')'`.

Once that is done, the daemon can be run (in a Screen session or similar, preferably) simply with `python3 email_spoofer_daemon.py [attachment file]`. The daemon is set up to send an email every 40-60 minutes between 9AM and 6PM.

## Examples

The examples directory has scripts to demonstrate two ways to interact with the server. Examples of calling each of the API methods are found in email\_api\_examples.py. An example of creating a consumer to ingest and display emails coming off of the email kafka topic is found in kafka\_consumer.py. The kafka example script can also take kafka topic name as an optional parameter to subscribe to a topic other than the default "email" (for example, "history").
