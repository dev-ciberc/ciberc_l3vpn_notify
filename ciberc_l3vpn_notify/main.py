"""
Principal module of the package
"""

import typer

from ciberc_l3vpn_notify.configure import configure
from ciberc_l3vpn_notify.rollback import rollback

app = typer.Typer()


def main():
    """
    Command line entry points
    """

    app.command()(configure)
    app.command()(rollback)

    return app()


if __name__ == "__main__":
    main()
