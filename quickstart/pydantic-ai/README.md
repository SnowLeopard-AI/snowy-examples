# Pydantic + Snow Leopard Example

A simple example demonstrating how to use Snow Leopard with Pydantic models for structured data extraction.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) package manager
- Anthropic API key
- [Snow Leopard API key](https://auth.snowleopard.ai/account/api_keys)

## Setup

1. Upload `superheroes.db` ([found here](https://github.com/SnowLeopard-AI/playground_datasets/raw/refs/heads/main/superheroes.db)) datafile to [try.snowleopard.ai](https://try.snowleopard.ai) and note the datafile ID

2. Set your API keys and datafile id:
```bash
export ANTHROPIC_API_KEY=...
export SNOWLEOPARD_API_KEY=...
export SNOWLEOPARD_EXAMPLE_DATAFILE_ID=...
```

## Usage
We will launch our agent as a CLI interface using clai:
```bash
uv run clai --agent agent:agent
```

Now we have entered an interactive repl where we can ask questions:
```
clai ➤ How many superheroes are there?
```
