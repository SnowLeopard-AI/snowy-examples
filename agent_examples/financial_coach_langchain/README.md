# 💰 Snow Leopard Financial Coach

A LangGraph-based financial coaching CLI agent that analyzes personal spending data through natural language queries. Uses Snow Leopard Cloud to convert your questions into SQL, executes them against your PostgreSQL dataset, and returns AI-powered financial coaching insights.

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

# 2. Load the sample dataset into a PostgreSQL database that Snow Leopard Cloud can reach
psql "$DATABASE_URL" -f data/finance_coach.sql

# 3. Attach the database to a Snow Leopard Cloud instance (see Dataset Setup)

# 4. Copy and fill .env
cp .env.example .env
# Edit .env with your Snow Leopard API key & instance ID

# 5. Run the app
python main.py

# 6. Try a query
You: Show me my spending by category
```

---

## 📦 Dataset Setup

### Overview

Snow Leopard Cloud queries a live PostgreSQL (or BigQuery) database, so the dataset ships as a SQL script you load
into a database of your own.

#### Step 1: Get a PostgreSQL database

You need a PostgreSQL database that Snow Leopard Cloud can reach over the internet. A free hosted database on
[Neon](https://neon.com) or [Supabase](https://supabase.com) works well. See
[docs/postgres-setup.md](../../docs/postgres-setup.md) for the details and alternatives.

#### Step 2: Load the sample dataset

The repo includes `data/finance_coach.sql`, built from the
[Kaggle Personal Finance dataset](https://www.kaggle.com/datasets/entrepreneurlife/personal-finance/data):
806 transactions across 22 categories and 65 merchants, normalized into `users`, `accounts`, `categories`,
`merchants`, and `transactions` tables plus three reporting views.

```bash
psql "postgresql://USER:PASSWORD@HOST/DBNAME?sslmode=require" -f data/finance_coach.sql
```

You can also paste the file into your provider's web SQL editor. The script drops and recreates its tables, so it is
safe to re-run.

To regenerate the SQL from the CSV (for example after editing the data), run:

```bash
python data/transform_personal_finance.py
```

#### Step 3: Attach the database to Snow Leopard Cloud

1. Go to https://cloud.snowleopard.ai and create an instance
2. Click **Add Data Source**, pick PostgreSQL (or Neon / Supabase), and enter the database's host, name, username, and password
3. On the **Keys** tab, create an API key and copy it (it is shown only once)
4. On the **Connection Info** tab, copy the instance ID
5. Paste both into `.env`:
   ```bash
   SNOWLEOPARD_API_KEY=...
   SNOWLEOPARD_INSTANCE_ID=...
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
# Snow Leopard Cloud Credentials
SNOWLEOPARD_API_KEY=...                        # API key from your instance's Keys tab
SNOWLEOPARD_INSTANCE_ID=...                    # Instance ID from your instance's Connection Info tab

# Debugging (optional)
DEBUG=False                                    # Set to True for verbose logs
```

#### How to Get Credentials

1. **API Key:**
   - Open your instance at https://cloud.snowleopard.ai
   - Go to the **Keys** tab and click **Create Key**
   - Copy the key when it is shown and paste it into `.env`

2. **Instance ID:**
   - Open your instance's **Connection Info** tab
   - Copy the instance ID and paste it into `.env`

See the [Cloud getting started guide](https://docs.snowleopard.ai/cloud/getting-started) for screenshots.

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
    ├── finance_coach.sql             # Sample dataset (PostgreSQL script)
    ├── transform_personal_finance.py # Regenerates finance_coach.sql from the CSV
    └── personal_finance/             # Source CSV from Kaggle
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

Powered by Snow Leopard, LangGraph, and real personal finance data

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
  c.category_name,
  SUM(t.amount) AS total_spending
FROM transactions t
JOIN categories c ON t.category_id = c.category_id
WHERE t.transaction_type = 'debit'
GROUP BY c.category_name
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
3. SNOW LEOPARD API CALL (query_snowleopard_node)
   User query → Snow Leopard Cloud → SQL → PostgreSQL execution
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
  c.category_name, 
  SUM(t.amount) AS total_spending
FROM transactions t
JOIN categories c ON t.category_id = c.category_id
WHERE t.transaction_type = 'debit'
GROUP BY c.category_name
ORDER BY total_spending DESC
```

**Stage 4: Raw Results (from PostgreSQL)**

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

Try these in the CLI. The sample data covers January 2018 through September 2019, so ask about those months rather
than "this month".

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
You: Compare March 2019 vs February 2019
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
- **Sample data is from a public Kaggle dataset** → Use your own real data if you like
- **Queries go to Snow Leopard Cloud** → It generates and runs the SQL against your database
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
echo "SNOWLEOPARD_API_KEY=your_key" >> .env
```

### "No rows returned"

```bash
# 1. Enable debug mode
sed -i 's/DEBUG=False/DEBUG=True/' .env

# 2. Run and check logs
python main.py

# 3. Look for: "[Snow Leopard] ✓ Extracted N rows"
# If N=0, check that finance_coach.sql loaded into the database attached to your instance,
# and that your question refers to dates the dataset covers (2018-01 through 2019-09)
```

### "ImportError: No module named 'snowleopard'"

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### "query failed" or a data source error

```bash
# Confirm the instance can see the tables by asking it directly:
snowy retrieve --instance "$SNOWLEOPARD_INSTANCE_ID" "How many transactions are there?"

# If that fails, re-check the data source credentials on your instance page at https://cloud.snowleopard.ai
```

---

## 📚 Learn More

- **Snowleopard Docs:** https://docs.snowleopard.ai
- **LangGraph Docs:** https://langchain-ai.github.io/langgraph/
- **Pydantic Docs:** https://docs.pydantic.dev/

---

**Happy coaching! 💡**
