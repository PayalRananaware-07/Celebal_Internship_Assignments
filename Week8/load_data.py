import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('../ecommerce.db')

# Load CSV files
customers = pd.read_csv('../data/cleaned/customers_cleaned.csv')
products = pd.read_csv('../data/cleaned/products_cleaned.csv')
orders = pd.read_csv('../data/cleaned/orders_cleaned.csv')
order_items = pd.read_csv('../data/cleaned/order_items_cleaned.csv')

# Insert into database
customers.to_sql('customers', conn, if_exists='replace', index=False)
products.to_sql('products', conn, if_exists='replace', index=False)
orders.to_sql('orders', conn, if_exists='replace', index=False)
order_items.to_sql('order_items', conn, if_exists='replace', index=False)

conn.close()

print("Data loaded successfully!")