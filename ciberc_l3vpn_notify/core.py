"""
Module for global variables and common functions
"""

import pkg_resources
from nornir import InitNornir
from nornir.core.filter import F

template_path = pkg_resources.resource_filename(
    'ciberc_l3vpn_notify', 'templates')


def automated_init(device):
    """
    Initialize Nornir with filter by device
    """

    inv = InitNornir(
        inventory={
            "plugin": "SimpleInventory",
            "options": {
                "host_file": "hosts.yaml",
            },
        },
    )

    if device is not None and device != "all":
        list_devices = device.split(',')
        inv = inv.filter(F(name__any=list_devices))

    return inv
