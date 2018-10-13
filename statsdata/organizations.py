from psycopg2.extras import execute_values


def truncate_organizations(conn):
    cur = conn.cursor()
    cur.execute('TRUNCATE TABLE organizations CASCADE')
    cur.close()
    conn.commit()


def add_orgs(conn, orgs):
    cur = conn.cursor()
    orgslist = []
    for o in orgs:
        orgslist.append((o.id, o.login, False))
    execute_values(cur, 'INSERT INTO organizations (id, name, scraped) VALUES %s', orgslist)
    cur.close()
    conn.commit()


def set_synced(conn, org):
    cur = conn.cursor()
    cur.execute('UPDATE organizations SET scraped = true WHERE id = %s', (org,))
    cur.close()
    conn.commit()


def get_unsynced(conn):
    cur = conn.cursor()
    cur.execute('SELECT id, name FROM organizations WHERE scraped=false')
    for c in cur:
        yield (c[0], c[1],)
    cur.close()
