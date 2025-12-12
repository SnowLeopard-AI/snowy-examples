# Snow Leopard API Examples

This repository contains a collection of self-contained examples demonstrating how to use the **[Snow Leopard APIs](https://docs.snowleopard.ai/)** in different environments, languages, and scenarios. 

There are two folders in this repo:
1. **Quickstarts**: Simple code snippets to get started with an agent framework quickly
2. **Agent Examples**: Detailed examples of working agents built to showcase different use cases

Each folder within these topic-folders focuses on a single example, including minimal setup, runnable code, and explanations.


## 🚀 Getting Started

To start playing with the examples, make sure you have:

* A valid [Snow Leopard API key](https://docs.snowleopard.ai/#authentication)
* Any language/runtime dependencies required by the specific example (Node, Python, etc.)

### Most examples follow this pattern:

1. **Install dependencies**
2. **Configuration** - The Following are typically set as environment variables:
    - `SNOWLEOPARD_API_KEY` - You can create an API key [here](https://auth.snowleopard.ai/account/api_keys)
    - `SNOWLEOPARD_DATAFILE_ID` - Go to [Snow Leopard Playground](https://try.snowleopard.ai), upload a datafile, and then click the `Copy ID` button for that file

Check the README inside each folder for exact steps after that.


## Quickstart Examples
* [**fastmcp**](https://github.com/SnowLeopard-AI/snowy-examples/tree/main/quickstart/fastmcp) - FastMCP + Snow Leopard Example
* [**langchain**](https://github.com/SnowLeopard-AI/snowy-examples/tree/main/quickstart/langchain) - LangChain Snow Leopard Quick Start Guide
* [**langgraph**](https://github.com/SnowLeopard-AI/snowy-examples/tree/main/quickstart/langgraph) - LangGraph Snow Leopard Quick Start Guide
* [**pydantic-ai**](https://github.com/SnowLeopard-AI/snowy-examples/tree/main/quickstart/pydantic-ai) - Pydantic + Snow Leopard Example
* [**vercel-ai**](https://github.com/SnowLeopard-AI/snowy-examples/tree/main/quickstart/vercel-ai) - Vercel AI + Snow Leopard Example


## 📁 Agent Examples
* [**financial_coach_langchain**](https://github.com/SnowLeopard-AI/snowy-examples/tree/main/agent_examples/financial_coach_langchain) - An example agent built using [Langchain]([url](https://www.langchain.com/)) that acts as a personal _Financial Coach_. 
* [**gameclub_crewai**](https://github.com/SnowLeopard-AI/snowy-examples/tree/main/agent_examples/gameclub_crewai) - An example agent built using [Crew AI](https://www.crewai.com/) that helps you build a _Game Discussion Club Plan_.


## 📝 License

This repository is licensed under the **MIT License** unless otherwise specified.
