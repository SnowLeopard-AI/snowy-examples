# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a CopilotKit + PydanticAI starter template for building AI agents with a Next.js frontend. The application demonstrates a proverbs management system with multiple CopilotKit integration patterns:
- **Shared State**: Agent state synchronized between frontend and backend
- **Generative UI**: Dynamic UI components rendered from tool calls
- **Frontend Tools**: Client-side actions callable by the agent
- **Human-in-the-Loop**: Interactive approval flows for agent actions

## Architecture

### Dual Server Architecture
The application runs two concurrent servers that communicate via HTTP:

1. **Next.js Frontend** (port 3000 by default)
   - Location: `src/`
   - Entry point: `src/app/page.tsx`
   - API route: `src/app/api/copilotkit/route.ts` - bridges frontend to agent

2. **PydanticAI Agent Backend** (port 8000)
   - Location: `agent/src/`
   - Entry point: `agent/src/main.py`
   - Agent definition: `agent/src/agent.py`
   - Runs as FastAPI server via Uvicorn with hot reload

### State Synchronization
State must be defined in **both** locations and kept in sync:

- **Frontend**: `src/lib/types.ts` - TypeScript `AgentState` type
- **Backend**: `agent/src/agent.py` - Pydantic `ProverbsState` model

When modifying agent state structure, **always update both files**.

### CopilotKit Integration Patterns

The main page (`src/app/page.tsx`) demonstrates four key patterns:

1. **`useCoAgent`**: Manages shared state between frontend and agent
2. **`useRenderToolCall`**: Renders custom UI when agent calls specific tools (e.g., `get_weather`)
3. **`useFrontendTool`**: Defines client-side actions the agent can call (e.g., `setThemeColor`)
4. **`useHumanInTheLoop`**: Creates approval flows for sensitive agent actions (e.g., `go_to_moon`)

### Agent-Frontend Connection

The connection flow:
```
Frontend (CopilotSidebar)
  → src/app/api/copilotkit/route.ts (HttpAgent pointing to localhost:8000)
  → agent/src/main.py (FastAPI server)
  → agent/src/agent.py (PydanticAI agent with tools)
```

The agent uses `agent.to_ag_ui()` in `main.py` to expose the PydanticAI agent via AG-UI protocol.

### Agent Tools

Tools in `agent/src/agent.py` can return `StateSnapshotEvent` to update shared state. Regular tools return primitive values. The system prompt instructs the agent to always check current state before modifying it.

### Custom Event Streaming Pattern

The agent uses a custom event streaming pattern (based on [PydanticAI issue #2382](https://github.com/pydantic/pydantic-ai/issues/2382)) to send state updates AND return different values from tools:

**Why**: Allows tools to update frontend state via `StateSnapshotEvent` while returning a different value for the agent's reasoning.

**Implementation**:
1. `CustomDeps` class extends `StateDeps[ProverbsState]` with:
   - `event_stream: MemoryObjectSendStream[str]` - for sending events
   - `encoder: EventEncoder` - for encoding events to strings

2. `main.py` creates memory streams and passes them to `run_ag_ui()`:
   ```python
   send_stream, receive_stream = create_memory_object_stream[str](max_buffer_size=100)
   deps = CustomDeps(state=ProverbsState(), event_stream=send_stream, encoder=EventEncoder())
   run_ag_ui(agent=agent, request=request, deps=deps, extra_event_stream=receive_stream)
   ```

3. Tools send events while returning different values:
   ```python
   # Update state and send event to frontend
   ctx.deps.state.queries[ctx.tool_call_id] = full_data
   await ctx.deps.event_stream.send(
     ctx.deps.encoder.encode(StateSnapshotEvent(type=EventType.STATE_SNAPSHOT, snapshot=ctx.deps.state))
   )
   # Return preview for agent reasoning
   return preview_dict
   ```

This pattern enables tools like `query_data` to store full data in state (for frontend access) while returning only a preview (for agent context efficiency).

## Key Dependencies

- **Frontend**: Next.js 16, React 19, CopilotKit 1.50+, @ag-ui/client
- **Agent**: PydanticAI (slim), Uvicorn, FastAPI, anyio, OpenAI, python-dotenv
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

## Common Patterns

### Adding a New Agent Tool
1. Define tool in `agent/src/agent.py` using `@agent.tool` decorator
2. If tool should render UI, add `useRenderToolCall` in `src/app/page.tsx`
3. If tool modifies state, return `StateSnapshotEvent` with updated state

### Adding Frontend Actions
1. Add `useFrontendTool` hook in `src/app/page.tsx`
2. Define parameters and handler function
3. Frontend actions don't need backend changes

### Modifying Agent State
1. Update `ProverbsState` Pydantic model in `agent/src/agent.py`
2. Update `AgentState` TypeScript type in `src/lib/types.ts`
3. Update initial state in `useCoAgent` hook if needed
