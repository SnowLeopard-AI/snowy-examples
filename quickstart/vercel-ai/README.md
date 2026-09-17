# Vercel AI SDK + Snow Leopard Example

A simple example demonstrating how to use Snow Leopard with Vercel AI SDK to create an interactive CLI agent with data retrieval capabilities.

This project contains two files:
#### [tool.js](tool.js)
The SnowLeopard vercel-ai tool definition. This is the SnowLeopard-specific portion of the project

#### [cli.js](cli.js)
A generic js vercel-ai agent repl.


## Prerequisites

- [Node.js](https://nodejs.org/) (v18 or higher)
- [Snow Leopard Cloud API key](https://docs.snowleopard.ai/cloud/getting-started#api-keys)
- OpenAI API key

## Setup

1. Create a [Snow Leopard Cloud](https://cloud.snowleopard.ai) instance, connect a data source, and note the instance ID from the instance's **Connection Info** tab. See the [Cloud getting started guide](https://docs.snowleopard.ai/cloud/getting-started) for details.
   - Don't have data? Use our sample `superheroes.db` dataset ([found here](https://github.com/SnowLeopard-AI/playground_datasets/raw/refs/heads/main/superheroes.db)).

2. Install dependencies:
```bash
npm install
```

3. Set your API keys and instance ID:
```bash
export SNOWLEOPARD_API_KEY=...
export SNOWLEOPARD_INSTANCE_ID=...
export OPENAI_API_KEY=...
```

## Usage

Launch the interactive CLI agent:
```bash
npm run snowy
```

Now you have entered an interactive REPL where you can ask questions:
```
Agent REPL started. Type your commands (Ctrl+C to exit)
> how many superheroes are there?
```

The agent will use the Snow Leopard tool to retrieve superhero data and answer your questions!

Type `Ctrl+C` to exit.
