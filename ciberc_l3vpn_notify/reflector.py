"""
Module to report the BGP reflector for L3VPN configuration
"""
import re

import typer
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

from ciberc_l3vpn_notify.core import automated_init
from ciberc_l3vpn_notify.notify import make_notify_markdown


def _get_bgp_neighbors(data):
    """
    Get the BGP neighbors
    """
    # pylint: disable=line-too-long
    neighbor_pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\w\d]+)\s+(\d+)"  # noqa
    neighbors = re.findall(neighbor_pattern, data)
    return neighbors


def _report_bgp_neighbors(task):
    """
    Get info about the reflector L3VPN - BGP
    """
    result = task.run(
        task=netmiko_send_command,
        command_string="show bgp vpnv4 unicast all summary",
        use_textfsm=True
    )
    return _get_bgp_neighbors(result.result)


def reflector():
    """
    Reflector L3VPN
    """
    typer.echo("Reflector L3VPN")
    inv = automated_init(device=None, reflector=True)
    result = inv.run(task=_report_bgp_neighbors)
    data = result['REFLECTOR'][0]
    make_notify_markdown(data)
    print_result(data)
