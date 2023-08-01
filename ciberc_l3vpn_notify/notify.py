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
    for hostname, result_item in result.items():
        if result_item.failed:
            host_failed += f"{hostname} "
        else:
            host_ok += f"{hostname} "

    if host_failed:
        notify(message=f"The process has Failed in {host_failed}")

    if host_ok:
        notify(message=f"Process configured in {host_ok}")


def make_notify_markdown(data):
    """
    Notify the result of the configuration in markdown
    """
    text_for_markdown = ""  # noqa

    for item in data.result:
        rid = item[0]
        _as = item[2]
        ms_rcvd = item[3]
        ms_sent = item[4]
        state = int(item[9])

        # si el estado es cero, icono de bola roja, si no, verde
        if int(state) == 0:
            icon = "🔴"
        else:
            icon = "🟢"

        # pylint: disable=line-too-long
        text_for_markdown += f"""\n **{rid}** \t {_as} \t {ms_rcvd} \t\t {ms_sent} \t\t {icon}::{state} \n"""  # noqa

    # pylint: disable=f-string-without-interpolation
    message = f"""
    ### **Reflector Report**\n*RID* \t *AS* \t *MS-RCVD* \t *MS-SENT* \t *STATE* \n
    { text_for_markdown  }
    """  # noqa

    notify(message=message, is_markdown=True)
