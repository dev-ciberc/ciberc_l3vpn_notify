"""
Module for global variables and common functions
"""
import os

import pkg_resources
from napalm import get_network_driver
from nornir import InitNornir
from nornir.core.filter import F
from nornir_jinja2.plugins.tasks import template_file

template_path = pkg_resources.resource_filename(
    'ciberc_l3vpn_notify', 'templates')


def backup_config(task, config: str, is_running: bool = True):
    """
    Backup the configuration of a device to a file
    """

    backup_folder = "backup-dispositivos" if is_running else "nueva-configuracion"  # noqa
    os.makedirs(backup_folder, exist_ok=True)
    backup_file = os.path.join(backup_folder, f"{task.host.name}.cfg")
    with open(backup_file, "w", encoding="utf8") as file:
        file.write(config)


def connect_device(task):
    """
    Connect to device
    """
    driver = get_network_driver(task.host.platform)
    device = driver(
        hostname=task.host.hostname,
        username=task.host.username,
        password=task.host.password,
        optional_args={'port': task.host.port},
    )

    return device


def render_template_config(task):
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


def render_template_rollback(task):
    """
    Render template file
    """
    result = task.run(
        task=template_file,
        name="Render template",
        template=f"{task.host.platform}.j2",
        path=f"{template_path}/rollback-templates/",
        **task.host,
    )

    return result[0].result


def automated_init(device, reflector=False):
    """
    Initialize Nornir with filter by device
    """

    inv = InitNornir(
        inventory={
            "plugin": "SimpleInventory",
            "options": {
                "host_file": "hosts.yaml",
                "defaults_file": "defaults.yaml",
            },
        },
    )

    if reflector:
        inv = inv.filter(F(name__any=["REFLECTOR"]))
    else:
        inv = inv.filter(~F(name__any=["REFLECTOR"]))

        if device is not None and device != "all":
            list_devices = device.split(',')
            inv = inv.filter(F(name__any=list_devices))

    return inv
