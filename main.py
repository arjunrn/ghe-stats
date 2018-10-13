import logging
from datetime import timedelta, datetime

import click

from ghe import client
from statsdata import connection, schemas, organizations, repos, contributions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('cmd')

conn_option = click.option('--db', type=str, help='The database connection string', prompt=True, envvar='DB_CONN')
token_option = click.option('--token', type=str, help='The Github Or Github Enterprise Token', prompt=True,
                            envvar='GITHUB_TOKEN')
github_option = click.option('--github-url', type=str, help='Github Enterprise URL', default='https://api.github.com',
                             envvar='GITHUB_URL')


@click.group()
def database():
    pass


@database.command()
@conn_option
def create_schemas(db):
    conn = connection.get_connection(db)
    logger.debug('Connection %s', conn)
    schemas.create_schemas(conn)


@click.group()
def ghe():
    pass


@ghe.command()
@token_option
@github_option
def whoami(token, github_url):
    g = client.client(token, github_url)
    user = g.get_user()
    click.echo('User: {}'.format(user.login))


@ghe.command()
@conn_option
@token_option
@github_option
def add_orgs(db, token, github_url):
    g = client.client(token, github_url)
    conn = connection.get_connection(db)
    organizations.truncate_organizations(conn)
    organs = g.get_organizations()
    organizations.add_orgs(conn, organs)


@ghe.command()
@conn_option
@token_option
@github_option
def add_repos(db, token, github_url):
    g = client.client(token, github_url)
    conn = connection.get_connection(db)
    for org in organizations.get_unsynced(conn):
        logger.debug("Adding Organization: %s", str(org))
        repos.truncate(conn, org[0])
        repos.get_repos(conn, g, org[0], org[1])
    logger.debug("Finished processing orgs")


@ghe.command()
@conn_option
@token_option
@github_option
@click.option("--days", type=int, help="Number of days of contributions for syncing", default=30)
def get_contributions(db, token, github_url, days):
    six_months_ago = datetime.now() + timedelta(days=-days)
    g = client.client(token, github_url)
    conn = connection.get_connection(db)
    for r in repos.get_unsynced(conn):
        logger.info('Syncing Repository: %s', str(r))
        contributions.del_repo_contributions(conn, r)
        repos.get_contributions(g, conn, r, six_months_ago)


cli = click.CommandCollection(sources=[database, ghe])
if __name__ == '__main__':
    cli()
