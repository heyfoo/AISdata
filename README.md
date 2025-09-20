# AIS Data Seeder

This repository contains a Python script (`seed_data.py`) that inserts a set of
sample records into the AIS monitoring schema.

## Prerequisites

* Python 3.9 or later
* Network access to the target PostgreSQL database

The script uses `psycopg2` to connect to PostgreSQL. If you do not already have
it installed you can add it with:

```bash
python -m pip install psycopg2-binary
```

(You can run that command inside a virtual environment if you prefer.)

## Configure database credentials

The script reads PostgreSQL connection information from environment variables.
Export them in your shell before running the script:

```bash
export PGUSER="neondb_owner"
export PGPASSWORD="npg_ak9bhgtpyW0D"
export PGHOST="ep-rapid-water-af39gz9u.c-2.us-west-2.aws.neon.tech"
export PGPORT="5432"
export PGDATABASE="neondb"
export PGSSLMODE="require"  # Neon requires SSL connections
```

Adjust the values if you want to target a different database.

## Run the seeder

Once the environment variables are set, execute the script with Python:

```bash
python seed_data.py
```

The script will delete any existing rows that share the sample IDs and then
insert fresh copies of the dataset. You should see confirmation messages such
as:

```
Inserted 4 rows into users.
Inserted 3 rows into monitoring_areas.
...
```

## Verifying the data

You can confirm that the data landed in the database with your preferred SQL
client. For example, using `psql`:

```bash
psql "sslmode=require host=$PGHOST port=$PGPORT dbname=$PGDATABASE user=$PGUSER password=$PGPASSWORD" \
  -c "SELECT id, title, status FROM incidents ORDER BY created_at DESC;"
```
