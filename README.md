## Github Stats

This script is used to collect statistic on contributions to Github or Github Enterprise
repositories. The collected statistics are stored in Postgres databases.

### Instructions

1. Install dependencies

```
    pipenv install 
```

2. Create Schemas

```bash

pipenv run python main.py create-schemas
```

3. Add Organization and Repositories

```bash

pipenv run python main.py add-orgs
pipenv run python main.py add-repos

```

4. Fetch the contributions

```bash

pipenv run python main.py get-contributions --days 30

```
The `--days` options can be used to pass the number of days in the past to consider 
while saving the contributions.

__Note:__ The *Access Token* and URL used to acces the API can be passed with the
environment variable `GITHUB_TOKEN` and `GITHUB_URL`. The connection string for
the Postgres database can be passed through the environment variable `DB_CONN`.
Following is a sample use:

```bash

    GITHUB_URL=https://github.example.com/api/v3 GITHUB_TOKEN=secrettokenxxxx33 \
    DB_CONN=posgres://ghestats:ghestats@localhost:5432/ghestats pipenv run \
    python main.py add-repos

```

