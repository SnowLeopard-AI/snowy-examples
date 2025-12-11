"""
Metrics tracking for debugging and performance analysis.
"""


from datetime import datetime
from typing import List, Dict, Any
from rich.table import Table
from rich.console import Console
import statistics

console = Console()

class MetricsTracker:
    """Track API calls, execution times, and query performance."""
    
    def __init__(self):
        self.calls: List[Dict[str, Any]] = []
        self.call_count = 0
    
    def record_query(self, query: str, response: Dict, context: Dict = None):
        """Record a single query execution"""
        
        self.call_count += 1
        
        call_entry = {
            'call_id': self.call_count,
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'context': context or {},
            'execution_time_ms': response.get('execution_time_ms', 0),
            'rows_returned': response.get('rows_returned', 0),
            'sql_generated': response.get('sql', ''),
            'success': response.get('success', True),
            'response_preview': response.get('response', '')[:100]
        }
        
        self.calls.append(call_entry)
    
    def print_summary(self):
        """Print summary of all queries"""
        
        if not self.calls:
            console.print("No queries recorded", style="yellow")
            return
        
        console.print("\n" + "="*80)
        console.print("📊 METRICS SUMMARY", style="bold cyan", justify="center")
        console.print("="*80)
        
        # Statistics
        successful = [c for c in self.calls if c['success']]
        times = [c['execution_time_ms'] for c in successful]
        
        console.print(f"\nTotal Queries: {self.call_count}")
        console.print(f"Successful: {len(successful)}")
        console.print(f"Failed: {self.call_count - len(successful)}")
        
        if times:
            console.print(f"\nExecution Times:")
            console.print(f"  • Min: {min(times):.2f}ms")
            console.print(f"  • Max: {max(times):.2f}ms")
            console.print(f"  • Avg: {statistics.mean(times):.2f}ms")
            console.print(f"  • Median: {statistics.median(times):.2f}ms")
        
        # Rows retrieved
        total_rows = sum(c.get('rows_returned', 0) for c in successful)
        console.print(f"\nTotal Rows Retrieved: {total_rows}")
        
        # Table of recent queries
        console.print("\n" + "="*80)
        console.print("Recent Queries:", style="bold")
        console.print("="*80)
        
        table = Table()
        table.add_column("#", style="cyan")
        table.add_column("Query", style="magenta")
        table.add_column("Time (ms)", style="green", justify="right")
        table.add_column("Rows", style="blue", justify="right")
        
        for call in self.calls[-10:]:  # Last 10
            table.add_row(
                str(call['call_id']),
                call['query'][:40] + "...",
                f"{call['execution_time_ms']:.2f}",
                str(call['rows_returned'])
            )
        
        console.print(table)
        console.print("="*80 + "\n")
