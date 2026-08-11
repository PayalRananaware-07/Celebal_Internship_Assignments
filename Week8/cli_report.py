import sqlite3
from datetime import datetime
import os

print("Current working dir:", os.getcwd())

#  Connect to DB (FIXED PATH)
conn = sqlite3.connect("C:/Users/nikhi/Desktop/Celebal/Week_8_Assignment/Ecommerce_Analytics/ecommerce.db")
cursor = conn.cursor()

#  USER INPUT
report_type = input("Enter report type (daily/weekly/monthly): ").lower()
start_date = input("Enter start date (YYYY-MM-DD): ")
end_date = input("Enter end date (YYYY-MM-DD): ")

#  Convert dates
start = datetime.strptime(start_date, "%Y-%m-%d")
end = datetime.strptime(end_date, "%Y-%m-%d")

# Previous period calculation
delta = end - start
prev_start = start - delta
prev_end = end - delta

#  MAIN QUERY
query = """
SELECT
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT o.customer_id) AS unique_customers,
    SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_date BETWEEN ? AND ?
"""

cursor.execute(query, (start_date, end_date))
current = cursor.fetchone()

cursor.execute(query, (prev_start.strftime("%Y-%m-%d"), prev_end.strftime("%Y-%m-%d")))
previous = cursor.fetchone()

#  TOP 3 PRODUCTS
top_products_query = """
SELECT p.product_name,
       SUM(oi.quantity) AS total_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_date BETWEEN ? AND ?
GROUP BY p.product_name
ORDER BY total_sold DESC
LIMIT 3;
"""

cursor.execute(top_products_query, (start_date, end_date))
top_products = cursor.fetchall()

#  % CHANGE FUNCTION
def percent_change(curr, prev):
    if prev is None or prev == 0 or curr is None:
        return "N/A"
    return round(((curr - prev) / prev) * 100, 2)

#  OUTPUT
print("\n REPORT")
print("Period:", start_date, "to", end_date)

print("\nTotal Orders:", current[0],
      "| Change:", percent_change(current[0], previous[0]))

print("Unique Customers:", current[1],
      "| Change:", percent_change(current[1], previous[1]))

print("Revenue:", current[2],
      "| Change:", percent_change(current[2], previous[2]))

print("\n Top 3 Products:")
for p in top_products:
    print(p[0], "-", p[1])

conn.close()