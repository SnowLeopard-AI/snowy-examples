# LangGraph Snowleopard AI Quick Start Guide


## HOW TO USE THE CODE

1. Set environment variables:
   export SNOWLEOPARD_API_KEY="your-api-key"
   export SNOWLEOPARD_DATAFILE_ID="your-datafile-id"
   export OPENAI_API_KEY="your-openai-key"

2. Install dependencies:
   ```
   pip install langgraph langchain langchain-openai snowleopard python-dotenv
   ```

3. Run the script:
   ```shell
   cd langgraph-quickstart
   python langgraph_quickstart.py
   ```

4. Expected output:
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

5. Customize by changing the question in main():
   question = "What are the top 5 products by revenue?"

6. Add more nodes to extend the workflow:
   workflow.add_node("validate", validate_results)
   workflow.add_edge("analyze", "validate")

---
