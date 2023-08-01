"""
Module that performs the rollback of the equipment configuration
"""

import typer
from tqdm import tqdm

from ciberc_l3vpn_notify.core import (automated_init, backup_config,
                                      connect_device, render_template_rollback)
from ciberc_l3vpn_notify.notify import make_notify


def rollback_l3vpn(task, pbar):
    """
    rollback L3VPN
    """
    template = render_template_rollback(task)
    conn = connect_device(task)
    conn.open()

    if conn.is_alive():
        backup_config(task, conn.get_config()["running"], is_running=True)
        conn.load_merge_candidate(config=template)

        try:
            conn.commit_config()
        except Exception:  # pylint: disable=broad-except
            typer.echo(f"Failed to commit configuration in {task.host.name}")

        conn.close()
    else:
        typer.echo(f"Failed to connect to {task.host.name}")

    pbar.update()


def rollback(
    device: str = typer.Option(..., help="Device to rollback"),
):
    """
    rollback L3VPN
    """
    typer.echo("Configuring L3VPN")
    inv = automated_init(device=device)
    len_devices = len(inv.inventory.hosts)

    with tqdm(total=len_devices) as pbar:
        result = inv.run(task=rollback_l3vpn, pbar=pbar)
        pbar.update()

    make_notify(result)
