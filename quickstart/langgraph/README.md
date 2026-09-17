# LangGraph Snowleopard AI Quick Start Guide


## Prerequisites

- Python 3.10+
- [Snow Leopard Cloud API key](https://docs.snowleopard.ai/cloud/getting-started#api-keys)
- OpenAI API key

## HOW TO USE THE CODE

1. Create a [Snow Leopard Cloud](https://cloud.snowleopard.ai) instance, connect a data source, and note the instance ID from the instance's **Connection Info** tab. See the [Cloud getting started guide](https://docs.snowleopard.ai/cloud/getting-started) for details.
   - Don't have data? Load the [sample Northwind dataset](https://github.com/SnowLeopard-AI/northwind_psql) into a PostgreSQL database that Snow Leopard Cloud can reach, such as a hosted [Neon](https://neon.com) or [Supabase](https://supabase.com) database. Run the dataset's `northwind.sql` script against your database, then [add the database as a data source](https://docs.snowleopard.ai/cloud/getting-started#adding-a-data-source) in your instance.

2. Set environment variables:
   export SNOWLEOPARD_API_KEY="your-api-key"
   export SNOWLEOPARD_INSTANCE_ID="your-instance-id"
   export OPENAI_API_KEY="your-openai-key"

3. Install dependencies:
   ```
   pip install langgraph langchain langchain-openai snowleopard python-dotenv
   ```

4. Run the script:
   ```shell
   cd quickstart/langgraph/
   python langgraph_quickstart.py
   ```

5. Expected output:
   Question: What data is available in the database?
   
   ```
   ============================================================
   STEP 1: Database Query Result
   ============================================================
   Generated SQL: SELECT * FROM ...
   Rows returned: 5
   Sample data: {...}
   Summary: The database contains...
   
   STEP 2: Final Answer
   ============================================================
   Based on the database query, here's what's available...
   ```

6. Customize by changing the question in main():
   question = "What are the top 5 products by revenue?"

7. Add more nodes to extend the workflow:
   workflow.add_node("validate", validate_results)
   workflow.add_edge("analyze", "validate")

---
