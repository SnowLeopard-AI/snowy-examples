# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a CopilotKit + PydanticAI + Snow Leopard starter template demonstrating a "chat with your data" agent. The application allows users to query the Northwind database using natural language and visualize the results through:
- **Shared State**: Agent state synchronized between frontend and backend to display full data results
- **Generative UI**: Custom UI components rendered inline when the agent calls tools
- **ToolReturn Metadata**: Pattern for sending state updates while returning different values to the agent

## Architecture

### Dual Server Architecture
The application runs two concurrent servers that communicate via HTTP:

1. **Next.js Frontend** (port 3000 by default)
   - Location: `src/`
   - Entry point: `src/app/page.tsx`
   - API route: `src/app/api/copilotkit/route.ts` - bridges frontend to agent via HttpAgent

2. **PydanticAI Agent Backend** (port 8000)
   - Location: `agent/src/`
   - Entry point: `agent/src/main.py`
   - Agent definition: `agent/src/agent.py`
   - Runs as FastAPI server via Uvicorn with hot reload

### State Synchronization
State must be defined in **both** locations and kept in sync:

- **Frontend**: `src/lib/types.ts` - TypeScript `AgentState` type
- **Backend**: `agent/src/agent.py` - Pydantic `DataState` model

When modifying agent state structure, **always update both files**.

### CopilotKit Integration Patterns

The main page (`src/app/page.tsx`) demonstrates two key patterns:

1. **`useCoAgent`**: Manages shared state between frontend and agent
   - Name: `"data_agent"` - must match the agent key in `route.ts`
   - Provides `state` object that updates automatically when agent emits `StateSnapshotEvent`

2. **`useRenderToolCall`**: Renders custom UI when agent calls the `get_data` tool
   - Displays query preview with SQL, row count, and top 5 rows
   - Component: `DataQueryCard` shows collapsible card in chat interface

### Agent-Frontend Connection

The connection flow:
```
Frontend (CopilotSidebar)
  → src/app/api/copilotkit/route.ts (HttpAgent pointing to localhost:8000)
  → agent/src/main.py (FastAPI server via agent.to_ag_ui())
  → agent/src/agent.py (PydanticAI agent with tools)
```

The agent is exposed via `agent.to_ag_ui(deps=StateDeps(DataState()))` in `main.py`.

### Agent Tools

The agent has two tools in `agent/src/agent.py`:

1. **`get_data(human_query: str)`**
   - Queries Snow Leopard's Northwind database using natural language
   - Stores full `SchemaData` in `state.data_responses[tool_call_id]`
   - Returns `ToolReturn` with:
     - `return_value`: Preview dict (SQL query, top 5 rows, row count) for agent reasoning
     - `metadata`: `StateSnapshotEvent` to update frontend state with full data
   - Pattern allows frontend to see full data while agent sees only preview (context efficiency)

2. **`read_get_data_response(tool_call_id: str, start_row: int, end_row: int)`**
   - Allows agent to read specific rows from a previous data query
   - Uses `tool_call_id` to reference stored query results
   - Returns windowed data slice for analysis

### ToolReturn Metadata Pattern

The agent uses `ToolReturn` with metadata to achieve dual-purpose tool responses:

```python
return ToolReturn(
  return_value=dict(sql_query=..., data_top=..., num_rows=...),  # Agent sees this
  metadata=[StateSnapshotEvent(...)],  # Frontend receives full state update
)
```

**Why**: Enables tools to update frontend state with complete data while returning only a preview to the agent for efficient context usage.

**Implementation**:
1. Tool stores full data in `ctx.deps.state.data_responses[ctx.tool_call_id]`
2. Tool returns `ToolReturn` with preview dict + `StateSnapshotEvent` in metadata
3. Frontend receives state update and displays full data table via `useCoAgent`
4. Agent receives only preview for reasoning about next steps

### UI Components

1. **`DataTable` (src/components/data-table.tsx)**
   - Main content area component
   - Displays full results from most recent query in state
   - Shows SQL query, row count, and scrollable table with all data

2. **`DataQueryCard` (src/components/data-query.tsx)**
   - Rendered inline in chat via `useRenderToolCall`
   - Collapsible card showing query preview (top 5 rows)
   - Provides immediate feedback when tool is called

## Key Dependencies

- **Frontend**: Next.js 16, React 19, CopilotKit 1.50+, @ag-ui/client
- **Agent**: PydanticAI (slim), Uvicorn, FastAPI, OpenAI, python-dotenv, snowleopard
- **Build**: uv (Python package manager), concurrently (multi-process runner)

### Dependency Management

**CRITICAL**: NEVER manually edit `pyproject.toml`, `package.json`, or lock files directly.

- **Python (agent/)**: Use `uv add <package>` or `uv remove <package>` commands
  - Example: `uv add fastapi` (NOT editing pyproject.toml)
  - Changes automatically update `pyproject.toml` and `uv.lock`

- **JavaScript (root)**: Use `npm install <package>` or `npm uninstall <package>`
  - Example: `npm install @copilotkit/react-core`
  - Changes automatically update `package.json` and `package-lock.json`

After dependency changes, the lock files are updated automatically. No manual sync needed.

## Environment Variables

Create `.env` file in `agent/` directory:

```
OPENAI_API_KEY=sk-...
SNOWLEOPARD_DATAFILE_ID=...
```

The `SNOWLEOPARD_DATAFILE_ID` should point to the uploaded Northwind database file on Snow Leopard.

## Common Patterns

### Adding a New Agent Tool
1. Define tool in `agent/src/agent.py` using `@agent.tool` decorator
2. If tool should update state, use `ToolReturn` pattern with `StateSnapshotEvent` in metadata
3. If tool should render UI, add `useRenderToolCall` in `src/app/page.tsx`
4. Provide clear docstring with parameter descriptions and examples

### Modifying Agent State
1. Update `DataState` Pydantic model in `agent/src/agent.py`
2. Update `AgentState` TypeScript type in `src/lib/types.ts`
3. Update initial state in `useCoAgent` hook if needed
4. Update component props if state shape changes

### Adding UI Components
1. Create component in `src/components/`
2. Import and use in `src/app/page.tsx`
3. Pass agent state via `useCoAgent` hook if component needs data
4. For tool-triggered UI, use `useRenderToolCall` hook

## Snow Leopard Integration

The agent uses Snow Leopard's `retrieve()` API to query the Northwind database:

```python
response = SnowLeopardClient().retrieve(
  user_query=human_query,
  datafile_id=os.environ['SNOWLEOPARD_DATAFILE_ID'],
)
```

Snow Leopard handles:
- Natural language to SQL translation
- Query execution
- Result formatting as `SchemaData` (query, rows, columns)
- Error handling for invalid queries or database errors

The agent's system prompt instructs it to never assume database schema - it should rely on Snow Leopard's natural language understanding and only reference specific tables/columns after seeing them in successful responses.

## Development Commands

- `npm run dev` - Start both UI (port 3000) and agent (port 8000) servers concurrently
- `npm run dev:ui` - Start only the Next.js frontend
- `npm run dev:agent` - Start only the PydanticAI agent backend
- `npm run build` - Build the Next.js application for production
- `npm run install:agent` - Set up Python virtual environment and install agent dependencies
