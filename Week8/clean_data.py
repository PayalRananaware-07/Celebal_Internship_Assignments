import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

raw_path = os.path.join(BASE_DIR, "data", "raw")
clean_path = os.path.join(BASE_DIR, "data", "cleaned")
report_path = os.path.join(BASE_DIR, "reports")

os.makedirs(clean_path, exist_ok=True)
os.makedirs(report_path, exist_ok=True)

issues = []

# ------------------ LOAD DATA ------------------
customers = pd.read_csv(os.path.join(raw_path, "customers.csv"))
products = pd.read_csv(os.path.join(raw_path, "products.csv"))
orders = pd.read_csv(os.path.join(raw_path, "orders.csv"))
order_items = pd.read_csv(os.path.join(raw_path, "order_items.csv"))

# ------------------ CLEAN CUSTOMERS ------------------
before = len(customers)

customers = customers[customers["email"].str.contains("@", na=False)]

after = len(customers)
issues.append(f"Customers: Removed {before - after} invalid emails")

# ------------------ CLEAN PRODUCTS ------------------
products["product_name"] = products["product_name"].str.strip().str.title()

# ------------------ CLEAN ORDERS ------------------
before = len(orders)

orders = orders.dropna(subset=["customer_id"])

# fix date format
orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")

after = len(orders)
issues.append(f"Orders: Removed {before - after} rows with NULL customer_id")

# ------------------ CLEAN ORDER ITEMS ------------------
before = len(order_items)

order_items = order_items[order_items["quantity"] > 0]

after = len(order_items)
issues.append(f"Order Items: Removed {before - after} negative quantity rows")

# ------------------ SAVE CLEAN DATA ------------------
customers.to_csv(os.path.join(clean_path, "customers_cleaned.csv"), index=False)
products.to_csv(os.path.join(clean_path, "products_cleaned.csv"), index=False)
orders.to_csv(os.path.join(clean_path, "orders_cleaned.csv"), index=False)
order_items.to_csv(os.path.join(clean_path, "order_items_cleaned.csv"), index=False)

# ------------------ SAVE REPORT ------------------
with open(os.path.join(report_path, "issues_report.txt"), "w") as f:
    for issue in issues:
        f.write(issue + "\n")

print("Data cleaned successfully!")