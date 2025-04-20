import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import random

def create_mock_database():
    # Create a connection to SQLite database
    conn = sqlite3.connect('mock_business_data.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
        date DATE,
        product_id INTEGER,
        quantity INTEGER,
        price DECIMAL(10,2),
        region TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        category TEXT,
        cost_price DECIMAL(10,2)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        region TEXT,
        customer_type TEXT
    )
    ''')

    # Insert mock products
    products = [
        (1, 'Laptop Pro', 'Electronics', 800.00),
        (2, 'Smartphone X', 'Electronics', 500.00),
        (3, 'Wireless Headphones', 'Accessories', 150.00),
        (4, 'Office Chair', 'Furniture', 200.00),
        (5, 'Desk Lamp', 'Furniture', 50.00)
    ]
    cursor.executemany('INSERT INTO products VALUES (?, ?, ?, ?)', products)

    # Insert mock customers
    customers = [
        (1, 'John Doe', 'North', 'Premium'),
        (2, 'Jane Smith', 'South', 'Regular'),
        (3, 'Bob Johnson', 'East', 'Premium'),
        (4, 'Alice Brown', 'West', 'Regular'),
        (5, 'Charlie Wilson', 'North', 'Premium')
    ]
    cursor.executemany('INSERT INTO customers VALUES (?, ?, ?, ?)', customers)

    # Generate mock sales data
    start_date = datetime(2023, 1, 1)
    sales_data = []
    for i in range(1, 101):  # 100 sales records
        date = start_date + timedelta(days=random.randint(0, 365))
        product_id = random.randint(1, 5)
        quantity = random.randint(1, 5)
        price = products[product_id-1][3] * (1 + random.uniform(0.1, 0.3))  # 10-30% markup
        region = random.choice(['North', 'South', 'East', 'West'])
        sales_data.append((i, date.strftime('%Y-%m-%d'), product_id, quantity, price, region))

    cursor.executemany('INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?)', sales_data)

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print("Mock database created successfully!")
    print("Database file: mock_business_data.db")
    print("Tables created: sales, products, customers")
    print("Sample data inserted for testing")

if __name__ == "__main__":
    create_mock_database() 