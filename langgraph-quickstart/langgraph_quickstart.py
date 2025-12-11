"""
LangGraph + SnowLeopard - Simple Quick Start Guide

This is an integration example of SnowLeopard with LangGraph.
"""

import os
import sys
from typing import Any
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from snowleopard import SnowLeopardPlaygroundClient



# ============================================================================
# STEP 1: Define Graph State
# ============================================================================

class GraphState(TypedDict):
    """State that flows through the graph."""
    user_question: str
    query_result: str
    final_answer: str


# ============================================================================
# STEP 2: Create SnowLeopard Client
# ============================================================================

from dotenv import load_dotenv
load_dotenv()

snowleopard_client = SnowLeopardPlaygroundClient(
    api_key=os.getenv("SNOWLEOPARD_API_KEY")
)


# ============================================================================
# STEP 3: Define Graph Nodes
# ============================================================================

def query_database(state: GraphState) -> GraphState:
    """Node 1: Query the database using SnowLeopard."""
    question = state["user_question"]
    
    # Call SnowLeopard API
    response = snowleopard_client.retrieve(
        datafile_id=os.getenv("SNOWLEOPARD_DATAFILE_ID"),
        user_query=question
    )
    
    # Process response
    if response.responseStatus != "SUCCESS":
        state["query_result"] = f"Error: {response.responseStatus}"
        return state
    
    if not response.data:
        state["query_result"] = "No data found"
        return state
    
    # Extract data using snowleopard.models dataclasses
    data_item = response.data[0]
    
    result_lines = [
        f"Generated SQL: {data_item.query}",
        f"Rows returned: {len(data_item.rows)}",
    ]
    
    if data_item.rows:
        result_lines.append(f"Sample data: {data_item.rows[0]}")
    
    if data_item.querySummary:
        result_lines.append(
            f"Summary: {data_item.querySummary}"
        )
    
    state["query_result"] = "\n".join(result_lines)
    return state


def analyze_and_answer(state: GraphState) -> GraphState:
    """Node 2: Use LLM to analyze results and provide final answer."""
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    prompt = f"""
You have the following database query result:

{state["query_result"]}

Original question: {state["user_question"]}

Provide a clear, business-friendly answer based on this data.
"""
    
    message = HumanMessage(content=prompt)
    response = llm.invoke([message])
    
    state["final_answer"] = response.content
    return state


# ============================================================================
# STEP 4: Build Graph
# ============================================================================

def create_graph():
    """Create and return the LangGraph workflow."""
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("query", query_database)
    workflow.add_node("analyze", analyze_and_answer)
    
    # Add edges (query → analyze → end)
    workflow.add_edge("query", "analyze")
    workflow.add_edge("analyze", END)
    
    # Set entry point
    workflow.set_entry_point("query")
    
    return workflow.compile()


# ============================================================================
# STEP 5: Use the Graph
# ============================================================================

def main():
    """Run the LangGraph workflow with a sample question."""
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
    
    # Create the graph
    print("Creating LangGraph workflow with SnowLeopard...\n")
    graph = create_graph()
    
    # Run the graph
    question = "What data is available in the database?"
    print(f"Question: {question}\n")
    print("="*60)
    
    try:
        result = graph.invoke({
            "user_question": question,
            "query_result": "",
            "final_answer": ""
        })
        
        print("STEP 1: Database Query Result")
        print("-"*60)
        print(result["query_result"])
        
        print("\n\nSTEP 2: Final Answer")
        print("-"*60)
        print(result["final_answer"])
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


# ============================================================================
# Usage
# ============================================================================

if __name__ == "__main__":
    main()
