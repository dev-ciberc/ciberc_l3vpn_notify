"""
Module that performs the rollback of the equipment configuration
"""

import typer
from nornir_utils.plugins.functions import print_result

from ciberc_l3vpn_notify.core import (automated_init, backup_config,
                                      connect_device, render_template_rollback)
from ciberc_l3vpn_notify.notify import make_notify


def rollback_l3vpn(task):
    """
    rollback L3VPN
    """
    template = render_template_rollback(task)
    conn = connect_device(task)
    conn.open()

    if conn.is_alive():
        backup_config(task, conn.get_config()["running"], is_running=True)
        result = conn.load_merge_candidate(config=template)
        typer.echo(f"Configuring result: {result}")

        try:
            conn.commit_config()
        except Exception:  # pylint: disable=broad-except
            pass

        conn.close()
    else:
        typer.echo(f"Failed to connect to {task.host.name}")


def rollback(
    device: str = typer.Option(..., help="Device to rollback"),
):
    """
    rollback L3VPN
    """
    typer.echo("Configuring L3VPN")
    inv = automated_init(device=device)
    result = inv.run(task=rollback_l3vpn)
    print_result(result)  # type: ignore
    make_notify(result)
