def add(conn, username, repo, additions, deletions):
    cur = conn.cursor()
    cur.execute('INSERT INTO contributions (username, repo, additions, deletions) VALUES '
                '(%s, %s, %s, %s)', (username, str(repo), str(additions), str(deletions)))
    cur.close()
    conn.commit()


def del_repo_contributions(conn, repo):
    cur = conn.cursor()
    cur.execute('DELETE FROM contributions WHERE repo = %s', (repo,))
    cur.close()
    conn.commit()
