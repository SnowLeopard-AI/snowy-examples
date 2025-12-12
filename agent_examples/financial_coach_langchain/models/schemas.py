"""
Pydantic models for type-safe data handling.
These validate all financial data before it's used.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


# ===== Request/Response Models =====


class TransactionDetail(BaseModel):
    """Individual transaction detail"""
    transaction_id: int
    merchant_name: str
    category_name: str
    amount: float = Field(..., ge=0, description="Transaction amount")
    transaction_date: str
    transaction_type: str = Field(..., pattern="^(debit|credit)$")
    account_name: str

class SpendingByCategory(BaseModel):
    """Spending breakdown by category"""
    category_name: str
    total_spent: float = Field(..., ge=0)
    transaction_count: int = Field(..., ge=0)
    avg_transaction: float = Field(..., ge=0)
    percentage_of_total: float = Field(..., ge=0, le=100)

class MonthlySummary(BaseModel):
    """Monthly spending and income summary"""
    month: str
    total_expenses: float = Field(..., ge=0)
    total_income: float = Field(..., ge=0)
    net_cash_flow: float
    transaction_count: int = Field(..., ge=0)
    net_savings_rate: float = Field(..., ge=-100, le=100)

class MerchantAnalysis(BaseModel):
    """Top merchant analysis"""
    merchant_name: str
    category_name: str
    total_spent: float = Field(..., ge=0)
    frequency: int = Field(..., ge=0)
    avg_transaction: float = Field(..., ge=0)

class FinancialInsight(BaseModel):
    """Financial analysis and insights"""
    query: str
    insight_type: str
    response_text: str
    data: Dict
    sql_generated: Optional[str] = None
    execution_time_ms: float = Field(..., ge=0)
    confidence_score: float = Field(..., ge=0, le=1)

class ConversationContext(BaseModel):
    """Multi-turn conversation context"""
    user_id: str
    conversation_turn: int
    current_query: str
    previous_queries: List[str] = []
    inferred_category: Optional[str] = None
    inferred_timeframe: Optional[str] = None
    inferred_merchant: Optional[str] = None
    last_result: Optional[Dict] = None

class SnowleopardResponse(BaseModel):
    """Response from Snow Leopard SDK"""
    success: bool
    data: List[Dict]
    sql: str
    response: str|list
    execution_time_ms: float
    rows_returned: int
