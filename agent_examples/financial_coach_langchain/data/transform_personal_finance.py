# transform_personal_finance.py
import pandas as pd
import sqlite3
from datetime import datetime
import os

def transform_csv_to_sqlite(csv_file, db_name='finance_coach.db'):
    """
    Transform personal finance CSV into normalized SQLite database.
    
    CSV Columns Expected:
    - Date (YYYY-MM-DD)
    - Description (merchant name)
    - Amount (numeric)
    - Transaction Type (debit/credit)
    - Category (expense category)
    - Account Name (account type)
    - Month (YYYY-MM)
    """
    
    print("Loading CSV file...")
    df = pd.read_csv(csv_file)
    
    # Data cleaning
    df['Date'] = pd.to_datetime(df['Date'])
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    df = df.dropna(subset=['Amount', 'Date'])
    
    print(f"✓ Loaded {len(df)} transactions from {csv_file}")
    
    # Create database connection
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # ===== TABLE 1: USERS =====
    print("Creating Users table...")
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        created_date TEXT,
        email TEXT
    )
    ''')
    
    cursor.execute("INSERT OR IGNORE INTO users (name, created_date) VALUES (?, ?)",
                   ("Default User", datetime.now().strftime("%Y-%m-%d")))
    user_id = 1
    print(f"✓ Created users table (user_id={user_id})")
    
    # ===== TABLE 2: ACCOUNTS =====
    print("Creating Accounts table...")
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        account_name TEXT NOT NULL UNIQUE,
        account_type TEXT,
        created_date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    ''')
    
    unique_accounts = df['Account Name'].unique()
    account_mapping = {}
    
    for idx, account_name in enumerate(unique_accounts, 1):
        cursor.execute(
            "INSERT OR IGNORE INTO accounts (user_id, account_name, account_type, created_date) VALUES (?, ?, ?, ?)",
            (user_id, account_name, "checking" if "Checking" in account_name else "credit",
             datetime.now().strftime("%Y-%m-%d"))
        )
        account_mapping[account_name] = idx
    
    print(f"✓ Created accounts table ({len(unique_accounts)} accounts)")
    
    # ===== TABLE 3: CATEGORIES =====
    print("Creating Categories table...")
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT NOT NULL UNIQUE,
        category_type TEXT,
        description TEXT
    )
    ''')
    
    unique_categories = df['Category'].unique()
    category_mapping = {}
    
    for idx, category in enumerate(unique_categories, 1):
        category_type = "income" if category == "Income" or "Salary" in category else "expense"
        cursor.execute(
            "INSERT OR IGNORE INTO categories (category_name, category_type) VALUES (?, ?)",
            (category, category_type)
        )
        category_mapping[category] = idx
    
    print(f"✓ Created categories table ({len(unique_categories)} categories)")
    
    # ===== TABLE 4: MERCHANTS =====
    print("Creating Merchants table...")
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS merchants (
        merchant_id INTEGER PRIMARY KEY AUTOINCREMENT,
        merchant_name TEXT NOT NULL UNIQUE,
        category_id INTEGER,
        merchant_type TEXT,
        FOREIGN KEY(category_id) REFERENCES categories(category_id)
    )
    ''')
    
    unique_merchants = df['Description'].unique()
    merchant_mapping = {}
    
    for idx, merchant in enumerate(unique_merchants, 1):
        # Try to infer category from merchant name and data
        merchant_category = df[df['Description'] == merchant]['Category'].iloc
        category_id = category_mapping.get(merchant_category, 1)
        
        cursor.execute(
            "INSERT OR IGNORE INTO merchants (merchant_name, category_id) VALUES (?, ?)",
            (merchant, category_id)
        )
        merchant_mapping[merchant] = idx
    
    print(f"✓ Created merchants table ({len(unique_merchants)} merchants)")
    
    # ===== TABLE 5: TRANSACTIONS =====
    print("Creating Transactions table...")
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        account_id INTEGER NOT NULL,
        merchant_id INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        transaction_date TEXT NOT NULL,
        amount REAL NOT NULL,
        transaction_type TEXT,
        month TEXT,
        description TEXT,
        created_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id),
        FOREIGN KEY(account_id) REFERENCES accounts(account_id),
        FOREIGN KEY(merchant_id) REFERENCES merchants(merchant_id),
        FOREIGN KEY(category_id) REFERENCES categories(category_id)
    )
    ''')
    
    # Insert transactions
    for idx, row in df.iterrows():
        account_id = account_mapping.get(row['Account Name'], 1)
        category_id = category_mapping.get(row['Category'], 1)
        merchant_id = merchant_mapping.get(row['Description'], 1)
        
        cursor.execute('''
        INSERT INTO transactions 
        (user_id, account_id, merchant_id, category_id, transaction_date, 
         amount, transaction_type, month, description, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            account_id,
            merchant_id,
            category_id,
            row['Date'].strftime("%Y-%m-%d"),
            row['Amount'],
            row['Transaction Type'].lower(),
            row['Month'],
            row['Description'],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
    
    print(f"✓ Created transactions table ({len(df)} transactions)")
    
    # ===== CREATE INDICES =====
    print("Creating indices for performance...")
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_trans_date ON transactions(transaction_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_trans_category ON transactions(category_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_trans_account ON transactions(account_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_trans_merchant ON transactions(merchant_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_trans_user ON transactions(user_id)')
    
    # ===== CREATE VIEWS =====
    print("Creating useful views...")
    
    # View: Spending by category
    cursor.execute('''
    CREATE VIEW IF NOT EXISTS vw_spending_by_category AS
    SELECT 
        c.category_name,
        SUM(t.amount) as total_spent,
        COUNT(*) as transaction_count,
        AVG(t.amount) as avg_transaction
    FROM transactions t
    JOIN categories c ON t.category_id = c.category_id
    WHERE t.transaction_type = 'debit'
    GROUP BY c.category_name
    ORDER BY total_spent DESC
    ''')
    
    # View: Monthly spending
    cursor.execute('''
    CREATE VIEW IF NOT EXISTS vw_monthly_spending AS
    SELECT 
        t.month,
        SUM(CASE WHEN t.transaction_type = 'debit' THEN t.amount ELSE 0 END) as total_expenses,
        SUM(CASE WHEN t.transaction_type = 'credit' THEN t.amount ELSE 0 END) as total_income,
        COUNT(*) as transaction_count
    FROM transactions t
    GROUP BY t.month
    ORDER BY t.month DESC
    ''')
    
    # View: Top merchants
    cursor.execute('''
    CREATE VIEW IF NOT EXISTS vw_top_merchants AS
    SELECT 
        m.merchant_name,
        c.category_name,
        SUM(t.amount) as total_spent,
        COUNT(*) as frequency
    FROM transactions t
    JOIN merchants m ON t.merchant_id = m.merchant_id
    JOIN categories c ON t.category_id = c.category_id
    WHERE t.transaction_type = 'debit'
    GROUP BY m.merchant_id
    ORDER BY total_spent DESC
    ''')
    
    print("✓ Created views (vw_spending_by_category, vw_monthly_spending, vw_top_merchants)")
    
    # Commit and close
    conn.commit()
    
    # Get database statistics
    db_size_mb = os.path.getsize(db_name) / (1024 * 1024)
    
    print("\n" + "="*60)
    print("✅ TRANSFORMATION COMPLETE")
    print("="*60)
    print(f"Database: {db_name}")
    print(f"Size: {db_size_mb:.2f} MB")
    print(f"\nTables Created:")
    print(f"  - users: 1 record")
    print(f"  - accounts: {len(unique_accounts)} records")
    print(f"  - categories: {len(unique_categories)} records")
    print(f"  - merchants: {len(unique_merchants)} records")
    print(f"  - transactions: {len(df)} records")
    print(f"\nIndices: 5 created (for fast queries)")
    print(f"Views: 3 created (for Snow Leopard queries)")
    print("="*60)
    
    conn.close()
    return db_name

if __name__ == "__main__":
    # Usage
    csv_file = "data/personal_finance/personal_transactions_dashboard_ready(2).csv"  # Your downloaded CSV
    
    # Check if file exists
    if not os.path.exists(csv_file):
        print(f"❌ Error: {csv_file} not found!")
        print("Please download the dataset first:")
        print("  kaggle datasets download -d entrepreneurlife/personal-finance")
        exit(1)
    
    # Transform
    db_path = transform_csv_to_sqlite(csv_file)
    print(f"\n✓ Ready for Snow Leopard: {db_path}")
