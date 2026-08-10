import sqlite3

#  FIXED PATH (use forward slash)
conn = sqlite3.connect("C:/Users/nikhi/Desktop/Celebal/Week_8_Assignment/Ecommerce_Analytics/ecommerce.db")
cursor = conn.cursor()

#  Test 1: order_items without matching order
def test_invalid_order_id():
    cursor.execute("""
    SELECT COUNT(*)
    FROM order_items oi
    LEFT JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_id IS NULL;
    """)
    result = cursor.fetchone()[0]
    print("Invalid order_id rows:", result)

#  Test 2: discount > 100
def test_invalid_discount():
    cursor.execute("""
    SELECT COUNT(*)
    FROM order_items
    WHERE discount_percent > 100;
    """)
    result = cursor.fetchone()[0]
    print("Discount > 100 rows:", result)

#  Test 3: quantity = 0
def test_zero_quantity():
    cursor.execute("""
    SELECT COUNT(*)
    FROM order_items
    WHERE quantity = 0;
    """)
    result = cursor.fetchone()[0]
    print("Zero quantity rows:", result)

#  Test 4: future order dates
def test_future_dates():
    cursor.execute("""
    SELECT COUNT(*)
    FROM orders
    WHERE order_date > date('now');
    """)
    result = cursor.fetchone()[0]
    print("Future orders:", result)

#  RUN ALL TESTS
print("\n EDGE CASE TEST RESULTS\n")

test_invalid_order_id()
test_invalid_discount()
test_zero_quantity()
test_future_dates()

conn.close()