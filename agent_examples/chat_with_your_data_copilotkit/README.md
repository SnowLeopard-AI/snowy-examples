# CopilotKit Snow Leopard Data Agent

This example agent demonstrates how to build a "chat with your data" agent using Snow Leopard, CopilotKit, and Pydantic AI.

The agent has a server-side tool that allows it to get data from Snow Leopard. This tool returns a preview but adds the  
entire data response into an AG-UI state object so it can be rendered onscreen for the user.

**[Try the live demo](https://try.snowleopard.ai/demos/data-agent)**

![](data_agent.png)

## Prerequisites

- OpenAI API Key (for the PydanticAI agent)
- Python 3.12+
- uv
- Node.js 20+ 
- npm or pnpm package manager
- A PostgreSQL database that Snow Leopard Cloud can reach (see [docs/postgres-setup.md](../../docs/postgres-setup.md))

## Getting Started

1. Install dependencies using your preferred package manager:
```bash
pnpm install
```

2. Load the Northwind sample database into PostgreSQL. The [northwind_psql](https://github.com/SnowLeopard-AI/northwind_psql) repository has a `northwind.sql` script; run it against a hosted database such as [Neon](https://neon.com) or [Supabase](https://supabase.com):
```bash
psql "postgresql://USER:PASSWORD@HOST/DBNAME?sslmode=require" -f northwind.sql
```
[docs/postgres-setup.md](../../docs/postgres-setup.md) covers the details.

3. Create a [Snow Leopard Cloud](https://cloud.snowleopard.ai) instance, add the Northwind database as a data source, create an API key on the **Keys** tab, and copy the instance ID from the **Connection Info** tab. See the [Cloud getting started guide](https://docs.snowleopard.ai/cloud/getting-started).

4. Set up your tokens:

Create a `.env` file inside the `agent` folder with the following content:

```
OPENAI_API_KEY=sk-...
SNOWLEOPARD_API_KEY=...
SNOWLEOPARD_INSTANCE_ID=...
```


5. Start the development server:
```bash
pnpm dev
```

This will start both the UI and agent servers concurrently.

Now head over to [http://localhost:3000](http://localhost:3000) to start chatting with your data!
