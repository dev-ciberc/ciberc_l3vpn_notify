"""
Module to notify users of changes in the system
"""

import os

from webexteamssdk import WebexTeamsAPI

WEBEX_ACCESS_TOKEN = os.environ.get("WEBEX_ACCESS_TOKEN")
LIST_USER_NOTIFY = os.environ.get("LIST_USER_NOTIFY")


def _send_message_webex(email: str, message: str, is_markdown: bool = False):
    """
    Send a message to a Webex Teams room
    """

    api = WebexTeamsAPI(access_token=f"{WEBEX_ACCESS_TOKEN}")

    if is_markdown:
        api.messages.create(
            toPersonEmail=email, markdown=message, markdownV2=True
        )
    else:
        api.messages.create(toPersonEmail=email, text=message)


def notify(message: str, is_markdown: bool = False):
    """
    Send a message to a Webex Teams room with email from env variable
    """
    list_users = LIST_USER_NOTIFY.split(",")
    for user in list_users:
        _send_message_webex(
            email=user,
            message=message,
            is_markdown=is_markdown
        )


def make_notify(result):
    """
    Notify the result of the configuration
    """
    host_failed = ""
    host_ok = ""
    for hostname, result in result.items():
        if result.failed:
            host_failed += f"{hostname} "
        else:
            host_ok += f"{hostname} "

    if host_failed:
        notify(message=f"Failed to configure L3VPN in {host_failed}")

    if host_ok:
        notify(message=f"L3VPN configured in {host_ok}")
