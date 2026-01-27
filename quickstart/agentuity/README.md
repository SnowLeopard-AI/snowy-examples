# Agentuity + Snow Leopard Example

A simple example demonstrating how to use Snow Leopard with the Agentuity platform and Vercel AI SDK to create a chat agent with data retrieval capabilities and conversation history.

This project contains two key files:

#### [src/agent/tools/getData.ts](src/agent/tools/getData.ts)
The Snow Leopard Vercel AI tool definition. This is the Snow Leopard-specific portion of the project.

This tool allows our agent to retrieve data using Snow Leopard's `/retrieve` endpoint. To learn more, visit [Snow 
Leopard docs](https://docs.snowleopard.ai)

#### [src/agent/chat/agent.ts](src/agent/chat/agent.ts)
An Agentuity agent powered by Vercel AI SDK with persistent conversation history via thread state.

## Prerequisites

- [Agentuity CLI](https://agentuity.com/)
- [Bun](https://bun.sh/) runtime
- [Snow Leopard API key](https://auth.snowleopard.ai/account/api_keys)
- [OpenAI API key](https://platform.openai.com/api-keys)

## Setup

1. Upload `northwind.db` ([found here](https://github.com/SnowLeopard-AI/playground_datasets/raw/refs/heads/main/northwind.db)) datafile to [try.snowleopard.ai](https://try.snowleopard.ai) and note the datafile ID

2. Install dependencies:
```bash
bun install
```

3. Set your API keys and datafile id in `.env`:
```
SNOWLEOPARD_API_KEY=...
SNOWLEOPARD_DATAFILE_ID=...
OPENAI_API_KEY=...
```

## Usage

Launch the development server:
```bash
agentuity dev
```

Now you can send requests to the chat endpoint:
```bash
curl -X POST http://localhost:3500/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the top 20 performing territories by revenue?"}' | jq -r ".response"
```

The agent will use the Snow Leopard tool to query the Northwind database and answer your questions!
```
Here are the top 20 territories by total revenue (USD), computed as sum(UnitPrice * Quantity * (1 − Discount)) across all orders in the Northwind dataset. Revenues are rounded to 2 decimals.

1. Rockville — USD 232,890.85
2. Greensboro — USD 232,890.85
3. Cary — USD 232,890.85
4. Atlanta — USD 202,812.84
5. Savannah — USD 202,812.84
6. Orlando — USD 202,812.84
7. Tampa — USD 202,812.84
8. Wilton — USD 192,107.60
9. Neward — USD 192,107.60
10. Westboro — USD 166,537.76
11. Bedford — USD 166,537.76
12. Georgetow — USD 166,537.76
13. Boston — USD 166,537.76
14. Cambridge — USD 166,537.76
15. Braintree — USD 166,537.76
16. Louisville — USD 166,537.76
17. Philadelphia — USD 126,862.28
18. Beachwood — USD 126,862.28
19. Findlay — USD 126,862.28
20. Racine — USD 126,862.28

Notes:
- Method: joined territories → employee_territories → employees → orders → order_details; revenue per order line = UnitPrice * Quantity * (1 − Discount).
- Timeframe: all orders present in the dataset (no date filter applied).
- Some territory names in the dataset appear truncated or duplicated (e.g., "Neward", "Georgetow").
```
