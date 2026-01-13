# CopilotKit Snow Leopard Data Agent

This example agent demonstrates how to build a "chat with your data" agent using Snow Leopard, CopilotKit, and Pydantic AI.

The agent has a server-side tool that allows it to get data from Snow Leopard. This tool returns a preview but adds the  
entire data response into an AG-UI state object so it can be rendered onscreen for the user.

## Prerequisites

- OpenAI API Key (for the PydanticAI agent)
- Python 3.12+
- uv
- Node.js 20+ 
- npm or pnpm package manager

## Getting Started

1. Install dependencies using your preferred package manager:
```bash
pnpm install
```

2. Upload `northwind.db` ([found here](https://github.com/SnowLeopard-AI/playground_datasets/raw/refs/heads/main/northwind.db)) datafile to [try.snowleopard.ai](https://try.snowleopard.ai) and save the datafile id for later.


3. Set up your tokens:

Create a `.env` file inside the `agent` folder with the following content:

```
OPENAI_API_KEY=sk-...
SNOWLEOPARD_DATAFILE_ID=...
```


4. Start the development server:
```bash
pnpm dev
```

This will start both the UI and agent servers concurrently.

Now head over to [http://localhost:3000](http://localhost:3000) to start chatting with your data!

![](demo.mov)
