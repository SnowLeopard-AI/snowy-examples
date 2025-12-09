# -*- coding: utf-8 -*-
# copyright 2025 Snow Leopard, Inc - all rights reserved


"""
CLI Formatting utilities for rich console output.
"""


from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from typing import List, Dict, Any

console = Console()

def print_header(text: str):
    """Print application header"""
    console.print(f"\n{text}", style="bold cyan", justify="center")
    console.print("="*60, style="cyan")

def print_result(response_text: str, execution_time_ms: float = None):
    """Print query result"""
    console.print(response_text, style="green")
    
    if execution_time_ms:
        console.print(f"⏱️  Executed in {execution_time_ms:.2f}ms", style="dim yellow")

def print_error(error_text: str):
    """Print error message"""
    console.print(f"❌ {error_text}", style="red")

def print_debug_sql(sql: str):
    """Print generated SQL in syntax-highlighted format"""
    syntax = Syntax(sql, "sql", theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title="Generated SQL", expand=False))

def print_metrics_table(metrics: Dict[str, Any]):
    """Print metrics in a nice table"""
    
    table = Table(title="📊 Query Metrics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    for key, value in metrics.items():
        # Format key for display
        display_key = key.replace('_', ' ').title()
        
        # Format value
        if isinstance(value, float):
            display_value = f"{value:.2f}"
        else:
            display_value = str(value)
        
        table.add_row(display_key, display_value)
    
    console.print(table)

def print_transactions_table(transactions: List[Dict]):
    """Print transactions in a table"""
    
    if not transactions:
        console.print("No transactions found", style="yellow")
        return
    
    table = Table(title="💳 Recent Transactions")
    table.add_column("Date", style="cyan")
    table.add_column("Merchant", style="magenta")
    table.add_column("Category", style="blue")
    table.add_column("Amount", style="green", justify="right")
    
    for tx in transactions[:10]:  # Show first 10
        table.add_row(
            tx.get('transaction_date', 'N/A'),
            tx.get('merchant_name', 'N/A'),
            tx.get('category_name', 'N/A'),
            f"${tx.get('amount', 0):.2f}"
        )
    
    console.print(table)
