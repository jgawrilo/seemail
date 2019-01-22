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

(Replace "yourdomain" with your domain name)

## Install kafka and redis

## Create auxiliary databases

## Clone this repo and run server

