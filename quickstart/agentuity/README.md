# Agentuity + Snow Leopard Example

A simple example demonstrating how to use [Snow Leopard](https://snowleopard.ai/) with the [Agentuity](https://agentuity.com/) platform using the [Vercel AI SDK](https://sdk.vercel.ai/) to create a **chat agent** with data retrieval capabilities and conversation history.

This project contains two key files:

1. **[src/agent/tools/getData.ts](src/agent/tools/getData.ts)**
   - This has the Snow Leopard tool definition for Vercel AI.
   - This is the Snow Leopard-specific portion of the project.
   - This tool allows our chat agent to retrieve data from a SQL database using Snow Leopard's `/retrieve` endpoint. To learn more, visit [Snow Leopard docs](https://docs.snowleopard.ai)

2. **[src/agent/chat/agent.ts](src/agent/chat/agent.ts)**
   - This defines an Agentuity agent, powered by Vercel AI SDK
   - It has persistent conversation history via thread state

## Prerequisites

- [Agentuity CLI](https://agentuity.com/)
- [Bun](https://bun.sh/) runtime
- [Snow Leopard Cloud API key](https://docs.snowleopard.ai/cloud/getting-started#api-keys)
- [OpenAI API key](https://platform.openai.com/api-keys)

## Setup

1. Create a [Snow Leopard Cloud](https://cloud.snowleopard.ai) instance, connect a data source, and note the instance ID from the instance's **Connection Info** tab. See the [Cloud getting started guide](https://docs.snowleopard.ai/cloud/getting-started) for details.
   - Don't have data? Load the [sample Northwind dataset](https://github.com/SnowLeopard-AI/northwind_psql) into a PostgreSQL database that Snow Leopard Cloud can reach, such as a hosted [Neon](https://neon.com) or [Supabase](https://supabase.com) database. Run the dataset's `northwind.sql` script against your database, then [add the database as a data source](https://docs.snowleopard.ai/cloud/getting-started#adding-a-data-source) in your instance.

2. Install dependencies:
```bash
bun install
```

3. Set your API keys and instance ID in `.env`:
```
SNOWLEOPARD_API_KEY=...
SNOWLEOPARD_INSTANCE_ID=...
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
