#!/usr/bin/env python
import click

@click.command()
@click.option("--mode",default='list', help="Enrichment mode (list or cluster).")


def main(mode):
    """Dummy function that prints arguments to console."""
    click.echo("AtEnrich running in {0} mode.".format(mode))

if __name__ == '__main__':
    main()