"""
Principal module of the package
"""

import typer

from ciberc_l3vpn_notify.configure import configure
from ciberc_l3vpn_notify.reflector import reflector
from ciberc_l3vpn_notify.rollback import rollback

app = typer.Typer()


def main():
    """
    Command line entry points
    """

    app.command()(configure)
    app.command()(rollback)
    app.command()(reflector)

    return app()


if __name__ == "__main__":
    main()
