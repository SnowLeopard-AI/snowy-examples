# -*- coding: utf-8 -*-
# copyright 2025 Snow Leopard, Inc - all rights reserved


"""
Modern Memory Manager for Financial Coach

Uses LangGraph state directly (no deprecated ConversationSummaryMemory).
Simply tracks conversation history and preferences.
"""


import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)

class MemoryManager:
    """
    Simple memory manager using state-based approach (LangGraph pattern).
    No deprecated ConversationSummaryMemory - just pure conversation tracking.
    """
    
    def __init__(self, memory_type: str = 'state'):
        self.memory_type = memory_type  # 'state' (no LangChain memory objects)
        self.user_preferences = {}
        self.conversation_history = []
        self.initialized = True  # Always initialized (no external deps)
        
        logger.info("="*60)
        logger.info("[MemoryManager] Initialized (state-based, no ConversationSummaryMemory)")
        logger.info("="*60)
    
    def add_message(self, query: str, response: str, metadata: Optional[Dict] = None) -> bool:
        """
        Add a message to conversation history.
        
        This is now simple - just stores the message and metadata.
        No LLM calls, no deprecation warnings.
        """
        try:
            # Store message
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'query': query,
                'response': response,
                'metadata': metadata or {}
            })
            
            # Extract and cache user preferences
            if metadata:
                self._update_preferences(metadata)
            
            logger.debug(f"[add_message] ✓ Message #{len(self.conversation_history)} added")
            return True
        
        except Exception as e:
            logger.error(f"[add_message] ❌ Error: {e}")
            return False
    
    def get_context(self) -> Dict[str, Any]:
        """
        Get context from recent messages for query enrichment.
        
        Returns the last few messages for context.
        """
        if not self.conversation_history:
            return {}
        
        # Get last 3 messages for context
        recent = self.conversation_history[-3:] if len(self.conversation_history) >= 3 else self.conversation_history
        
        return {
            'recent_messages': recent,
            'total_messages': len(self.conversation_history),
            'user_preferences': self.user_preferences
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Get conversation summary for display"""
        
        # Calculate unique merchants
        unique_merchants = set()
        for msg in self.conversation_history:
            if 'merchants' in msg.get('metadata', {}):
                for m in msg['metadata'].get('merchants', []):
                    unique_merchants.add(m)
        
        return {
            'total_messages': len(self.conversation_history),
            'unique_merchants': len(unique_merchants),
            'user_preferences': dict(sorted(
                self.user_preferences.items(),
                key=lambda x: x,
                reverse=True
            )[:5]) if self.user_preferences else {},
            'memory_initialized': self.initialized,
            'memory_type': self.memory_type,
            'recent_topics': self._get_recent_topics()
        }
    
    def get_full_history(self) -> List[Dict]:
        """Get full conversation history"""
        return self.conversation_history
    
    def _update_preferences(self, metadata: Dict):
        """Extract and cache user preferences from metadata"""
        try:
            # Track frequently mentioned categories
            if 'category' in metadata:
                category = metadata['category']
                self.user_preferences[category] = self.user_preferences.get(category, 0) + 1
            
            # Track frequently mentioned merchants
            if 'merchants' in metadata:
                for merchant in metadata['merchants']:
                    self.user_preferences[merchant] = self.user_preferences.get(merchant, 0) + 1
        
        except Exception as e:
            logger.debug(f"[_update_preferences] Error: {e}")
    
    def _get_recent_topics(self) -> List[str]:
        """Extract recent topics from conversation"""
        topics = []
        for msg in self.conversation_history[-5:]:  # Last 5 messages
            metadata = msg.get('metadata', {})
            if 'category' in metadata:
                topics.append(metadata['category'])
        
        return list(set(topics))  # Unique topics

# ===== GLOBAL SINGLETON INSTANCE =====

logger.info("[MAIN] Creating global memory_manager instance...")
memory_manager = MemoryManager(memory_type='state')
logger.info(f"[MAIN] memory_manager initialized: {memory_manager.initialized}")
