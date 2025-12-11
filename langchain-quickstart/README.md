# LangChain Snowleopard AI Quick Start Guide


## HOW TO USE THE CODE
1. Set environment variables:
   export SNOWLEOPARD_API_KEY="your-api-key"
   export SNOWLEOPARD_DATAFILE_ID="your-datafile-id"
   export OPENAI_API_KEY="your-openai-key"

2. Install dependencies:
   pip install langchain langchain-openai snowleopard python-dotenv

3. Run the script:
   ```shell
   cd langchain-quickstart
   python langchain_quickstart.py
   ```

4. Expected output:
   ```
   > Entering new AgentExecutor...
   Thought: I need to query the database...
   Action: query_database
   Action Input: What data is in the database?
   Observation: [data results]
   Final Answer: [summary]
   ```

5. Customize by changing the query in main():
   query = "What are the top 5 customers by revenue?"

---
