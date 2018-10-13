import logging

import backoff
import github

from statsdata import organizations, contributions

logger = logging.getLogger(__name__)


def add_repos(unsync_orgs, client, cur):
    for o in unsync_orgs:
        org = client.get_org(o)
        repos = org.get_repos()


def truncate(conn, org_id):
    cur = conn.cursor()
    cur.execute('DELETE FROM repos WHERE org = %s', (str(org_id),))
    cur.close()
    conn.commit()


def del_org_repose(conn, o):
    cur = conn.cursor()
    cur.execute('DELETE FROM repos WHERE org = %s', (o,))
    cur.close()
    conn.commit()


def get_repos(conn, client, org_id, org_name):
    go = client.get_organization(org_name)
    repos = go.get_repos()
    del_org_repose(conn, org_id)
    for r in repos:
        cur = conn.cursor()
        cur.execute('INSERT INTO repos (id, name, org, language) VALUES (%s, %s, %s, %s)',
                    (str(r.id), r.name, org_id, r.language))
        cur.close()
    conn.commit()
    organizations.set_synced(conn, org_id)


def get_unsynced(conn):
    cur = conn.cursor()
    cur.execute('SELECT id FROM repos WHERE synced = false')
    for c in cur:
        yield c[0]
    cur.close()


def set_synced(conn, repo_id):
    cur = conn.cursor()
    cur.execute('UPDATE repos SET synced = true WHERE id = %s', (str(repo_id),))
    cur.close()
    conn.commit()


@backoff.on_exception(backoff.expo, github.BadCredentialsException, max_time=60 * 5)
def get_stats(client, repo_id):
    r = client.get_repo(repo_id)
    return r.get_stats_contributors()


def get_contributions(client, conn, repo_id, earliest):
    try:
        stats = get_stats(client, repo_id)
    except Exception as e:
        logger.warning('Could not fetch stats for Repo: %d', repo_id, e)
        return

    if not stats:
        return

    for s in stats:
        username = s.author.login
        additions = deletions = 0
        for w in s.weeks:
            if w.w > earliest:
                additions += w.a
                deletions += w.d
        if additions > 0 or deletions > 0:
            contributions.add(conn, username, repo_id, additions, deletions)
    set_synced(conn, repo_id)
