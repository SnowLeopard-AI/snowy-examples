# Pydantic + Snow Leopard Example

A simple example demonstrating how to use Snow Leopard with Pydantic models for structured data extraction.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) package manager
- Anthropic API key
- [Snow Leopard Cloud API key](https://docs.snowleopard.ai/cloud/getting-started#api-keys)

## Setup

1. Create a [Snow Leopard Cloud](https://cloud.snowleopard.ai) instance, connect a data source, and note the instance ID from the instance's **Connection Info** tab. See the [Cloud getting started guide](https://docs.snowleopard.ai/cloud/getting-started) for details.
   - Don't have data? Load the [sample Northwind dataset](https://github.com/SnowLeopard-AI/northwind_psql) into a PostgreSQL database that Snow Leopard Cloud can reach, such as a hosted [Neon](https://neon.com) or [Supabase](https://supabase.com) database. Run the dataset's `northwind.sql` script against your database, then [add the database as a data source](https://docs.snowleopard.ai/cloud/getting-started#adding-a-data-source) in your instance.

2. Set your API keys and instance ID:
```bash
export ANTHROPIC_API_KEY=...
export SNOWLEOPARD_API_KEY=...
export SNOWLEOPARD_INSTANCE_ID=...
```

## Usage
We will launch our agent as a CLI interface using clai:
```bash
uv run clai --agent agent:agent
```

Now we have entered an interactive repl where we can ask questions:
```
clai ➤ How many customers do we have?
```
