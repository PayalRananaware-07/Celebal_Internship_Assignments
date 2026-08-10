import pandas as pd
import random
from faker import Faker

fake = Faker()

# Function 1: Generate Customers
def generate_customers(n=500):
    customers = []

    for i in range(1, n+1):
        email = fake.email()

        # 2% invalid emails
        if random.random() < 0.02:
            email = email.replace("@", "")  # invalid

        customers.append({
            "customer_id": i,
            "customer_name": fake.name(),
            "email": email,
            "registration_date": fake.date_time_this_decade(),
            "customer_type": random.choice(["REGULAR", "PREMIUM", "VIP"])
        })

    return pd.DataFrame(customers)

# Function 2: Generate Products
def generate_products(n=500):
    categories = ["Electronics", "Clothing", "Home", "Books"]
    products = []

    for i in range(1, n+1):
        name = fake.word()

        # messy names
        if random.random() < 0.1:
            name = " " + name.upper() + " "

        products.append({
            "product_id": i,
            "product_name": name,
            "category": random.choice(categories),
            "subcategory": fake.word(),
            "cost_price": round(random.uniform(10, 1000), 2)
        })

    return pd.DataFrame(products)

# Function 3: Generate Orders
def generate_orders(customers_df, n=500):
    orders = []

    for i in range(1, n+1):
        customer_id = random.choice(customers_df["customer_id"].tolist())

        # 5% NULL customer_id
        if random.random() < 0.05:
            customer_id = None

        order_date = fake.date_time_this_year()

        # wrong format
        if random.random() < 0.05:
            order_date = order_date.strftime("%d-%m-%Y")

        orders.append({
            "order_id": i,
            "customer_id": customer_id,
            "order_date": order_date,
            "status": random.choice(["PLACED", "SHIPPED", "DELIVERED", "CANCELLED", "RETURNED"]),
            "region_code": random.choice(["NORTH", "SOUTH", "EAST", "WEST"])
        })

    return pd.DataFrame(orders)

# Function 4: Generate Order Items
def generate_order_items(orders_df, products_df, n=700):
    items = []

    for i in range(1, n+1):
        quantity = random.randint(1, 5)

        # 3% negative quantity
        if random.random() < 0.03:
            quantity = -quantity

        items.append({
            "item_id": i,
            "order_id": random.choice(orders_df["order_id"].tolist()),
            "product_id": random.choice(products_df["product_id"].tolist()),
            "quantity": quantity,
            "unit_price": round(random.uniform(20, 500), 2),
            "discount_percent": round(random.uniform(0, 30), 2)
        })

    return pd.DataFrame(items)


import os

if __name__ == "__main__":
    customers = generate_customers()
    products = generate_products()
    orders = generate_orders(customers)
    order_items = generate_order_items(orders, products)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(BASE_DIR, "data", "raw")

    # ensure folder exists
    os.makedirs(raw_path, exist_ok=True)

    customers.to_csv(os.path.join(raw_path, "customers.csv"), index=False)
    products.to_csv(os.path.join(raw_path, "products.csv"), index=False)
    orders.to_csv(os.path.join(raw_path, "orders.csv"), index=False)
    order_items.to_csv(os.path.join(raw_path, "order_items.csv"), index=False)

    print("Data generated successfully!")