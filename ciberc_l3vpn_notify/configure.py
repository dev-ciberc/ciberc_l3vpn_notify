"""
Module to perform the configuration of the equipment
"""

import typer
from nornir_utils.plugins.functions import print_result

from ciberc_l3vpn_notify.core import (automated_init, backup_config,
                                      connect_device, render_template_config)


def configure_l3vpn(task):
    """
    Configure L3VPN
    """
    template = render_template_config(task)
    conn = connect_device(task)
    conn.open()

    if conn.is_alive():
        backup_config(task, conn.get_config()["running"], is_running=True)
        result = conn.load_merge_candidate(config=template)
        typer.echo(f"Configuring result: {result}")

        try:
            conn.commit_config()
        except Exception:
            pass

        conn.close()
    else:
        typer.echo(f"Failed to connect to {task.host.name}")


def configure(
    device: str = typer.Option(..., help="Device to configure"),
):
    """
    configure L3VPN
    """
    typer.echo("Configuring L3VPN")
    inv = automated_init(device=device)
    result = inv.run(task=configure_l3vpn)
    print_result(result)
