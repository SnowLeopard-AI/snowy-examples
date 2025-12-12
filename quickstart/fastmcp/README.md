# FastMCP + Snow Leopard Example

A simple example demonstrating how to use Snow Leopard with FastMCP to create an MCP server with data retrieval capabilities.

In this example we show how to use this server with Claude Desktop, but it can be used with any system that supports the 
MCP protocol.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) package manager
- [Snow Leopard API key](https://auth.snowleopard.ai/account/api_keys)
- [Claude Desktop app](https://claude.ai/download)

## Setup

1. Upload `superheroes.db` ([found here](https://github.com/SnowLeopard-AI/playground_datasets/raw/refs/heads/main/superheroes.db)) datafile to [try.snowleopard.ai](https://try.snowleopard.ai) and note the datafile ID.

## Usage
We will launch the MCP server using fastmcp:
```bash
uv run fastmcp run server.py
```

This will start the MCP server that can be connected to by any MCP client (like Claude Desktop, clai, etc).

### Example with Claude Desktop

Add to your Claude Desktop configuration:

Note! You need to update the `/path/to/snowy-examples/fastmcp`, `SNOWLEOPARD_API_KEY`, and `SNOWLEOPARD_DATAFILE_ID`

```json
{
  "mcpServers": {
    "snowy": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/snowy-examples/quickstart/fastmcp",
        "run",
        "fastmcp",
        "run",
        "server.py"
      ],
      "env": {
        "SNOWLEOPARD_API_KEY": "your-api-key",
        "SNOWLEOPARD_DATAFILE_ID": "your-datafile-id"
      }
    }
  }
}
```

Now you can ask Claude questions about superhero data and it will use the Snow Leopard tool to retrieve information!

![screenshot](screenshot.png)
