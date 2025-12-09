# Pydantic + Snow Leopard Example

A simple example demonstrating how to use Snow Leopard with Pydantic models for structured data extraction.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) package manager
- Anthropic API key
- [Snow Leopard API key](https://auth.snowleopard.ai/account/api_keys)

## Setup

1. Upload `superheroes.db` datafile to [try.snowleopard.ai](https://try.snowleopard.ai) and note the datafile ID

2. Set your API keys and datafile id:
```bash
export ANTHROPIC_API_KEY=...
export SNOWLEOPARD_API_KEY=...
export SNOWLEOPARD_EXAMPLE_DFID=...
```

## Usage

Run the agent:
```bash
uv run clai --agent agent:agent
```

Ask a question:
```
clai ➤ How many superheroes are there?
```
