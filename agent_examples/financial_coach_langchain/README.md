# 💰 SnowleopardAI Financial Coach

A LangGraph-based financial coaching CLI agent that analyzes personal spending data through natural language queries. Uses SnowleopardAI to convert your questions into SQL, executes them against your SQLite dataset, and returns AI-powered financial coaching insights.

---

## 📊 Table of Contents

1. [Quick Start](#quick-start)
2. [Dataset Setup](#dataset-setup)
3. [Environment Configuration](#environment-configuration)
4. [Project Structure](#project-structure)
5. [How to Run](#how-to-run)
6. [How to Debug](#how-to-debug)
7. [Data Transformation Pipeline](#data-transformation-pipeline)
8. [Security Notes](#security-Notes)

---

## 🚀 Quick Start

### In 5 Minutes

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy and fill .env
cp .env.example .env
# Edit .env with your Snowleopard API key & datafile ID

# 3. Create sample dataset
python data/create_sample_data.py

# 4. Run the app
python main.py

# 5. Try a query
You: Show me my spending by category
```

---

## 📦 Dataset Setup

### Overview

#### Step 1: Prepare your SQLite database

This application expects a **SQLite database** with financial transaction data. You have two options:

1. **Use the sample dataset generator** (easiest - includes sample data)
    1. Generate Sample Dataset
    ```bash
    python data/create_sample_data.py
    ```
    This generates `financial_data.db` with sample transactions from the past 6 months

2. **Use the sample dataset** (personal_finance.db, included in repo. Download data from (Kaggle)[https://www.kaggle.com/datasets/entrepreneurlife/personal-finance/data])
    1. Use the provided `personal_finance.db` file or download from Kaggle (https://www.kaggle.com/datasets/entrepreneurlife/personal-finance/data) and run `data/transform_personal_finance.py`

#### Step 2: Upload to SnowleopardAI Playground

1. Go to http://try.snowleopard.ai
2. **"Create New Datafile"** → Select `financial_data.db`
3. Give it a name: `"Personal Finance Data"`
4. Click **"Upload"** and wait for processing
5. Copy the generated **Datafile ID** (looks like `datafile_xxx`)
6. Paste into `.env`:
   ```bash
   SNOWLEOPARD_DATAFILE_ID=datafile_xxx
   ```
---

## 🔧 Environment Configuration

### Step 1: Copy Template

```bash
cp .env.example .env
```

### Step 2: Fill Your Credentials

Edit `.env`:

```bash
# SnowleopardAI API Credentials
SNOWLEOPARD_API_KEY=sk-proj-abc123...          # Your Snowleopard API key
SNOWLEOPARD_DATAFILE_ID=datafile_xyz789        # Your uploaded datafile ID

# Debugging (optional)
DEBUG=False                                    # Set to True for verbose logs
```

#### How to Get Credentials

1. **API Key:**
   - Sign up at https://www.snowleopard.ai
   - Go to **Account Settings** → **API Keys**
   - Copy your API key
   - Paste into `.env`

2. **Datafile ID:**
   - Upload your SQLite to Playground (see Dataset Setup)
   - On the datafile row, click **"Copy ID"**
   - Paste into `.env`

---

## 📁 Project Structure

```
financial-coach/
├── main.py                      # Entry point (CLI)
│
├── agents/
│   ├── financial_coach.py       # LangGraph workflow (4 nodes)
│   └── coaching_analyzer.py     # Analysis engine (insights + recs)
│
├── tools/
│   └── snowleopard_tool.py      # API integration
│
├── utils/
│   ├── memory_manager.py        # Conversation memory
│   ├── cli_formatter.py         # Rich CLI output
│   ├── metrics.py               # Performance tracking
│   └── schemas.py               # Pydantic models
│
├── models/
│   └── schemas.py               # Pydantic models
│
└── data/
    └── create_sample_data.py    # Generate sample dataset
    └── financial_data.db            # Sample SQLite (generated)
    ...
```

---

## 🏃 How to Run

### Basic Startup

```bash
python main.py
```

You should see:

```
💰 ╔════════════════════════════════════════╗
   ║ SnowleopardAI Financial Coach          ║ 
   ╚════════════════════════════════════════╝

Powered by SnowleopardAI, LangGraph, and real personal finance data

✓ Ready to help with your finances!

Commands:
 • Type your question to ask about your finances
 • Type 'memory' or 'summary' to see conversation summary
 • Type 'debug' to see query metrics
 • Type 'quit' or 'exit' to close

============================================================

You:
```

### Example Usage

**Query: Spending by Category**

```
You: Show me my spending by category
```

**Response:**

```
🤖 
╔════════════════════════════════════════════════╗
║ 💡 FINANCIAL COACHING INSIGHTS                 ║
╚════════════════════════════════════════════════╝

📊 YOUR SPENDING ANALYSIS
────────────────────────────────────────────────────
 💰 Real Monthly Spending: $2,543.22 (excluding transfers)
 🔴 Highest Expense: Rent @ $1,200.00 (47.2% of total)
 💡 Found 3 optimization opportunities totaling $425/month
 🟡 Monitor: Dining at 8.2% - watch for growth

💡 RECOMMENDATIONS FOR YOU
────────────────────────────────────────────────────
 1. Your Rent is your largest expense (47.2%). This should be priority #1.
 2. Meal prep 2x/week could save $127/month (Highest impact)
 3. Optimization could save $85/month

❓ LET'S DIVE DEEPER
────────────────────────────────────────────────────
 1. Is your Rent spending one-time or recurring?
 2. Which of these 3 opportunities interests you most?
 3. Should we create a monthly savings goal based on these opportunities?

🎯 YOUR SAVINGS OPPORTUNITY
────────────────────────────────────────────────────
 💰 Total Potential Savings: $425/month

⏱️ Executed in 145ms
```

---

### CLI Commands

| Command | Action |
|---------|--------|
| Natural language query | Ask about your finances |
| `memory` / `summary` | Show conversation memory |
| `debug` | Show query metrics (time, rows) |
| `help` | Print example queries |
| `quit` / `exit` | Exit app |

---

## 🐛 How to Debug

### Enable Debug Logging

Set `DEBUG=True` in `.env`:

```bash
DEBUG=True
```

### View Generated SQL

With `DEBUG=True`, the generated SQL is shown after each query:

```
📋 GENERATED SQL
────────────────────────────────────────────────────────────────────────────
SELECT
  category_name,
  SUM(amount) as total_spending
FROM transactions
WHERE transaction_date >= date('now', '-30 days')
GROUP BY category_name
ORDER BY total_spending DESC
```

---

## 🔄 Data Transformation Pipeline

### End-to-End Flow

```
1. USER INPUT (CLI)
   "Show me my spending by category"
            ↓
2. QUERY ENRICHMENT (enrich_query_node)
   Add context: time period, entity type, intent
            ↓
3. SNOWLEOPARD API CALL (query_snowleopard_node)
   User query → LLM → SQL → SQLite execution
   Returns: rows, sql, execution_time_ms
            ↓
4. COACHING ANALYSIS (analyze_and_coach_node)
   Rows → Pattern detection → Insights generation
   Returns: insights, recommendations, opportunities
            ↓
5. RESPONSE FORMATTING (format_response_node)
   Insights → Rich CLI format → User display
            ↓
6. OUTPUT (CLI)
   Beautiful formatted response with sections
```

### Data Transformations

**Stage 1: Query Input**

```python
query = "Show me my spending by category"
```

**Stage 2: Enrichment**

```python
enriched_context = {
    'query_type': 'category_analysis',
    'has_date': False,
    'has_category': True,
    'has_merchant': False
}
```

**Stage 3: SQL Generation**

```sql
SELECT 
  category_name, 
  SUM(amount) as total_spending
FROM transactions
WHERE transaction_date >= date('now', '-30 days')
GROUP BY category_name
ORDER BY total_spending DESC
```

**Stage 4: Raw Results (from SQLite)**

```python
rows = [
    {'category_name': 'Groceries', 'total_spending': 425.50},
    {'category_name': 'Dining', 'total_spending': 180.75},
    {'category_name': 'Fuel', 'total_spending': 165.00},
]
```

**Stage 5: Coaching Analysis**

```python
coaching = {
    'type': 'spending_by_category',
    'total_spending': 771.25,
    'real_spending': 771.25,
    'insights': [
        '💰 Real Monthly Spending: $771.25',
        '🔴 Highest Expense: Groceries @ $425.50 (55.1%)',
        '💡 Found 2 optimization opportunities totaling $127/month'
    ],
    'recommendations': [
        'Your Groceries is your largest expense...',
        'Meal prep 2x/week could save $127/month...'
    ],
    'follow_up_questions': [
        'Is your Groceries spending one-time or recurring?',
        'Which of these opportunities interests you most?'
    ],
    'total_opportunity': 127
}
```

**Stage 6: Formatted Output**

```
📊 YOUR SPENDING ANALYSIS
────────────────────────────────────────────────────
 💰 Real Monthly Spending: $771.25
 🔴 Highest Expense: Groceries @ $425.50 (55.1%)
 💡 Found 2 optimization opportunities totaling $127/month

[... more sections ...]
```

---

## 📝 Example Queries

Try these in the CLI:

### Category Analysis

```
You: Show me my spending by category
You: Break down my spending by category
You: What are my biggest expenses?
```

**Returns:** Category totals, percentages, and recommendations.

### Merchant Analysis

```
You: Which merchants did I spend the most at?
You: Where did I spend the most money?
You: Top spending merchants
```

**Returns:** Merchant breakdown, restaurant vs grocery ratio, insights.

### Trend Analysis

```
You: Show me my spending trends over time
You: Compare this month vs last month
You: Monthly spending breakdown
```

**Returns:** Time-series analysis and growth insights.

### General Insights

```
You: How much did I spend on groceries?
You: Total spending analysis
You: Financial overview
```

**Returns:** Custom analysis based on query.

---

## 🔐 Security Notes

- **Never commit `.env`** → Listed in `.gitignore`
- **API keys only in `.env`** → Not in code
- **Sample data is fake** → Use your own real data
- **Queries go to Snowleopard** → They handle SQL execution
- **No data stored locally** → Stateless per request

---

## 🆘 Troubleshooting

### "SNOWLEOPARD_API_KEY not set"

```bash
# Check .env exists
ls -la .env

# Check it has your key
grep SNOWLEOPARD_API_KEY .env

# If missing, add it:
echo "SNOWLEOPARD_API_KEY=sk-proj-your_key" >> .env
```

### "No rows returned"

```bash
# 1. Enable debug mode
sed -i 's/DEBUG=False/DEBUG=True/' .env

# 2. Run and check logs
python main.py

# 3. Look for: "[Snowleopard] ✓ Extracted N rows"
# If N=0, your datafile might be empty or schema mismatched
```

### "ImportError: No module named 'snowleopard'"

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### "Can't find financial_data.db"

```bash
# Generate sample data
python data/create_sample_data.py

# This creates ./financial_data.db
# Then upload to Snowleopard Playground
```

---

## 📚 Learn More

- **Snowleopard Docs:** https://docs.snowleopard.ai
- **LangGraph Docs:** https://langchain-ai.github.io/langgraph/
- **Pydantic Docs:** https://docs.pydantic.dev/

---

**Happy coaching! 💡**
