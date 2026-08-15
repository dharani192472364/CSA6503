import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

# Enable foreign keys
cursor.execute("PRAGMA foreign_keys = ON")

# Drop old tables
cursor.execute("DROP TABLE IF EXISTS order_items")
cursor.execute("DROP TABLE IF EXISTS orders")
cursor.execute("DROP TABLE IF EXISTS products")
cursor.execute("DROP TABLE IF EXISTS customers")

# -----------------------------
# Create tables
# -----------------------------

cursor.execute("""
CREATE TABLE customers (
    cust_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT,
    join_date TEXT,
    segment TEXT
)
""")

cursor.execute("""
CREATE TABLE products (
    prod_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    unit_price REAL
)
""")

cursor.execute("""
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    cust_id INTEGER,
    order_date TEXT,
    status TEXT,
    FOREIGN KEY (cust_id) REFERENCES customers(cust_id)
)
""")

cursor.execute("""
CREATE TABLE order_items (
    order_id INTEGER,
    prod_id INTEGER,
    qty INTEGER,
    discount_pct REAL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (prod_id) REFERENCES products(prod_id)
)
""")

# -----------------------------
# Insert customers
# -----------------------------

customers = [
    (1, "Arun Kumar", "Chennai", "2024-01-15", "Retail"),
    (2, "Priya Sharma", "Bangalore", "2024-02-20", "Premium"),
    (3, "Rahul Singh", "Mumbai", "2024-03-10", "Retail"),
    (4, "Meena Devi", "Chennai", "2024-04-05", "Premium"),
    (5, "Karthik Raj", "Hyderabad", "2024-05-12", "Retail"),
    (6, "Anita Rao", "Pune", "2024-06-18", "Premium"),
    (7, "Vijay Kumar", "Chennai", "2024-07-22", "Retail"),
    (8, "Sneha Patel", "Delhi", "2024-08-14", "Premium"),
    (9, "Ravi Shankar", "Coimbatore", "2024-09-01", "Retail"),
    (10, "Divya Menon", "Kochi", "2024-10-11", "Premium")
]

cursor.executemany("""
INSERT INTO customers
(cust_id, name, city, join_date, segment)
VALUES (?, ?, ?, ?, ?)
""", customers)

# -----------------------------
# Insert products
# -----------------------------

products = [
    (1, "Laptop", "Electronics", 60000),
    (2, "Phone", "Electronics", 30000),
    (3, "Headphones", "Accessories", 3000),
    (4, "Keyboard", "Accessories", 1500),
    (5, "Office Chair", "Furniture", 8000),
    (6, "Desk", "Furniture", 12000),
    (7, "Monitor", "Electronics", 18000),
    (8, "Mouse", "Accessories", 1000)
]

cursor.executemany("""
INSERT INTO products
(prod_id, name, category, unit_price)
VALUES (?, ?, ?, ?)
""", products)

# -----------------------------
# Insert orders
# -----------------------------

orders = [
    (101, 1, "2025-01-10", "COMPLETED"),
    (102, 2, "2025-01-20", "COMPLETED"),
    (103, 3, "2025-02-15", "COMPLETED"),
    (104, 4, "2025-03-05", "COMPLETED"),
    (105, 5, "2025-04-10", "COMPLETED"),
    (106, 6, "2025-04-25", "COMPLETED"),
    (107, 7, "2025-05-15", "COMPLETED"),
    (108, 8, "2025-06-20", "COMPLETED"),
    (109, 9, "2025-07-10", "COMPLETED"),
    (110, 10, "2025-08-05", "COMPLETED"),
    (111, 1, "2025-09-12", "COMPLETED"),
    (112, 2, "2025-10-18", "COMPLETED"),
    (113, 3, "2025-11-22", "COMPLETED"),
    (114, 4, "2025-12-15", "COMPLETED"),

    (115, 5, "2026-01-10", "COMPLETED"),
    (116, 6, "2026-01-25", "COMPLETED"),
    (117, 7, "2026-02-12", "COMPLETED"),
    (118, 8, "2026-02-28", "COMPLETED"),
    (119, 9, "2026-03-15", "COMPLETED"),
    (120, 10, "2026-03-25", "COMPLETED"),
    (121, 1, "2026-04-10", "COMPLETED"),
    (122, 2, "2026-04-20", "COMPLETED"),
    (123, 3, "2026-05-05", "COMPLETED"),
    (124, 4, "2026-05-18", "COMPLETED"),
    (125, 5, "2026-06-10", "COMPLETED"),
    (126, 6, "2026-06-25", "COMPLETED"),
    (127, 7, "2026-07-08", "COMPLETED"),
    (128, 8, "2026-07-20", "COMPLETED"),
    (129, 9, "2026-08-01", "COMPLETED"),
    (130, 10, "2026-08-05", "CANCELLED")
]

cursor.executemany("""
INSERT INTO orders
(order_id, cust_id, order_date, status)
VALUES (?, ?, ?, ?)
""", orders)

# -----------------------------
# Insert order items
# -----------------------------

