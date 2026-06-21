import pandas as pd
import sqlite3
import os

print("🚀 DATA WAREHOUSE PIPELINE STARTED")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("data/sales.csv")

print("\n📊 RAW DATA")
print(df)

# =========================
# TRANSFORM DATA
# =========================
df["total_amount"] = df["quantity"] * df["price"]

print("\n📊 TRANSFORMED DATA")
print(df)

# =========================
# CREATE DATABASE FOLDER
# =========================
os.makedirs("database", exist_ok=True)

# =========================
# CONNECT SQLITE DATABASE
# =========================
conn = sqlite3.connect("database/sales_warehouse.db")

# =========================
# LOAD DATA INTO SQL TABLE
# =========================
df.to_sql(
    "sales_fact",
    conn,
    if_exists="replace",
    index=False
)

cursor = conn.cursor()

# =========================
# BUSINESS QUERIES
# =========================

print("\n💰 TOTAL SALES")

cursor.execute("""
SELECT SUM(total_amount) FROM sales_fact
""")
print(cursor.fetchone()[0])

print("\n🏆 TOP PRODUCTS")

cursor.execute("""
SELECT product_name,
SUM(total_amount) AS revenue
FROM sales_fact
GROUP BY product_name
ORDER BY revenue DESC
""")

for row in cursor.fetchall():
    print(row)

print("\n👤 CUSTOMER REVENUE")

cursor.execute("""
SELECT customer_name,
SUM(total_amount) AS revenue
FROM sales_fact
GROUP BY customer_name
ORDER BY revenue DESC
""")

for row in cursor.fetchall():
    print(row)

# =========================
# CLOSE CONNECTION
# =========================
conn.close()

print("\n🎯 DATA WAREHOUSE CREATED SUCCESSFULLY")