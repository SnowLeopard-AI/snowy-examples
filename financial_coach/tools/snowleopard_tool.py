# -*- coding: utf-8 -*-
# copyright 2025 Snow Leopard, Inc - all rights reserved

"""
Snowleopard Tool - wrapper for Snowleopard Playground API
"""

import logging
import os
import time
from typing import Dict, Any
import json

from snowleopard import SnowLeopardPlaygroundClient

logger = logging.getLogger(__name__)

_client = None


def get_client() -> SnowLeopardPlaygroundClient:
    """Get or create Snowleopard client"""
    global _client
    
    if _client is None:
        api_key = os.getenv('SNOWLEOPARD_API_KEY')
        if not api_key:
            raise ValueError("SNOWLEOPARD_API_KEY not set")
        
        _client = SnowLeopardPlaygroundClient(api_key=api_key)
        logger.info("[Snowleopard] Client initialized")
    
    return _client


def query_snowleopard(query: str) -> Dict[str, Any]:
    """Query Snowleopard for financial data
    
    Args:
        query: User's natural language query
        
    Returns:
        Dict with keys: success, rows, sql, execution_time_ms, message/error
    """
    try:
        start_time = time.time()
        client = get_client()
        datafile_id = os.getenv('SNOWLEOPARD_DATAFILE_ID')
        
        if not datafile_id:
            raise ValueError("SNOWLEOPARD_DATAFILE_ID not set")
        
        logger.info(f"[Snowleopard] Query: {query[:80]}...")
        
        # Call Snowleopard API with correct parameter names
        result = client.retrieve(datafile_id=datafile_id, user_query=query)
        
        # ✅ FIXED: Extract SchemaData object attributes cleanly
        # Result is guaranteed to be a SchemaData object from Snowleopard API
        # Use getattr() to safely extract attributes with fallbacks
        
        response_status = getattr(result, 'responseStatus', '')
        rows = getattr(result.data[0], 'rows', [])
        sql = getattr(result.data[0], 'query', '')
        execution_time = round((time.time() - start_time) * 1000)
        
        logger.info(f"[Snowleopard] ✓ Extracted {len(rows)} rows from SchemaData")
        
        # Debug logging: Show structure of first row if data present
        if rows:
            logger.debug(f"[Snowleopard] Response type: {type(rows)}")
            first_row = rows[0] if isinstance(rows, list) and rows else None
            
            if first_row and isinstance(first_row, dict):
                logger.debug(f"[Snowleopard] Row keys: {list(first_row.keys())}")
                logger.debug(f"[Snowleopard] Sample row: {json.dumps(first_row, indent=2, default=str)}")
            elif first_row:
                logger.debug(f"[Snowleopard] Row content: {first_row}")
        
        return {
            'success': True,
            'rows': rows,
            'sql': sql,
            'execution_time_ms': execution_time,
            'message': ''
        }
    
    except Exception as e:
        logger.error(f"[Snowleopard] ❌ Failed: {str(e)}")
        import traceback
        logger.error(f"[Snowleopard] Traceback: {traceback.format_exc()}")
        
        return {
            'success': False,
            'error': str(e),
            'rows': [],
            'sql': '',
            'execution_time_ms': 0
        }