order_items = [
    (101, 1, 2, 5),
    (102, 2, 3, 10),
    (103, 3, 5, 0),
    (104, 5, 2, 5),
    (105, 6, 3, 0),
    (106, 7, 2, 5),
    (107, 4, 5, 10),
    (108, 8, 10, 0),
    (109, 1, 1, 5),
    (110, 2, 2, 0),
    (111, 3, 8, 5),
    (112, 7, 3, 10),
    (113, 5, 4, 0),
    (114, 6, 2, 5),

    (115, 1, 1, 5),
    (116, 2, 2, 10),
    (117, 3, 10, 0),
    (118, 4, 8, 5),
    (119, 5, 3, 0),
    (120, 6, 2, 5),
    (121, 1, 1, 0),
    (122, 7, 2, 10),
    (123, 3, 2, 0),
    (124, 5, 1, 5),
    (125, 6, 4, 0),
    (126, 2, 3, 5),
    (127, 8, 5, 0),
    (128, 4, 2, 10),
    (129, 1, 2, 5),
    (130, 2, 5, 0)
]

cursor.executemany("""
INSERT INTO order_items
(order_id, prod_id, qty, discount_pct)
VALUES (?, ?, ?, ?)
""", order_items)

conn.commit()

# -----------------------------
# Verify inserted records
# -----------------------------

cursor.execute("SELECT COUNT(*) FROM customers")
customer_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM products")
product_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM orders")
order_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM order_items")
item_count = cursor.fetchone()[0]

print("=" * 60)
print("EXERCISE 9 - DATABASE SETUP")
print("=" * 60)
print("Database created successfully.")
print(f"Customers inserted   : {customer_count}")
print(f"Products inserted    : {product_count}")
print(f"Orders inserted      : {order_count}")
print(f"Order items inserted : {item_count}")
print("Database ready for SQL verification.")

# ============================================================
# QUERY 1 - MONTH-OVER-MONTH REVENUE GROWTH
# ============================================================

conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

query1 = """
WITH monthly_revenue AS (
    SELECT
        strftime('%Y-%m', o.order_date) AS month,
        p.category AS category,
        SUM(
            oi.qty * p.unit_price *
            (1 - oi.discount_pct / 100.0)
        ) AS revenue
    FROM orders AS o
    JOIN order_items AS oi
        ON o.order_id = oi.order_id
    JOIN products AS p
        ON oi.prod_id = p.prod_id
    WHERE o.status <> 'CANCELLED'
      AND o.order_date >= date('2025-09-01')
    GROUP BY
        strftime('%Y-%m', o.order_date),
        p.category
),

revenue_with_previous AS (
    SELECT
        month,
        category,
        revenue,
        LAG(revenue) OVER (
            PARTITION BY category
            ORDER BY month
        ) AS previous_revenue
    FROM monthly_revenue
)

SELECT
    month,
    category,
    ROUND(revenue, 2) AS revenue,
    ROUND(previous_revenue, 2) AS previous_revenue,
    ROUND(
        CASE
            WHEN previous_revenue IS NULL
                 OR previous_revenue = 0
            THEN NULL
            ELSE
                ((revenue - previous_revenue)
                 / previous_revenue) * 100
        END,
        2
    ) AS mom_growth_pct
FROM revenue_with_previous
ORDER BY month, category;
"""

try:
    print("\n" + "=" * 80)
    print("QUERY 1 - MONTH-OVER-MONTH REVENUE GROWTH")
    print("=" * 80)

    cursor.execute(query1)
    results = cursor.fetchall()

    print(
        f"{'Month':<12}"
        f"{'Category':<18}"
        f"{'Revenue':<15}"
        f"{'Previous':<15}"
        f"{'MoM Growth %':<15}"
    )

    print("-" * 75)

    for row in results:
        print(
            f"{str(row[0]):<12}"
            f"{str(row[1]):<18}"
            f"{str(row[2]):<15}"
            f"{str(row[3]):<15}"
            f"{str(row[4]):<15}"
        )

    print("\nQuery 1 executed successfully.")
    query1_status = "YES"

except Exception as e:
    print("\nQuery 1 FAILED.")
    print("Error:", e)
    query1_status = "NO"

conn.close()
# ============================================================
# QUERY 2 - TOP 5 CUSTOMERS BY LIFETIME VALUE
# ============================================================

conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

query2 = """
WITH customer_ltv AS (
    SELECT
        c.cust_id AS cust_id,
        c.name AS customer_name,
        SUM(
            oi.qty * p.unit_price *
            (1 - oi.discount_pct / 100.0)
        ) AS lifetime_value
    FROM customers AS c
    JOIN orders AS o
        ON c.cust_id = o.cust_id
    JOIN order_items AS oi
        ON o.order_id = oi.order_id
    JOIN products AS p
        ON oi.prod_id = p.prod_id
    WHERE o.status <> 'CANCELLED'
    GROUP BY
        c.cust_id,
        c.name
)

SELECT
    cust_id,
    customer_name,
    ROUND(lifetime_value, 2) AS lifetime_value
FROM customer_ltv
ORDER BY lifetime_value DESC
LIMIT 5;
"""

