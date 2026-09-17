# Snow Leopard API Examples

This repository contains a collection of self-contained examples demonstrating how to use the **[Snow Leopard APIs](https://docs.snowleopard.ai/)** in different environments, languages, and scenarios. 

There are two folders in this repo:
1. **Quickstarts**: Simple code snippets to get started with an agent framework quickly
2. **Agent Examples**: Detailed examples of working agents built to showcase different use cases

Each folder within these topic-folders focuses on a single example, including minimal setup, runnable code, and explanations.


## 🚀 Getting Started

To start playing with the examples, make sure you have:

* A [Snow Leopard Cloud](https://cloud.snowleopard.ai) instance with at least one data source connected
* A valid [Snow Leopard Cloud API key](https://docs.snowleopard.ai/cloud/getting-started#api-keys)
* Any language/runtime dependencies required by the specific example (Node, Python, etc.)

### Most examples follow this pattern:

1. **Install dependencies**
2. **Configuration** - The Following are typically set as environment variables:
    - `SNOWLEOPARD_API_KEY` - Create an API key from your instance's **Keys** tab. See [API Keys](https://docs.snowleopard.ai/cloud/getting-started#api-keys)
    - `SNOWLEOPARD_INSTANCE_ID` - Copy the instance ID from your instance's **Connection Info** tab. See [Connection Info](https://docs.snowleopard.ai/cloud/getting-started#connection-info)

Check the README inside each folder for exact steps after that.


## Integrations: Quickstart
* [**Agentuity**](https://github.com/SnowLeopard-AI/snowy-examples/tree/main/quickstart/fastmcp) - Agentuity Platform + Snow Leopard Example
* [**LangChain**](https://github.com/SnowLeopard-AI/snowy-examples/tree/main/quickstart/langchain) - LangChain + Snow Leopard Quick Start Guide
* [**LangGraph**](https://github.com/SnowLeopard-AI/snowy-examples/tree/main/quickstart/langgraph) - LangGraph + Snow Leopard Quick Start Guide
* [**MCP**](https://github.com/SnowLeopard-AI/snowy-examples/tree/main/quickstart/fastmcp) - FastMCP + Snow Leopard Example
* [**Pydantic**](https://github.com/SnowLeopard-AI/snowy-examples/tree/main/quickstart/pydantic-ai) - Pydantic AI + Snow Leopard Example
* [**Vercel**](https://github.com/SnowLeopard-AI/snowy-examples/tree/main/quickstart/vercel-ai) - Vercel AI SDK + Snow Leopard Example


## 📁 Agent: Examples
* [**chat_with_you_data_copilotkit**](https://github.com/SnowLeopard-AI/snowy-examples/tree/main/agent_examples/chat_with_your_data_copilotkit) - An example “chat with your data” application built using [CopilotKit](https://www.copilotkit.ai) and [Pydantic AI](https://ai.pydantic.dev).
* [**financial_coach_langchain**](https://github.com/SnowLeopard-AI/snowy-examples/tree/main/agent_examples/financial_coach_langchain) - An example agent built using [Langchain]([url](https://www.langchain.com/)) that acts as a personal _Financial Coach_. 
* [**gameclub_crewai**](https://github.com/SnowLeopard-AI/snowy-examples/tree/main/agent_examples/gameclub_crewai) - An example agent built using [Crew AI](https://www.crewai.com/) that helps you build a _Game Discussion Club Plan_.


## 📝 License

This repository is licensed under the **MIT License** unless otherwise specified.
