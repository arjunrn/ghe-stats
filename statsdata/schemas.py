import logging

logger = logging.getLogger(__name__)


def create_org(conn):
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS organizations CASCADE')
    cur.execute('CREATE TABLE organizations (id int, name varchar(100) , scraped bool DEFAULT false, PRIMARY KEY(id))')
    cur.close()
    conn.commit()


def create_repos(conn):
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS repos CASCADE')
    cur.execute('CREATE TABLE repos (id int, name varchar(100), org INT REFERENCES organizations(id) ON DELETE CASCADE,'
                'language VARCHAR(100), synced bool DEFAULT false, PRIMARY KEY(id))')
    cur.close()
    conn.commit()


def create_contributions(conn):
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS contributions')
    result = cur.execute('CREATE TABLE contributions (username varchar(50), repo INT REFERENCES repos(id) '
                         'ON DELETE CASCADE, additions INT, deletions INT)')
    logger.debug('Result: %s', str(result))
    cur.close()
    conn.commit()


def create_schemas(conn):
    create_org(conn)
    create_repos(conn)
    create_contributions(conn)
