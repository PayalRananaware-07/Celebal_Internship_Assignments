-- BASIC QUERIES

--  Q1: Total revenue per category
SELECT p.category,
       SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)) AS revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category;

-- Q2: Top 10 customers by total order value
SELECT o.customer_id,
       SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)) AS total_value
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.customer_id
ORDER BY total_value DESC
LIMIT 10;

-- Q3: Month-wise order count (last 12 months)
SELECT strftime('%Y-%m', order_date) AS month,
       COUNT(*) AS order_count
FROM orders
WHERE order_date >= date('now', '-12 months')
GROUP BY month
ORDER BY month;


-- INTERMEDIATE QUERIES
-- Q4: Customers who ordered but nothing delivered
SELECT customer_id
FROM orders
GROUP BY customer_id
HAVING SUM(CASE WHEN status = 'DELIVERED' THEN 1 ELSE 0 END) = 0;

-- Q5: Products with more returns than purchases
SELECT oi.product_id
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
GROUP BY oi.product_id
HAVING SUM(CASE WHEN o.status = 'RETURNED' THEN oi.quantity ELSE 0 END) >
       SUM(CASE WHEN o.status != 'RETURNED' THEN oi.quantity ELSE 0 END);

-- Q6: Return rate per category
SELECT p.category,
       SUM(CASE WHEN o.status = 'RETURNED' THEN oi.quantity ELSE 0 END) * 1.0 /
       SUM(oi.quantity) AS return_rate
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category;

-- ADVANCED QUERIES
-- Q7: Running total revenue per region
SELECT region_code,
       order_date,
       daily_revenue,
       SUM(daily_revenue) OVER (
           PARTITION BY region_code 
           ORDER BY order_date
       ) AS running_total
FROM (
    SELECT o.region_code,
           o.order_date,
           SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)) AS daily_revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.region_code, o.order_date
);
-- Q8: Ranking products within category
WITH revenue_data AS (
    SELECT p.category,
           p.product_name,
           SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)) AS total_revenue
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.category, p.product_name
)
SELECT *,
       DENSE_RANK() OVER (PARTITION BY category ORDER BY total_revenue DESC) AS rank_in_category
FROM revenue_data;

-- Q9: LAG — Days between orders
SELECT customer_id,
       order_date,
       LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_date,
       JULIANDAY(order_date) - JULIANDAY(LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date)) AS days_gap,
       CASE 
           WHEN JULIANDAY(order_date) - JULIANDAY(LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date)) > 30
           THEN 'At Risk'
           ELSE 'Normal'
       END AS risk_flag
FROM orders;

-- Q10: Customer segmentation (CTE)
WITH monthly AS (
    SELECT o.customer_id,
           strftime('%Y-%m', o.order_date) AS month,
           SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)) AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.customer_id, month
)
SELECT month,
       CASE 
           WHEN revenue > 10000 THEN 'High'
           WHEN revenue BETWEEN 5000 AND 10000 THEN 'Medium'
           ELSE 'Low'
       END AS segment,
       COUNT(DISTINCT customer_id) AS customer_count
FROM monthly
GROUP BY month, segment;

-- Q11: NTILE (quartiles)
WITH customer_value AS (
    SELECT o.customer_id,
           SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)) AS total_value
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.customer_id
)
SELECT *,
       NTILE(4) OVER (ORDER BY total_value DESC) AS quartile,
       CASE 
           WHEN NTILE(4) OVER (ORDER BY total_value DESC) = 1 THEN 'Platinum'
           WHEN NTILE(4) OVER (ORDER BY total_value DESC) = 2 THEN 'Gold'
           WHEN NTILE(4) OVER (ORDER BY total_value DESC) = 3 THEN 'Silver'
           ELSE 'Bronze'
       END AS quartile_label
FROM customer_value;

-- Q12: Year-over-Year Growth

WITH monthly AS (
    SELECT 
        strftime('%Y', o.order_date) AS year,
        strftime('%m', o.order_date) AS month,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100)) AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY year, month
)

SELECT 
    m1.year,
    m1.month,
    m1.revenue,
    m2.revenue AS prev_year_revenue,
    CASE 
        WHEN m2.revenue IS NULL THEN NULL
        ELSE ROUND((m1.revenue - m2.revenue) * 100.0 / m2.revenue, 2)
    END AS yoy_growth_percent
FROM monthly m1
LEFT JOIN monthly m2
    ON m1.month = m2.month
   AND m1.year = CAST(m2.year AS INTEGER) + 1
ORDER BY m1.year, m1.month;

-- Q13: First & Last Category
WITH customer_orders AS (
    SELECT 
        o.customer_id,
        o.order_date,
        p.category
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
)

SELECT DISTINCT
    customer_id,
    FIRST_VALUE(category) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) AS first_category,

    LAST_VALUE(category) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS last_category,

    CASE 
        WHEN FIRST_VALUE(category) OVER (
            PARTITION BY customer_id ORDER BY order_date
        ) 
        =
        LAST_VALUE(category) OVER (
            PARTITION BY customer_id ORDER BY order_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        )
        THEN 'No'
        ELSE 'Yes'
    END AS category_shift
FROM customer_orders;

-- Q14: Cumulative revenue %
WITH customer_revenue AS (
    SELECT 
        o.customer_id,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100)) AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.customer_id
)

SELECT 
    customer_id,
    revenue,
    SUM(revenue) OVER (ORDER BY revenue DESC) AS cumulative_revenue,
    ROUND(
        SUM(revenue) OVER (ORDER BY revenue DESC) * 100.0 /
        SUM(revenue) OVER (), 
    2) AS cumulative_percent
FROM customer_revenue
ORDER BY revenue DESC;

-- Q15: Cohort Analysis (simplified)
WITH customer_cohort AS (
    SELECT 
        customer_id,
        strftime('%Y-%m', registration_date) AS cohort_month
    FROM customers
),

orders_data AS (
    SELECT 
        o.customer_id,
        strftime('%Y-%m', o.order_date) AS order_month
    FROM orders o
),

cohort_activity AS (
    SELECT 
        c.cohort_month,
        o.order_month,
        c.customer_id,
        (CAST(strftime('%Y', o.order_month) AS INTEGER) - 
         CAST(strftime('%Y', c.cohort_month) AS INTEGER)) * 12 +
        (CAST(strftime('%m', o.order_month) AS INTEGER) - 
         CAST(strftime('%m', c.cohort_month) AS INTEGER)) 
        AS month_number
    FROM customer_cohort c
    JOIN orders_data o 
        ON c.customer_id = o.customer_id
)

SELECT 
    cohort_month,
    month_number,
    COUNT(DISTINCT customer_id) AS active_customers
FROM cohort_activity
GROUP BY cohort_month, month_number
ORDER BY cohort_month, month_number;




-- Q16: Frequently bought together
SELECT a.product_id AS product_a,
       b.product_id AS product_b,
       COUNT(*) AS times
FROM order_items a
JOIN order_items b
ON a.order_id = b.order_id AND a.product_id < b.product_id
GROUP BY product_a, product_b
ORDER BY times DESC;