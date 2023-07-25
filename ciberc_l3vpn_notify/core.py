"""
Module for global variables and common functions
"""

import pkg_resources
from nornir import InitNornir
from nornir.core.filter import F
from nornir_jinja2.plugins.tasks import template_file

template_path = pkg_resources.resource_filename(
    'ciberc_l3vpn_notify', 'templates')


def render_template(task):
    """
    Render template file
    """
    result = task.run(
        task=template_file,
        name="Render template",
        template=f"{task.host.platform}.j2",
        path=f"{template_path}/config-templates/",
        **task.host,
    )

    return result[0].result


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
