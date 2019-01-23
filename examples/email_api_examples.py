import requests
import json
import base64

domain = 'chunkman.com'
base_url = "https://box.{}:8080".format(domain)

# Get list of all email users (excluding bots)

res = requests.get(base_url + "/getAllUsers")
user_list = json.loads(res.text)
print("getAllUsers: {}".format(res))
print(user_list)

# Add list of email addresses to list of monitored (emails sent to kafka) accounts

params = {"email_addresses": ["ricky@{}".format(domain), "justin@{}".format(domain)]}
res = requests.get(base_url + "/monitorUsers", params = params)
print("monitorUsers: {}".format(res))
print(res.text)

# Remove list of email addresses from list of monitored accounts

params = {"email_addresses": ["ricky@{}".format(domain), "justin@{}".format(domain)]}
res = requests.get(base_url + "/unmonitorUsers", params = params)
print("unmonitorUsers: {}".format(res))
print(res.text)

# Create a bot account

data = {"email_address": "lewis.haynes@{}".format(domain), "first_name": "Lewis", "last_name": "Haynes"}
res = requests.post(base_url + "/createBotAccount", json = data)
print("createBotAccount: {}".format(res))
print(res.text)

# Remove a bot account from list of active bots (emails will remain in archive)

params = {"email_addresses": ["charlie.jones@{}".format(domain)]}
res = requests.get(base_url + "/removeBotAccount", params = params)
print("removeBotAccount: {}".format(res))
print(res.text)

# Request mail history for a list of email addresses. Will be sent to "history" kafka topic

params = {"email_addresses": ["charlie.jones@{}".format(domain), "lewis.haynes@{}".format(domain)],
        "request_key": "test1", "back_to_iso_date_string": "2019-01-01"}
res = requests.get(base_url + "/requestMailHistory", params = params)
print("requestMailHistory: {}".format(res))
print(res.text)


# Send an email on behalf of a user

charlie = {"email_address": "charlie.jones@".format(domain), "first_name": "Charlie", "last_name": "Jones"}
lewis = {"email_address": "lewis.haynes@".format(domain), "first_name": "Lewis", "last_name": "Haynes"}
attachments = []
for fname in ('Sombrero_PROMPT.png',):
    with open(fname, "rb") as f:
        attachments.append({"name": fname, "base64_string": base64.b64encode(f.read()).decode('ascii')})
email = {
        "sent_from": charlie,
        "sent_to": [lewis,],
        "sent_cc": [],
        "sent_bcc": [],
        "body": "Hello fellow human! Thought you might enjoy this excellent human content.",
        "subject": "Wow we are so real",
        "attachments": attachments,
        "reply_to_id": "",
        "forward_id": "",
        "headers": []
        }

res = requests.post(base_url + "/requestSendMail", json = email)
print("requestSendMail: {}".format(res))
print(res.text)
