"""
Financial Coach Agent - LangGraph Implementation

Multi-node agent that:
1. Enriches user queries with context
2. Queries Snow Leopard for financial data
3. Analyzes data and generates coaching insights
4. Formats response with recommendations
"""

import logging
import os
from typing import Dict, Any
from datetime import datetime

from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field

from tools.snowleopard_tool import query_snowleopard
from agents.coaching_analyzer import coaching_analyzer
from utils.memory_manager import memory_manager

logger = logging.getLogger(__name__)

# ===== STATE DEFINITION =====

class FinancialCoachState(BaseModel):
    """State schema for the financial coach agent"""
    current_query: str = Field(description="Current user query")
    conversation_turn: int = Field(default=0, description="Conversation turn number")
    messages: list = Field(default_factory=list, description="Conversation history")

    # Query enrichment
    enriched_query: str = Field(default="", description="Enriched version of query")
    analysis_context: Dict[str, Any] = Field(default_factory=dict, description="Query context")

    # Snow Leopard response
    snowleopard_response: Dict[str, Any] = Field(default_factory=dict, description="Raw response from Snow Leopard SDK")

    # Coaching insights
    coaching_insights: Dict[str, Any] = Field(default_factory=dict, description="Coaching analysis and recommendations")

    # Formatted response
    formatted_response: str = Field(default="", description="Final formatted response for user")

    # Metadata
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())

# ===== NODE DEFINITIONS =====

def enrich_query_node(state: FinancialCoachState) -> Dict:
    """
    Node 1: Enrich the user query with context
    Adds context about time period, categories, merchants, etc.
    """
    logger.info(f"[Turn {state.conversation_turn}] Enriching query: {state.current_query}")

    query = state.current_query.lower()
    context = {
        'has_date': any(word in query for word in ['month', 'week', 'year', 'quarter', 'last']),
        'has_category': any(word in query for word in ['category', 'categories', 'spending']),
        'has_merchant': any(word in query for word in ['merchant', 'where', 'store', 'restaurant']),
        'query_type': 'unknown'
    }

    # Determine query type
    if context['has_category']:
        context['query_type'] = 'category_analysis'
    elif context['has_merchant']:
        context['query_type'] = 'merchant_analysis'
    elif context['has_date']:
        context['query_type'] = 'trend_analysis'

    return {
        'enriched_query': state.current_query,
        'analysis_context': context
    }


def query_snowleopard_node(state: FinancialCoachState) -> Dict:
    """
    Node 2: Query Snow Leopard for financial data
    Uses the enriched query to get relevant financial data
    """
    logger.info(f"[Turn {state.conversation_turn}] Querying with Snow Leopard")

    # Query Snow Leopard
    response = query_snowleopard(state.current_query)

    if response.get('success'):
        logger.info(f"✓ Snow Leopard returned {len(response.get('rows', []))} rows in {response.get('execution_time_ms')}ms")
    else:
        logger.warning(f"⚠️ Snow Leopard query failed: {response.get('error')}")

    return {
        'snowleopard_response': response
    }


def analyze_and_coach_node(state: FinancialCoachState) -> Dict:
    """
    Node 3: Analyze financial data and generate coaching insights
    Transforms raw Snow Leopard SDK response into:
    - Financial analysis
    - Pattern recognition
    - Actionable recommendations
    - Follow-up questions
    """
    logger.info(f"[Turn {state.conversation_turn}] Analyzing and coaching")

    response = state.snowleopard_response

    if not response.get('success'):
        logger.warning("Skipping coaching analysis - no successful data")
        return {'coaching_insights': {}}

    rows = response.get('rows', [])

    # Use coaching analyzer
    coaching_insights = coaching_analyzer.analyze(
        rows=rows,
        query=state.current_query,
        analysis_context=state.analysis_context
    )

    if coaching_insights.get('insights'):
        logger.info(f"✓ Generated {len(coaching_insights.get('insights', []))} insights")

    return {
        'coaching_insights': coaching_insights
    }


