"""
Snow Leopard Tool - wrapper for the Snow Leopard Cloud retrieve API
"""

import logging
import os
import time
from typing import Dict, Any
import json

from snowleopard import SnowLeopardClient
from snowleopard.models import APIError, ErrorSchemaData

logger = logging.getLogger(__name__)

_client = None


def get_client() -> SnowLeopardClient:
    """Get or create Snow Leopard client"""
    global _client

    if _client is None:
        api_key = os.getenv('SNOWLEOPARD_API_KEY')
        if not api_key:
            raise ValueError("SNOWLEOPARD_API_KEY not set")

        _client = SnowLeopardClient(api_key=api_key)
        logger.info("[Snow Leopard] Client initialized")

    return _client


def query_snowleopard(query: str) -> Dict[str, Any]:
    """Query Snow Leopard for financial data
    
    Args:
        query: User's natural language query
        
    Returns:
        Dict with keys: success, rows, sql, execution_time_ms, message/error
    """
    try:
        start_time = time.time()
        client = get_client()
        instance_id = os.getenv('SNOWLEOPARD_INSTANCE_ID')
        
        if not instance_id:
            raise ValueError("SNOWLEOPARD_INSTANCE_ID not set")
        
        logger.info(f"[Snowleopard] Query: {query[:80]}...")
        
        # Ask the Snow Leopard Cloud instance to answer the question against its data source
        result = client.retrieve(instance_id=instance_id, user_query=query)
        execution_time = round((time.time() - start_time) * 1000)
        
        if isinstance(result, APIError):
            raise RuntimeError(f"{result.responseStatus}: {result.description}")
        if not result.data:
            raise RuntimeError("Snow Leopard returned no data")
        
        # The last data item holds the final query; earlier items are intermediate steps
        data = result.data[-1]
        if isinstance(data, ErrorSchemaData):
            raise RuntimeError(f"query failed: {data.error} (sql: {data.query})")
        
        rows = data.rows or []
        sql = data.query or ''
        
        logger.info(f"[Snow Leopard] ✓ Extracted {len(rows)} rows from SchemaData")
        
        # Debug logging: Show structure of first row if data present
        if rows:
            logger.debug(f"[Snow Leopard] Response type: {type(rows)}")
            first_row = rows[0] if isinstance(rows, list) and rows else None
            
            if first_row and isinstance(first_row, dict):
                logger.debug(f"[Snow Leopard] Row keys: {list(first_row.keys())}")
                logger.debug(f"[Snow Leopard] Sample row: {json.dumps(first_row, indent=2, default=str)}")
            elif first_row:
                logger.debug(f"[Snow Leopard] Row content: {first_row}")
        
        return {
            'success': True,
            'rows': rows,
            'sql': sql,
            'execution_time_ms': execution_time,
            'message': ''
        }
    
    except Exception as e:
        logger.error(f"[Snow Leopard] ❌ Failed: {str(e)}")
        import traceback
        logger.error(f"[Snow Leopard] Traceback: {traceback.format_exc()}")
        
        return {
            'success': False,
            'error': str(e),
            'rows': [],
            'sql': '',
            'execution_time_ms': 0
        }
