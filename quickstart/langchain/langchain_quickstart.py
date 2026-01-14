"""
LangChain + SnowLeopard - Simple Quick Start Guide

This is an integration example of SnowLeopard with LangChain.
"""

import os
import sys
from langchain_core.tools import Tool
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from snowleopard import SnowLeopardClient


# ============================================================================
# STEP 1: Create SnowLeopard Tool
# ============================================================================

def create_snowleopard_tool():
    """Create a SnowLeopard tool that LangChain can use."""
    client = SnowLeopardClient(api_key=os.getenv("SNOWLEOPARD_API_KEY"))
    
    def query_data(natural_language_query: str) -> str:
        """Query your database using natural language."""
        response = client.retrieve(
            datafile_id=os.getenv("SNOWLEOPARD_DATAFILE_ID"),
            user_query=natural_language_query
        )
        
        # Check response status
        if response.responseStatus != "SUCCESS":
            return f"Error: {response.responseStatus}"
        
        # Extract data from response
        if not response.data:
            return "No data found"
        
        data_item = response.data[0]
        
        # Format results
        results = []
        results.append(f"SQL Query: {data_item.query}")
        results.append(f"Rows: {len(data_item.rows)}")
        
        if data_item.rows:
            results.append(f"Data: {data_item.rows[:3]}")  # First 3 rows
        
        if data_item.querySummary:
            results.append(f"Summary: {data_item.querySummary}")
        
        return "\n".join(results)
    
    return Tool(
        name="query_database",
        func=query_data,
        description="Query your database with natural language questions"
    )


# ============================================================================
# STEP 2: Create LangChain Agent
# ============================================================================

def create_agent():
    """Create a simple LangChain agent with SnowLeopard tool."""
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    tools = [create_snowleopard_tool()]
    
    # ReAct prompt format (required for this agent type)
    prompt = PromptTemplate.from_template("""
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
""")
    
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )
    
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True,
    )
    
    return agent_executor


# ============================================================================
# STEP 3: Use the Agent
# ============================================================================

def main():
    """Run the agent with a sample query."""
    # Check credentials
    if not os.getenv("SNOWLEOPARD_API_KEY"):
        print("Error: Set SNOWLEOPARD_API_KEY environment variable")
        return
    
    if not os.getenv("SNOWLEOPARD_DATAFILE_ID"):
        print("Error: Set SNOWLEOPARD_DATAFILE_ID environment variable")
        return
    
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: Set OPENAI_API_KEY environment variable")
        return
    
    # Create agent
    print("Creating LangChain agent with SnowLeopard...")
    agent = create_agent()
    
    # Ask a question
    query = "What data is in the database? Show me a summary."
    print(f"\nQuery: {query}\n")
    
    try:
        result = agent.invoke({"input": query})
        print("\n" + "="*60)
        print("FINAL ANSWER:")
        print("="*60)
        print(result["output"])
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


# ============================================================================
# Usage
# ============================================================================

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    main()
