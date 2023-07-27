"""
Module to perform the configuration of the equipment
"""

from difflib import ndiff

import typer
from nornir.core.task import Result
from nornir_napalm.plugins.tasks import napalm_configure, napalm_get
from nornir_utils.plugins.functions import print_result

from ciberc_l3vpn_notify.core import automated_init, render_template_config
from ciberc_l3vpn_notify.notify import make_notify


def get_config(task):
    """
    Get the running configuration
    """
    result = task.run(task=napalm_get, getters=["config"])
    return result.result["config"]["running"]


def task_diff_xr(task, template):
    """
    Task to diff the configuration
    """
    initial_config = get_config(task)
    diff = ndiff(
        initial_config.splitlines(keepends=True),
        template.splitlines(keepends=True)
    )
    diff = [line for line in diff if line.startswith('+')]

    return Result(
        name="Diff, =>PARTIAL support<= for IOS-XR",
        host=task.host,
        diff=''.join(diff)
    )


def configure_l3vpn(task, dry_run):
    """
    Configure L3VPN
    """
    template = render_template_config(task)
    if task.host.platform == "iosxr" and dry_run is True:
        result = task_diff_xr(task, template)
    else:
        result = task.run(
            task=napalm_configure,
            configuration=template,
            replace=False,
            dry_run=dry_run,
        )

    print_result(result)


def configure(
    device: str = typer.Option(..., help="Device to configure"),
    dry_run: bool = typer.Option(True, help="Dry run"),
):
    """
    configure L3VPN
    """
    typer.echo("Configuring L3VPN")
    inv = automated_init(device=device)
    result = inv.run(task=configure_l3vpn, dry_run=dry_run)
    make_notify(result)