def format_response_node(state: FinancialCoachState) -> Dict:
    """
    Node 4: Format response with coaching insights
    Combines raw data with coaching to create engaging, actionable response
    """
    logger.info(f"[Turn {state.conversation_turn}] Formatting response")

    response_data = state.snowleopard_response
    coaching = state.coaching_insights

    # Build formatted response
    lines = []

    # Add section header
    lines.append("")
    lines.append("🤖 ╔" + "═" * 58 + "╗")
    lines.append("   ║           💡 FINANCIAL COACHING INSIGHTS                 ║")
    lines.append("   ╚" + "═" * 58 + "╝")
    lines.append("")

    # Add coaching insights
    if coaching.get('insights'):
        lines.append("📊 YOUR SPENDING ANALYSIS")
        lines.append("─" * 62)
        for insight in coaching['insights']:
            lines.append(f"  {insight}")
        lines.append("")

    # Add recommendations
    if coaching.get('recommendations'):
        lines.append("💡 RECOMMENDATIONS FOR YOU")
        lines.append("─" * 62)
        for i, rec in enumerate(coaching['recommendations'], 1):
            # Wrap long text
            lines.append(f"  {i}. {rec}")
        lines.append("")

    # Add follow-up questions
    if coaching.get('follow_up_questions'):
        lines.append("❓ LET'S DIVE DEEPER")
        lines.append("─" * 62)
        for i, q in enumerate(coaching['follow_up_questions'], 1):
            lines.append(f"  {i}. {q}")
        lines.append("")

    # Add total opportunity (savings potential)
    if coaching.get('total_opportunity', 0) > 0:
        lines.append("🎯 YOUR SAVINGS OPPORTUNITY")
        lines.append("─" * 62)
        lines.append(f"  💰 Total Potential Savings: ${coaching['total_opportunity']:,.0f}/month")
        lines.append("")

    # Add execution metrics
    execution_time = response_data.get('execution_time_ms')
    if execution_time:
        lines.append("⏱️  QUERY PERFORMANCE")
        lines.append("─" * 62)
        lines.append(f"  Executed in {execution_time:.0f}ms")
        lines.append("")

    # Add SQL if in debug mode
    if os.getenv('DEBUG', 'False').lower() == 'true':
        if response_data.get('sql'):
            lines.append("📋 GENERATED SQL")
            lines.append("─" * 62)
            # Format SQL with indentation
            sql_lines = response_data['sql'].split('\n')
            for sql_line in sql_lines:
                lines.append(f"  {sql_line}")
            lines.append("")

    formatted_response = "\n".join(lines)

    # Update messages
    messages = state.messages.copy() if state.messages else []
    messages.append({
        'turn': state.conversation_turn,
        'role': 'user',
        'content': state.current_query
    })
    messages.append({
        'turn': state.conversation_turn,
        'role': 'assistant',
        'content': formatted_response
    })

    # Add to memory
    if memory_manager and memory_manager.initialized:
        memory_manager.add_message(
            query=state.current_query,
            response=formatted_response,
            metadata=state.analysis_context
        )

    logger.debug(f"Message added to memory (turn {state.conversation_turn})")

    return {
        'formatted_response': formatted_response,
        'messages': messages,
        'conversation_turn': state.conversation_turn + 1,
        'updated_at': datetime.now().isoformat()
    }


# ===== LANGGRAPH COMPILATION =====

def create_financial_coach_graph():
    """Create and compile the LangGraph agent"""
    logger.info("Creating Financial Coach LangGraph...")

    # Create workflow
    workflow = StateGraph(FinancialCoachState)

    # Add nodes
    workflow.add_node("enrich", enrich_query_node)
    workflow.add_node("query_snowleopard", query_snowleopard_node)
    workflow.add_node("analyze_and_coach", analyze_and_coach_node)
    workflow.add_node("format_response", format_response_node)

    # Define edges
    workflow.add_edge(START, "enrich")
    workflow.add_edge("enrich", "query_snowleopard")
    workflow.add_edge("query_snowleopard", "analyze_and_coach")
    workflow.add_edge("analyze_and_coach", "format_response")
    workflow.add_edge("format_response", END)

    # Compile
    app = workflow.compile()

    logger.info("✓ Financial Coach LangGraph compiled")
    return app


# Create the agent graph
coach_graph = create_financial_coach_graph()


# ===== APPLICATION BUILDERS =====

def build_financial_coach_app():
    """Build and return the financial coach application"""
    return coach_graph


def invoke_financial_coach(app, user_query: str, session_id: str, conversation_turn: int):
    """Invoke the financial coach with a user query"""
    logger.info(f"Invoking financial coach: {user_query}")

    # Create initial state
    initial_state = FinancialCoachState(
        current_query=user_query,
        conversation_turn=conversation_turn,
        messages=[]
    )

    # Invoke the graph
    result = app.invoke(initial_state)
    
    logger.info(f"Financial coach invoked with result: {result}")

    # Convert result to dict for JSON serialization
    return {
        'current_query': result.get('current_query', ''),
        'enriched_query': result.get('enriched_query', ''),
        'analysis_context': result.get('analysis_context', {}),
        'snowleopard_response': result.get('snowleopard_response', {}),
        'coaching_insights': result.get('coaching_insights', {}),
        'formatted_response': result.get('formatted_response', ''),
        'messages': result.get('messages', []),
        'conversation_turn': result.get('conversation_turn', conversation_turn),
        'updated_at': result.get('updated_at', '')
    }
