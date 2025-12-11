"""
SnowleopardAI Financial Coach - Main Application

This is the entry point for the conversational financial coach.
It provides a CLI interface where users can ask questions about their finances,
and the app uses SnowleopardAI to generate and execute SQL queries.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from rich.console import Console
from utils.memory_manager import memory_manager
import logging

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO if os.getenv('DEBUG') != 'True' else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Import components
from agents.financial_coach import build_financial_coach_app, invoke_financial_coach
from utils.cli_formatter import print_header, print_result, print_error, print_debug_sql
from utils.metrics import MetricsTracker

console = Console()

# Global state
metrics_tracker = MetricsTracker()
coach_app = None
session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
conversation_turn = 0

def initialize_app():
    """Initialize the financial coach application"""
    print_header("💰 SnowleopardAI Financial Coach")
    console.print("[dim]Powered by SnowleopardAI, LangGraph, and real personal finance data[/dim]\n")

    global coach_app

    try:
        logger.info("Initializing Financial Coach...")
        coach_app = build_financial_coach_app()
        logger.info("✓ Financial Coach initialized")
        console.print("[green]✓ Ready to help with your finances![/green]\n")
        return True

    except Exception as e:
        print_error(f"Failed to initialize: {str(e)}")
        logger.error(f"Initialization failed: {e}", exc_info=True)
        return False

def process_query(user_input: str):
    """Process a user query through the financial coach"""
    global conversation_turn

    # Handle memory commands
    if user_input.lower() in ['memory', 'history', 'summary', 'stats']:
        if memory_manager and memory_manager.initialized:
            summary = memory_manager.get_summary()
            print("\n" + "="*60)
            print("📊 CONVERSATION MEMORY SUMMARY")
            print("="*60)
            print(f"Total exchanges: {summary['total_messages']}")
            print(f"Unique merchants: {summary.get('unique_merchants', 0)}")
            if summary.get('user_preferences'):
                prefs_str = ", ".join([f"{k} ({v})" for k, v in list(summary['user_preferences'].items())[:3]])
                print(f"Top preferences: {prefs_str}")
            print("="*60 + "\n")
        else:
            print("❌ Memory not initialized\n")
        return True

    try:
        logger.info(f"[Turn {conversation_turn}] Processing query: {user_input}")

        # Invoke the coach
        result = invoke_financial_coach(
            coach_app,
            user_query=user_input,
            session_id=session_id,
            conversation_turn=conversation_turn
        )

        # Get response
        response = result.get('formatted_response', 'No response generated')
        snowleopard_response = result.get('snowleopard_response', {})

        # Print response
        print_result(
            response,
            execution_time_ms=snowleopard_response.get('execution_time_ms')
        )

        # Record metrics
        metrics_tracker.record_query(
            query=user_input,
            response=snowleopard_response,
            context=result.get('analysis_context')
        )

        # Show SQL if in debug mode
        if os.getenv('DEBUG', 'False').lower() == 'true':
            if snowleopard_response.get('sql'):
                print_debug_sql(snowleopard_response['sql'])

        conversation_turn += 1
        return True

    except Exception as e:
        print_error(f"Error processing query: {str(e)}")
        logger.error(f"Query processing failed: {e}", exc_info=True)
        return False

def main():
    """Main application loop"""
    # Initialize
    if not initialize_app():
        return 1

    console.print("Commands:")
    console.print(" • Type your question to ask about your finances")
    console.print(" • Type 'memory' or 'summary' to see conversation summary")
    console.print(" • Type 'debug' to see query metrics")
    console.print(" • Type 'quit' or 'exit' to close\n")
    console.print("="*60 + "\n")

    # Main loop
    try:
        while True:
            try:
                # Get user input
                user_input = console.input("[bold cyan]You:[/bold cyan] ").strip()
                if not user_input:
                    continue

                # Handle special commands
                if user_input.lower() in ['quit', 'exit']:
                    console.print("[yellow]Goodbye![/yellow]")
                    break

                if user_input.lower() == 'debug':
                    metrics_tracker.print_summary()
                    continue

                if user_input.lower() == 'help':
                    console.print("""
[bold cyan]Financial Coach Commands:[/bold cyan]
"Show me my spending by category"
"How much did I spend on groceries?"
"Show me my spending trends"
"Which merchants did I spend the most at?"
"Compare my spending this month vs last month"
"What's my biggest expense category?"
"Break down my spending by category"
"Show me transactions from January"

[bold cyan]Special Commands:[/bold cyan]
debug - Show query metrics
help - Show this help
quit/exit - Exit the application
""")
                    continue

                # Process query
                console.print()
                if not process_query(user_input):
                    console.print("[yellow]Try again or type 'help' for assistance[/yellow]")
                console.print()

            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted. Type 'quit' to exit.[/yellow]")
                continue

            except EOFError:
                console.print("\n[yellow]End of input. Goodbye![/yellow]")
                return 0

        return 0

    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
