import connexion
import six
import redis

from swagger_server.models.email import Email  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server import util

users_r = redis.StrictRedis(host='localhost', port=6379, db=1)
bots_r = redis.StrictRedis(host='localhost', port=6379, db=2)

def create_bot_account_post(user):  # noqa: E501
    """Create a bot email account to send/receive messages from.

     # noqa: E501

    :param user: The bot user to send/receive messages from.
    :type user: dict | bytes

    :rtype: bool
    """
    if connexion.request.is_json:
        user = User.from_dict(connexion.request.get_json())  # noqa: E501

    res = bots_r.set(user, 1)
    return 'do some magic!'


def get_all_users():  # noqa: E501
    """Get all users on email server

     # noqa: E501


    :rtype: List[User]
    """
    return 'do some magic!'


def monitor_users_get(email_addresses):  # noqa: E501
    """Add users to set to monitor email for (sent to kafka)

     # noqa: E501

    :param email_addresses: The full email addresses of the users to montor
    :type email_addresses: List[str]

    :rtype: List[bool]
    """
    res_codes = {True: "Success", False: "Failed"}
    results = []
    for address in email_addresses:
        res = users_r.set(address, 1)
        results.append(res_codes[res])
    return results


def remove_bot_account_get(email_addresses):  # noqa: E501
    """Remove a bot email account to send/receive messages from.

     # noqa: E501

    :param email_addresses: The full email addresses of the bot user to remove
    :type email_addresses: str

    :rtype: bool
    """
    return 'do some magic!'


def request_mail_history_get(email_addresses, request_key, back_to_iso_date_string):  # noqa: E501
    """Have all email involving users sent to historic kafka topic.

     # noqa: E501

    :param email_addresses: The full email addresses of the users to montor
    :type email_addresses: List[str]
    :param request_key: The provided key from requesting client to tag results with.
    :type request_key: str
    :param back_to_iso_date_string: The date back to retrieve email messages from.
    :type back_to_iso_date_string: str

    :rtype: List[bool]
    """
    return 'do some magic!'


def request_send_mail_post(email):  # noqa: E501
    """Send the email.

     # noqa: E501

    :param email: The email to send.
    :type email: dict | bytes

    :rtype: bool
    """
    if connexion.request.is_json:
        email = Email.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def unmonitor_users_get(email_addresses):  # noqa: E501
    """Remove users from set to monitor email for (sent to kafka)

     # noqa: E501

    :param email_addresses: The full email addresses of the users to unmonitor
    :type email_addresses: List[str]

    :rtype: List[bool]
    """
    res_codes = {1: "Success", 0: "Failed"}
    results = []
    for address in email_addresses:
        res = users_r.delete(address)
	results.append(res_codes[res])
    return results
