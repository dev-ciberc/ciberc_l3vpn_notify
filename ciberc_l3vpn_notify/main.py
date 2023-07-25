"""
Principal module of the package
"""

import typer

from ciberc_l3vpn_notify.configure import configure

app = typer.Typer()


def main():
    """
    Command line entry points
    """

    app.command()(configure)

    return app()


if __name__ == "__main__":
    main()
