# Vercel AI + Snow Leopard Example

A simple example demonstrating how to use Snow Leopard with Vercel AI SDK to create an interactive CLI agent with data retrieval capabilities.

This project contains two files:
#### [tool.js](tool.js)
The SnowLeopard vercel-ai tool definition. This is the SnowLeopard-specific portion of the project

#### [cli.js](cli.js)
A generic js vercel-ai agent repl.


## Prerequisites

- [Node.js](https://nodejs.org/) (v18 or higher)
- [Snow Leopard API key](https://auth.snowleopard.ai/account/api_keys)
- OpenAI API key

## Setup

1. Upload `superheroes.db` ([found here](https://github.com/SnowLeopard-AI/playground_datasets/raw/refs/heads/main/superheroes.db)) datafile to [try.snowleopard.ai](https://try.snowleopard.ai) and note the datafile ID

2. Install dependencies:
```bash
npm install
```

3. Set your API keys and datafile id:
```bash
export SNOWLEOPARD_API_KEY=...
export SNOWLEOPARD_EXAMPLE_DATAFILE_ID=...
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
