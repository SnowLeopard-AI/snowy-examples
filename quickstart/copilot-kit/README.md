# CopilotKit + Snow Leopard Example

A Next.js application demonstrating how to integrate Snow Leopard with CopilotKit to create an interactive AI chat interface with data retrieval capabilities.

This project showcases:
- **[app/api/copilotkit/route.ts](app/api/copilotkit/route.ts)** - CopilotKit runtime with Snow Leopard backend action integration
- **[app/page.tsx](app/page.tsx)** - CopilotChat UI component
- **[app/layout.tsx](app/layout.tsx)** - CopilotKit provider setup

## Prerequisites

- [Node.js](https://nodejs.org/) (v18 or higher)
- [Snow Leopard API key](https://auth.snowleopard.ai/account)
- OpenAI API key

## Setup

1. Upload `northwind.db` ([found here](https://github.com/SnowLeopard-AI/playground_datasets/raw/refs/heads/main/northwind.db)) datafile to [try.snowleopard.ai](https://try.snowleopard.ai) and note the datafile ID

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file and add your API keys and datafile ID:
```bash
OPENAI_API_KEY=your-openai-api-key
SNOWLEOPARD_API_KEY=your-snowleopard-api-key
SNOWLEOPARD_DATAFILE_ID=your-datafile-id
```

## Usage

Run the development server:
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the CopilotKit chat interface.

You can now ask questions about the Northwind database:
```
> How many customers are there?
> What are the top selling products?
> Show me orders from Germany
```

The AI assistant will use the Snow Leopard backend action to retrieve data and answer your questions!