try:
    print("\n" + "=" * 80)
    print("QUERY 2 - TOP 5 CUSTOMERS BY LIFETIME VALUE")
    print("=" * 80)

    cursor.execute(query2)
    results = cursor.fetchall()

    print(
        f"{'Customer ID':<15}"
        f"{'Customer Name':<20}"
        f"{'Lifetime Value':<20}"
    )

    print("-" * 55)

    for row in results:
        print(
            f"{str(row[0]):<15}"
            f"{str(row[1]):<20}"
            f"{str(row[2]):<20}"
        )

    print("\nQuery 2 executed successfully.")
    query2_status = "YES"

except Exception as e:
    print("\nQuery 2 FAILED.")
    print("Error:", e)
    query2_status = "NO"

conn.close()

# ============================================================
# QUERY 3 - PRODUCTS WITH SALES DROP > 30% QUARTER-OVER-QUARTER
# ============================================================

conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

query3 = """
WITH quarterly_sales AS (
    SELECT
        p.prod_id AS prod_id,
        p.name AS product_name,
        strftime('%Y', o.order_date) || '-Q' ||
        ((CAST(strftime('%m', o.order_date) AS INTEGER) - 1) / 3 + 1)
        AS quarter,
        SUM(
            oi.qty * p.unit_price *
            (1 - oi.discount_pct / 100.0)
        ) AS revenue
    FROM products AS p
    JOIN order_items AS oi
        ON p.prod_id = oi.prod_id
    JOIN orders AS o
        ON oi.order_id = o.order_id
    WHERE o.status <> 'CANCELLED'
    GROUP BY
        p.prod_id,
        p.name,
        strftime('%Y', o.order_date),
        ((CAST(strftime('%m', o.order_date) AS INTEGER) - 1) / 3 + 1)
),

sales_with_previous AS (
    SELECT
        prod_id,
        product_name,
        quarter,
        revenue,
        LAG(revenue) OVER (
            PARTITION BY prod_id
            ORDER BY quarter
        ) AS previous_revenue
    FROM quarterly_sales
)

SELECT
    prod_id,
    product_name,
    quarter,
    ROUND(revenue, 2) AS revenue,
    ROUND(previous_revenue, 2) AS previous_revenue,
    ROUND(
        ((revenue - previous_revenue) / previous_revenue) * 100,
        2
    ) AS change_pct
FROM sales_with_previous
WHERE previous_revenue IS NOT NULL
  AND revenue < previous_revenue * 0.70
ORDER BY change_pct;
"""

try:
    print("\n" + "=" * 90)
    print("QUERY 3 - PRODUCTS WITH SALES DROP > 30% QOQ")
    print("=" * 90)

    cursor.execute(query3)
    results = cursor.fetchall()

    print(
        f"{'ID':<8}"
        f"{'Product':<20}"
        f"{'Quarter':<12}"
        f"{'Revenue':<15}"
        f"{'Previous':<15}"
        f"{'Change %':<12}"
    )

    print("-" * 82)

    for row in results:
        print(
            f"{str(row[0]):<8}"
            f"{str(row[1]):<20}"
            f"{str(row[2]):<12}"
            f"{str(row[3]):<15}"
            f"{str(row[4]):<15}"
            f"{str(row[5]):<12}"
        )

    print("\nQuery 3 executed successfully.")
    query3_status = "YES"

except Exception as e:
    print("\nQuery 3 FAILED.")
    print("Error:", e)
    query3_status = "NO"



# ============================================================
# QUERY 4 - CUSTOMERS WHO PURCHASED IN Q1 BUT NOT IN Q2
# ============================================================

query4 = """
WITH q1_customers AS (
    SELECT DISTINCT o.cust_id
    FROM orders o
    WHERE o.order_date >= '2026-01-01'
      AND o.order_date < '2026-04-01'
      AND o.status <> 'CANCELLED'
),
q2_customers AS (
    SELECT DISTINCT o.cust_id
    FROM orders o
    WHERE o.order_date >= '2026-04-01'
      AND o.order_date < '2026-07-01'
      AND o.status <> 'CANCELLED'
)
SELECT
    c.cust_id AS customer_id,
    c.name AS customer_name,
    c.city AS city,
    c.segment AS segment
FROM customers c
JOIN q1_customers q1
    ON c.cust_id = q1.cust_id
LEFT JOIN q2_customers q2
    ON c.cust_id = q2.cust_id
WHERE q2.cust_id IS NULL
ORDER BY c.cust_id;
"""

cursor.execute(query4)

results = cursor.fetchall()

print("\n" + "=" * 60)
print("QUERY 4 - Q1 CUSTOMERS WHO DID NOT PURCHASE IN Q2")
print("=" * 60)

if results:
    print(f"{'Customer ID':<15}{'Customer Name':<20}{'City':<15}{'Segment'}")

    for row in results:
        print(
            f"{row[0]:<15}"
            f"{row[1]:<20}"
            f"{row[2]:<15}"
            f"{row[3]}"
        )
else:
    print("No churn candidates found.")

print("\nQuery 4 executed successfully.")

conn.close()