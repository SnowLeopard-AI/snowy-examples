# Loading example data into PostgreSQL for Snow Leopard Cloud

Snow Leopard Cloud queries live databases: PostgreSQL (including Neon and Supabase) and Google BigQuery. It does not accept
uploaded files. Each example in this repository ships its dataset as a plain SQL script that creates the tables and inserts
the rows, so you can load it into any PostgreSQL database with `psql` or a web SQL editor.

This page walks through the steps every example shares. Each example's README tells you which SQL file to load.

## 1. Get a PostgreSQL database that Snow Leopard Cloud can reach

Snow Leopard Cloud connects to your database over the internet, so the database needs a publicly reachable host.
The quickest options are hosted free tiers:

- [Neon](https://neon.com): create a project, then create one database per example (for example `northwind`, `finance_coach`, `metacritic`).
- [Supabase](https://supabase.com): create a project per example. Use the **Shared Pooler (Supavisor)** connection details when adding the data source to Snow Leopard, as described in the [Cloud docs](https://docs.snowleopard.ai/cloud/getting-started#adding-a-data-source).

Any other PostgreSQL you can expose publicly (RDS, Cloud SQL, a VPS) works the same way. A PostgreSQL running only on
your laptop or in a local Docker container is **not** reachable by Snow Leopard Cloud unless you put a public tunnel in
front of it, so treat local databases as a development convenience only.

Use a separate database (or a separate Snow Leopard instance) for each example. Snow Leopard reads every schema it can
see through the credentials you give it, and keeping datasets apart keeps its query planner from mixing them.

## 2. Load the SQL file

With `psql` installed locally, point it at the database connection string your provider gives you and run the example's
SQL file:

```bash
psql "postgresql://USER:PASSWORD@HOST/DBNAME?sslmode=require" -f path/to/dataset.sql
```

If you prefer not to install `psql`, paste the contents of the SQL file into your provider's web SQL editor and run it.
The example SQL files use only `CREATE TABLE`, `INSERT`, and `CREATE VIEW`, which every editor supports.

The scripts start with `DROP ... IF EXISTS` statements, so re-running one replaces the previous load.

## 3. Connect the database to a Snow Leopard Cloud instance

1. Sign in to [Snow Leopard Cloud](https://cloud.snowleopard.ai) and create an instance.
2. On the instance page, click **Add Data Source**, pick PostgreSQL (or Neon / Supabase), and enter the host, database
   name, username, and password for the database you loaded.
3. On the **Keys** tab, create an API key. It is shown only once, so copy it now.
4. On the **Connection Info** tab, copy the instance ID.

The full walkthrough with screenshots is in the [Cloud getting started guide](https://docs.snowleopard.ai/cloud/getting-started).

## 4. Configure the example

Every example reads two environment variables:

```bash
SNOWLEOPARD_API_KEY=...       # from the instance's Keys tab
SNOWLEOPARD_INSTANCE_ID=...   # from the instance's Connection Info tab
```

Put them in the example's `.env` file (each example ships a `.env.example`) or export them in your shell.

## 5. Smoke test before running the agent

The `snowleopard` Python package installs a small `snowy` CLI you can use to confirm the instance answers questions about the
data you loaded:

```bash
pip install "snowleopard>=0.5.1"
export SNOWLEOPARD_API_KEY=...
snowy retrieve --instance "$SNOWLEOPARD_INSTANCE_ID" "How many rows are in the largest table?"
```

If that returns rows, the example's agent will be able to query the data too.
