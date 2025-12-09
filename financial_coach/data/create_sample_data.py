#!/usr/bin/env python3
"""
Sample Financial Data Generator

Generates a realistic SQLite database with 6 months of personal finance transactions.
This is perfect for testing the SnowleopardAI Financial Coach.

Usage:
    python scripts/create_sample_data.py

Output:
    Creates/updates: financial_data.db

Schema:
    CREATE TABLE transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_date TEXT,
        merchant_name TEXT,
        category_name TEXT,
        amount REAL,
        description TEXT
    )
"""

import sqlite3
import random
from datetime import datetime, timedelta
import os

# Sample data definitions
MERCHANTS = {
    'Groceries': [
        'Whole Foods',
        'Trader Joes',
        'Safeway',
        'Kroger',
        'Instacart',
        'Sprouts Farmers Market'
    ],
    'Dining': [
        'Chipotle',
        'Starbucks',
        'Panera Bread',
        'Chick-fil-A',
        'Subway',
        'Olive Garden',
        'The Cheesecake Factory',
        'Thai Palace',
        'Sushi Roll',
        'Pizza Hut'
    ],
    'Fuel': [
        'Shell Gas',
        'BP',
        'Chevron',
        'Exxon',
        'Valero',
        'Costco Gas',
        'QuikTrip'
    ],
    'Shopping': [
        'Amazon',
        'Target',
        'Walmart',
        'Best Buy',
        'Gap',
        'H&M',
        'Forever 21',
        'Nike Store'
    ],
    'Entertainment': [
        'Netflix',
        'Spotify',
        'Disney+',
        'Hulu',
        'AMC Theaters',
        'Regal Cinemas',
        'Dave & Busters'
    ],
    'Utilities': [
        'PG&E Electric',
        'Water Department',
        'Internet Provider',
        'Phone Bill'
    ],
    'Rent': [
        'Landlord Payment',
        'Property Management'
    ]
}

DESCRIPTIONS = {
    'Groceries': ['Weekly shopping', 'Groceries', 'Food shopping', 'Produce', 'Weekly stock'],
    'Dining': ['Lunch', 'Coffee', 'Dinner', 'Breakfast', 'Quick bite', 'Takeout'],
    'Fuel': ['Fill up', 'Gas', 'Fuel', 'Regular unleaded', 'Premium'],
    'Shopping': ['Online purchase', 'Store purchase', 'Impulse buy', 'Needed supplies'],
    'Entertainment': ['Monthly subscription', 'Streaming service', 'Concert tickets', 'Movie night'],
    'Utilities': ['Monthly bill', 'Service charge'],
    'Rent': ['Monthly rent', 'Rent payment']
}

AMOUNT_RANGES = {
    'Groceries': (50, 200),
    'Dining': (5, 50),
    'Fuel': (40, 80),
    'Shopping': (15, 150),
    'Entertainment': (10, 50),
    'Utilities': (50, 200),
    'Rent': (1200, 1500)
}


def generate_transactions(num_transactions=500, months_back=6):
    """Generate realistic financial transactions."""
    transactions = []
    
    # Start date: 6 months ago
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30 * months_back)
    
    # Rent should occur once a month on the 1st
    rent_dates = []
    current = start_date.replace(day=1)
    while current <= end_date:
        rent_dates.append(current)
        # Add one month
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)
    
    # Generate rent transactions
    for rent_date in rent_dates:
        category = 'Rent'
        merchant = random.choice(MERCHANTS[category])
        amount = random.uniform(*AMOUNT_RANGES[category])
        description = random.choice(DESCRIPTIONS[category])
        
        transactions.append({
            'date': rent_date.strftime('%Y-%m-%d'),
            'merchant': merchant,
            'category': category,
            'amount': amount,
            'description': description
        })
    
    # Generate other transactions
    remaining_count = num_transactions - len(rent_dates)
    
    for _ in range(remaining_count):
        # Random date within range
        random_days = random.randint(0, (end_date - start_date).days)
        transaction_date = start_date + timedelta(days=random_days)
        
        # Random category (weighted towards common categories)
        category = random.choices(
            list(MERCHANTS.keys()),
            weights=[4, 3, 2, 2, 1, 1, 1],  # Groceries most common
            k=1
        )[0]
        
        # Random merchant in category
        merchant = random.choice(MERCHANTS[category])
        
        # Random amount in range
        amount = random.uniform(*AMOUNT_RANGES[category])
        
        # Random description
        description = random.choice(DESCRIPTIONS[category])
        
        transactions.append({
            'date': transaction_date.strftime('%Y-%m-%d'),
            'merchant': merchant,
            'category': category,
            'amount': round(amount, 2),
            'description': description
        })
    
    # Sort by date
    transactions.sort(key=lambda x: x['date'])
    
    return transactions


def create_database(filename='financial_data.db'):
    """Create SQLite database with transactions."""
    
    # Remove if exists
    if os.path.exists(filename):
        os.remove(filename)
        print(f"✓ Removed existing {filename}")
    
    # Create connection
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_date TEXT NOT NULL,
            merchant_name TEXT NOT NULL,
            category_name TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT
        )
    ''')
    
    print(f"✓ Created table: transactions")
    
    # Generate and insert data
    print("📊 Generating sample transactions...")
    transactions = generate_transactions(num_transactions=500, months_back=6)
    
    for tx in transactions:
        cursor.execute('''
            INSERT INTO transactions 
            (transaction_date, merchant_name, category_name, amount, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            tx['date'],
            tx['merchant'],
            tx['category'],
            tx['amount'],
            tx['description']
        ))
    
    conn.commit()
    print(f"✓ Inserted {len(transactions)} transactions")
    
    # Create index for faster queries
    cursor.execute('''
        CREATE INDEX idx_transaction_date 
        ON transactions(transaction_date)
    ''')
    cursor.execute('''
        CREATE INDEX idx_category 
        ON transactions(category_name)
    ''')
    cursor.execute('''
        CREATE INDEX idx_merchant 
        ON transactions(merchant_name)
    ''')
    
    conn.commit()
    print(f"✓ Created indexes")
    
    # Show summary
    cursor.execute('SELECT COUNT(*) FROM transactions')
    total_rows = cursor.fetchone()[0]
    
    cursor.execute('SELECT SUM(amount) FROM transactions')
    total_amount = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT category_name, COUNT(*), SUM(amount)
        FROM transactions
        GROUP BY category_name
        ORDER BY SUM(amount) DESC
    ''')
    categories = cursor.fetchall()
    
    print(f"\n📈 Summary:")
    print(f"   Total transactions: {total_rows}")
    print(f"   Total spending: ${total_amount:,.2f}")
    print(f"\n   By category:")
    for cat_name, count, amount in categories:
        pct = (amount / total_amount * 100) if total_amount > 0 else 0
        print(f"     • {cat_name}: {count} tx, ${amount:,.2f} ({pct:.1f}%)")
    
    # Close connection
    conn.close()
    
    print(f"\n✅ Database created: {filename}")
    print(f"\nNext steps:")
    print(f"  1. Upload {filename} to https://playground.snowleopard.ai")
    print(f"  2. Copy the Datafile ID")
    print(f"  3. Paste into .env as SNOWLEOPARD_DATAFILE_ID")
    print(f"  4. Run: python main.py")


if __name__ == '__main__':
    # Create in project root
    db_path = 'financial_data.db'
    
    print("🚀 Creating sample financial dataset...\n")
    create_database(db_path)
